print('importing...')
import pyaudio
from time import time, sleep
import numpy as np
from resampy import resample
from queue import Queue
from threading import Lock
import keyboard as kb
try:
    from yin import yin
except ImportError:
    print('Missing module "yin". Please download at')
    print('https://github.com/Daniel-Chin/Python_Lib/blob/master/yin.py')
    input('Press Enter to quit...')
from interactive import inputChin

print('Preparing constants...')
# CHORD = (0, -3, +4)
# CHORD = (0, -4, +3)
# CHORD = (0, -3.863137138648348, +3.1564128700055285)
CHORD = (0, +3.863137138648348, -3.1564128700055285)
# CHORD = (0, )
# CHORD = (0, -3)
# CHORD = (0, -7.019550008653873)
# CHORD = (0, -7.019550008653873, +7.019550008653873)
# CHORD = (0, -3.863137138648348, -7.019550008653873)
# CHORD = (0, -3.1564128700055285, )
QUANTIZE = False
HYSTERESIS = .2
PAGE_LEN = 512
CROSS_FADE = 0.04
DO_ECHO = True
ECHO_DELAY = .25
ECHO_DECAY = .3

SR = 44100
DTYPE = (np.float32, pyaudio.paFloat32)
# FILTER = 'kaiser_fast'
FILTER = 'kaiser_best'

FRAME_TIME = 1 / SR * PAGE_LEN
CROSS_FADE_TAILS = round(PAGE_LEN * (1 - CROSS_FADE) / 2)
CROSS_FADE_OVERLAP = PAGE_LEN - 2 * CROSS_FADE_TAILS
assert CROSS_FADE_OVERLAP + 2 * CROSS_FADE_TAILS == PAGE_LEN
# Linear cross fade
FADE_IN_WINDOW = np.array([
    x / CROSS_FADE_OVERLAP for x in range(CROSS_FADE_OVERLAP)
], DTYPE[0])
FADE_OUT_WINDOW = np.flip(FADE_IN_WINDOW)

streamOutContainer = []
display_time = 0
classification = 0
confidence = 0
tolerance = HYSTERESIS
time_start = 0
echo = [np.zeros(PAGE_LEN, DTYPE[0]) for _ in range(
    round(ECHO_DELAY * SR / PAGE_LEN)
)]
release_state = 0
lock = Lock()

def main():
    global release_state, mixer
    pa = pyaudio.PyAudio()
    mixer = np.zeros((len(CHORD), PAGE_LEN), DTYPE[0])
    info = pa.get_host_api_info_by_index(0)
    n_devices = info.get('deviceCount')
    devices = []
    in_devices = []
    out_devices = []
    for i in range(n_devices):
        info = pa.get_device_info_by_host_api_device_index(0, i)
        devices.append(info['name'])
        if info['maxInputChannels'] > 0:
            in_devices.append([i, info['name']])
        elif info['maxOutputChannels'] > 0:
            out_devices.append([i, info['name']])
    print()
    print('Input Devices:')
    for i, name in in_devices:
        print(i, name)
    default_in = guess(in_devices, ['Headset', 'Microphone Array'])
    in_i = int(inputChin('select input device: ', default_in))
    print()
    print('Input device:', devices[in_i])

    print()
    print('Output Devices:')
    for i, name in out_devices:
        print(i, name)
    default_out = guess(out_devices, ['VoiceMeeter Input'])
    out_i = int(inputChin('select output device: ', default_out))
    print()
    print('Output device:', devices[out_i])

    streamOutContainer.append(pa.open(
        format = DTYPE[1], channels = 1, rate = SR, 
        output = True, frames_per_buffer = PAGE_LEN,
        output_device_index = out_i, 
    ))
    streamIn = pa.open(
        format = DTYPE[1], channels = 1, rate = SR, 
        input = True, frames_per_buffer = PAGE_LEN,
        stream_callback = onAudioIn, 
        input_device_index = in_i, 
    )
    streamIn.start_stream()
    kb.hook(onKey)
    print('go...')
    try:
        while streamIn.is_active():
            sleep(1)
        # relay(stream, streamOut)
    except KeyboardInterrupt:
        print('Ctrl+C received. Shutting down. ')
    finally:
        lock.acquire()
        release_state = 1
        lock.acquire()
        lock.release()
        streamOutContainer[0].stop_stream()
        streamOutContainer[0].close()
        sleep(.4)   # not perfect
        streamIn.stop_stream()
        streamIn.close()
        pa.terminate()
        print('Resources released. ')
        kb.unhook_all()

