'''
Transpose an audio up one octave, by removing odd partials.  
'''
from os import path
import numpy as np
import librosa
import soundfile as sf
from yin import yin
from myfile import sysArgvOrInput
from jdt import Jdt

# PAGE_LEN = 512
PAGE_LEN = 2048

def main():
    in_file = sysArgvOrInput()
    print('Reading file...')
    audio, sr = librosa.load(in_file)
    buffer = []
    i = 0
    smoother = Smoother()
    with Jdt(len(audio), UPP=16) as j:
        while True:
            j.update(i)
            page = audio[i : i + PAGE_LEN]
            i += PAGE_LEN
            if len(page) < PAGE_LEN:
                break
            buffer.append(shift(page, sr, smoother))
    out_file = path.splitext(in_file)[0] + '_+8.wav'
    print('writing file...')
    sf.write(out_file, np.concatenate(buffer), sr)

class Smoother:
    MAX = 1
    MID = (MAX - 1) // 2

    def __init__(self) -> None:
        self.history = []
    def eat(self, f0):
        history = self.history
        history.append(f0)
        if len(history) > self.MAX:
            history.pop(0)
            return sorted(history)[self.MID]
        else:
            return f0

def shift(page: np.array, sr, smoother: Smoother):
    nyquist = sr / 2
    f0 = smoother.eat(yin(page, sr, PAGE_LEN))
    spectrum = np.fft.rfft(page)
    for bin_i in range(PAGE_LEN // 2 + 1):
        bin_freq = bin_i / (PAGE_LEN // 2) * nyquist
        distance = (.5 - abs(
            ((bin_freq + f0) / (2 * f0)) % 1 - .5
        )) * 2
        if distance < max(.15, (170 - f0) / 50 * .2 + .15):
            spectrum[bin_i] = 0
    return np.fft.irfft(spectrum)

main()
