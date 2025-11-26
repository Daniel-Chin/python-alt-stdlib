'''
Playback audio in real-time.  
Useful if you want to hear your doorbell while watching videos 
with headphones.  
'''

from queue import Queue, Empty

import numpy as np
import pyaudio

from .interactive import listen
from .select_audio_device import select_audio_device_input, select_audio_device_output

DELAY = 1.0 # sec

PAGE_LEN = 1024
SR = 22050
# SR = 48000
DTYPE_IO = (np.int32, pyaudio.paInt32)

BLANK_PAGE = (np.zeros(PAGE_LEN, dtype=DTYPE_IO[0])).tobytes()

def main():
    queue = Queue[bytes]()
    for _ in range(int(DELAY * SR / PAGE_LEN) + 1):
        queue.put(BLANK_PAGE)
    pa = pyaudio.PyAudio()
    in_i  = select_audio_device_input(pa)
    out_i = select_audio_device_output(pa)
    # in_i, out_i = None, None

    def on_audio_out(in_data, frame_count, time_info, status):
        assert frame_count == PAGE_LEN, f'Expected {PAGE_LEN=}, got {frame_count=}'
        try:
            data = queue.get_nowait()
        except Empty:
            data = BLANK_PAGE
        return (data, pyaudio.paContinue)
    
    def on_audio_in(in_data, frame_count, time_info, status):
        assert frame_count == PAGE_LEN, f'Expected {PAGE_LEN=}, got {frame_count=}'
        queue.put(in_data)
        return (None, pyaudio.paContinue)

    stream_out = pa.open(
        format = DTYPE_IO[1], channels = 1, rate = SR, 
        output = True, frames_per_buffer = PAGE_LEN,
        output_device_index = out_i, 
        stream_callback = on_audio_out,
    )
    stream_in = pa.open(
        format = DTYPE_IO[1], channels = 1, rate = SR, 
        input = True, frames_per_buffer = PAGE_LEN,
        input_device_index = in_i, 
        stream_callback = on_audio_in, 
    )
    stream_out.start_stream()
    stream_in .start_stream()

    print('Press ESC to quit. ')
    try:
        while True:
            op = listen(b'\x1b', priorize_esc_or_arrow=True)
            if op == b'\x1b':
                print('Esc received. Shutting down. ')
                break
    except KeyboardInterrupt:
        print('Ctrl+C received. Shutting down. ')
    finally:
        print('Releasing resources... ')
        stream_in.stop_stream()
        stream_in.close()
        stream_out.stop_stream()
        stream_out.close()
        pa.terminate()
        print('Resources released. ')

if __name__ == '__main__':
    main()
