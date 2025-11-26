print('importing...')
import pyaudio
from time import time, sleep
import numpy as np
import scipy
from scipy import stats
from threading import Lock
from collections import namedtuple
import wave
import random
from resampy import resample
try:
    from interactive import listen
    from yin import yin
    from streamProfiler import StreamProfiler
    from harmonicSynth import HarmonicSynth, Harmonic
    from interactive import inputChin
except ImportError as e:
    module_name = str(e).split('No module named ', 1)[1].strip().strip('"\'')
    print(f'Missing module {module_name}. Please download at')
    print(f'https://github.com/Daniel-Chin/Python_Lib/blob/master/{module_name}.py')
    input('Press Enter to quit...')
    raise e

print('Preparing...')
PAGE_LEN = 512
N_HARMONICS = 60
DO_SWIPE = False
DO_PROFILE = False
AUTOTUNE = True
QUAN = 1
DO_ECHO = True
ECHO_DELAY = .25
ECHO_DECAY = .3
WRITE_FILE = None
# WRITE_FILE = f'demo_{random.randint(0, 99999)}.wav'
CROSS_FADE = 0.04

MASTER_VOLUME = 1
SR = 22050
DTYPE = (np.int32, pyaudio.paInt32)
FILTER = 'kaiser_best'
TWO_PI = np.pi * 2
HANN = scipy.signal.get_window('hann', PAGE_LEN, True)
PAGE_TIME = 1 / SR * PAGE_LEN
IMAGINARY_LADDER = np.linspace(0, TWO_PI * 1j, PAGE_LEN)
CROSS_FADE_TAILS = round(PAGE_LEN * (1 - CROSS_FADE) / 2)
CROSS_FADE_OVERLAP = PAGE_LEN - 2 * CROSS_FADE_TAILS
assert CROSS_FADE_OVERLAP + 2 * CROSS_FADE_TAILS == PAGE_LEN
# Linear cross fade
FADE_IN_WINDOW = np.array([
    x / CROSS_FADE_OVERLAP for x in range(CROSS_FADE_OVERLAP)
], DTYPE[0])
FADE_OUT_WINDOW = np.flip(FADE_IN_WINDOW)

streamOutContainer = []
terminate_flag = 0
terminateLock = Lock()
profiler = StreamProfiler(PAGE_LEN / SR, DO_PROFILE)
echo = [np.zeros(PAGE_LEN, DTYPE[0]) for _ in range(
    round(ECHO_DELAY * SR / PAGE_LEN)
)]

if DO_PROFILE:
    _print = print
    def print(*a, **k):
        _print()
        _print(*a, **k)

def main():
    global terminate_flag, f, synth
    print('Press ESC to quit. ')
    terminateLock.acquire()
    synth = HarmonicSynth(N_HARMONICS, SR, PAGE_LEN, DTYPE[0], True, DO_SWIPE, .3)
    pa = pyaudio.PyAudio()
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
    if WRITE_FILE is not None:
        f = wave.open(WRITE_FILE, 'wb')
        f.setnchannels(1)
        f.setsampwidth(4)
        f.setframerate(SR)
    streamIn.start_stream()
    print('go!')
    try:
        while streamIn.is_active():
            op = listen(b'\x1b', priorize_esc_or_arrow=True)
            if op == b'\x1b':
                print('Esc received. Shutting down. ')
                break
    except KeyboardInterrupt:
        print('Ctrl+C received. Shutting down. ')
    finally:
        print('Releasing resources... ')
        terminate_flag = 1
        terminateLock.acquire()
        terminateLock.release()
        streamOutContainer[0].stop_stream()
        streamOutContainer[0].close()
        if WRITE_FILE is not None:
            f.close()
        while streamIn.is_active():
            sleep(.1)   # not perfect
        streamIn.stop_stream()
        streamIn.close()
        pa.terminate()
        print('Resources released. ')

def sft(signal, freq_bin):
    # Slow Fourier Transform
    return np.abs(np.sum(signal * np.exp(IMAGINARY_LADDER * freq_bin))) / PAGE_LEN

def onAudioIn(in_data, sample_count, *_):
    global terminate_flag

    try:
        if terminate_flag == 1:
            terminate_flag = 2
            terminateLock.release()
            print('PA handler terminating. ')
            # Sadly, there is no way to notify main thread after returning. 
            return (None, pyaudio.paComplete)

        if sample_count > PAGE_LEN:
            print('Discarding audio page!')
            in_data = in_data[-PAGE_LEN:]

        profiler.gonna('typing')
        page = np.frombuffer(
            in_data, dtype = DTYPE[0]
        )

        profiler.gonna('yin')
        f0 = yin(page * HANN, SR, PAGE_LEN)
        f0_ = autotune(f0, 0)[0]

        profiler.gonna('sft')
        harmonics = []
        for i in range(1, N_HARMONICS + 1):
            freq = f0 * i
            harmonics.append(Harmonic(
                f0_ * i, 
                sft(page * HANN, freq * PAGE_LEN / SR)
            ))
        
        profiler.gonna('eat')
        synth.eat(harmonics)

        profiler.gonna('mix')
        mixed = synth.mix()

        if DO_ECHO:
            profiler.gonna('echo')
            mixed += echo.pop(0)
            # echo.append(np.rint(mixed * ECHO_DECAY).astype(DTYPE[0]))
            echo.append(pitchBend(np.rint(mixed * ECHO_DECAY).astype(DTYPE[0]), 2))
        
        streamOutContainer[0].write(mixed, PAGE_LEN)
        if WRITE_FILE is not None:
            f.writeframes(mixed)

        profiler.display(same_line=True)
        profiler.gonna('idle')
        return (None, pyaudio.paContinue)
    except:
        terminateLock.release()
        import traceback
        traceback.print_exc()
        return (None, pyaudio.paAbort)

def autotune(freq, mag):
    if not AUTOTUNE:
        return freq, mag
    pitch = np.log(freq) * 17.312340490667562 - 36.37631656229591
    return np.exp((round(pitch / QUAN) * QUAN + 36.37631656229591) * 0.05776226504666211), mag

def guess(devices, targets):
    for t in targets:
        for i, name in devices:
            if t in name:
                return i
    return ''

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

main()
