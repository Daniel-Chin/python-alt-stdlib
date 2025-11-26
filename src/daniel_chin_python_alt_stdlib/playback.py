'''
Playback audio in real-time.  
Useful if you want to hear your doorbell while watching videos 
with headphones.  
'''

from time import time, sleep
from threading import Lock

import numpy as np
import pyaudio
import keyboard as kb

from .interactive import listen
from .select_audio_device import select_audio_device_input, select_audio_device_output

MASTER_VOLUME = .2

PAGE_LEN = 1024
# SR = 22050
SR = 48000
DTYPE_BUF = np.float32
DTYPE_IO = (np.int32, pyaudio.paInt32)

streamOutContainer = []
terminate_flag = 0
terminateLock = Lock()

def main():
    global terminate_flag
    terminateLock.acquire()
    pa = pyaudio.PyAudio()
    in_i  = select_audio_device_input(pa)
    out_i = select_audio_device_output(pa)
    # in_i, out_i = None, None
    streamOutContainer.append(pa.open(
        format = DTYPE_IO[1], channels = 1, rate = SR, 
        output = True, frames_per_buffer = PAGE_LEN,
        output_device_index = out_i, 
    ))
    streamIn = pa.open(
        format = DTYPE_IO[1], channels = 1, rate = SR, 
        input = True, frames_per_buffer = PAGE_LEN,
        input_device_index = in_i, 
        stream_callback = onAudioIn, 
    )
    streamIn.start_stream()
    print('Press ESC to quit. ')
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
        while streamIn.is_active():
            sleep(.1)   # not perfect
        streamIn.stop_stream()
        streamIn.close()
        pa.terminate()
        print('Resources released. ')

def onAudioIn(in_data, sample_count, *_):
    try:
        if terminate_flag == 1:
            terminateLock.release()
            print('PA handler terminating. ')
            # Sadly, there is no way to notify main thread after returning. 
            return (None, pyaudio.paComplete)

        if sample_count > PAGE_LEN:
            print('Discarding audio page!')
            in_data = in_data[-PAGE_LEN:]

        # page = np.frombuffer(
        #     in_data, dtype = DTYPE_IO[0]
        # )
        streamOutContainer[0].write(in_data, PAGE_LEN)

        return (None, pyaudio.paContinue)
    except:
        terminateLock.release()
        import traceback
        traceback.print_exc()
        return (None, pyaudio.paAbort)

if __name__ == '__main__':
    main()
