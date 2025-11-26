'''
Plays an array of audio signal. Blocking.  
'''
import pyaudio
import numpy as np

PAGE_LEN = 4096

def previewAudio(signal, sr):
    signal = np.float32(signal)
    signal /= np.max(np.abs(signal))
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format = pyaudio.paFloat32, channels = 1, rate = sr, 
        output = True, frames_per_buffer = PAGE_LEN,
    )
    i = 0
    while i < signal.size - PAGE_LEN:
        stream.write(signal[i:i+PAGE_LEN], PAGE_LEN)
        i += PAGE_LEN
    last = signal[i:i+PAGE_LEN]
    stream.write(
        np.concatenate([
            last, 
            np.zeros((PAGE_LEN - last.size, ), dtype = np.float32)
        ]), PAGE_LEN, 
    )
    stream.stop_stream()
    stream.close()
    pa.terminate()