def onAudioIn(in_data, frame_count, time_info, status):
    global classification, confidence, tolerance, release_state

    if release_state == 1:
        release_state = 2
        lock.release()
        return (None, pyaudio.paComplete)

    frame = np.frombuffer(
        in_data, dtype = DTYPE[0]
    )
    if QUANTIZE or len(CHORD) == 0:
        f0 = yin(frame, SR, PAGE_LEN)
        pitch = np.log(f0) * 17.312340490667562 - 36.37631656229591

    if len(CHORD):
        if QUANTIZE:
            classification = round(pitch / 7.9) * 7.9
            p2b = classification - pitch
        else:
            p2b = 0
        
        weight = (1 / (len(CHORD) - .99)) * .5
        for i, c in enumerate(CHORD):
            mixer[i] = pitchBend(frame, p2b + c) * (.5 if i == 0 else weight)
        frame = np.sum(mixer, 0)
    else:
        loss = abs(pitch - classification) - .5
        if loss < 0:
            tolerance = HYSTERESIS
        else:
            tolerance -= loss
            if tolerance < 0:
                classification = round(pitch / 2) * 2
        pitch_to_bend = classification - pitch
        # confident_correction = pitch_to_bend * confidence
        confident_correction = pitch_to_bend

        frame = pitchBend(frame, confident_correction)

    if DO_ECHO:
        frame += echo.pop(0)
        # echo.append((frame * ECHO_DECAY).astype(DTYPE[0]))
        echo.append(pitchBend((frame * ECHO_DECAY).astype(DTYPE[0]), 2))

    streamOutContainer[0].write(frame, PAGE_LEN)

    return (None, pyaudio.paContinue)

def pitchBend(frame, pitch_to_bend):
    if pitch_to_bend == 0:
        return frame
    freq_oitar = np.exp(- pitch_to_bend * 0.057762265046662105)
    # The inverse of 'ratio'
    frame = resample(frame, SR, SR * freq_oitar, filter=FILTER)
    left      = frame[:CROSS_FADE_TAILS]
    left_mid  = frame[CROSS_FADE_TAILS:CROSS_FADE_TAILS + CROSS_FADE_OVERLAP]
    right_mid = frame[-CROSS_FADE_TAILS - CROSS_FADE_OVERLAP:-CROSS_FADE_TAILS]
    right     = frame[-CROSS_FADE_TAILS:]
    frame = np.concatenate((
        left, 
        np.multiply(left_mid, FADE_OUT_WINDOW) 
        + np.multiply(right_mid, FADE_IN_WINDOW), 
        right,
    ))
    return frame

METER_WIDTH = 50
METER = '[' + ' ' * METER_WIDTH + '|' + ' ' * METER_WIDTH + ']'
METER_CENTER = METER_WIDTH + 1
TIMES = [
    'f0_time', 'hysteresis_time', 
    'bender_time', 'echo_time', 'write_time', 
    'display_time', 'idle_time',
]
def display(
    f0_time, bender_time, write_time, 
    display_time, pitch_to_bend, hysteresis_time, 
    idle_time, echo_time, 
):
    buffer_0 = [*METER]
    offset = - round(METER_WIDTH * pitch_to_bend)
    try:
        buffer_0[METER_CENTER + offset] = '#'
    except IndexError:
        print('爆表了：', pitch_to_bend)
    _locals = locals()
    print(*buffer_0, sep='')
    print('', *[x[:-5] + ' {:4.0%}.    '.format(_locals[x] / FRAME_TIME) for x in TIMES])

is_q_down = False
def onKey(x):
    global is_q_down
    if x.name == '0' and x.event_type == 'down':
        if is_q_down:
            kb.release('q')
        else:
            kb.press('q')
        is_q_down = not is_q_down
    if x.name == 'q' and x.event_type == 'up':
        is_q_down = False

def guess(devices, targets):
    for t in targets:
        for i, name in devices:
            if t in name:
                return i
    return ''

main()
