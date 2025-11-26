'''
Uses HarmonicSynth (precise) for the lower register 
and IfftSynth (fast) for the higher register.  
'''

import numpy as np
from harmonicSynth import HarmonicSynth, Harmonic
from ifftSynth import IfftSynth

BLANK = Harmonic(220, 0)

class HybridSynth:
    '''
    `max_out_of_tune`: smaller gives better precision but 
    slower to synth. (It decides the register cutoff.)  
    '''
    def __init__(
        self, n_harmonics, SR, PAGE_LEN, DTYPE, 
    ):
        self.n_harmonics = n_harmonics
        self.SR = SR
        self.PAGE_LEN = PAGE_LEN
        self.DTYPE = DTYPE
        self.bin_freq = SR / PAGE_LEN
        self.hSynth = HarmonicSynth(
            n_harmonics, SR, PAGE_LEN, DTYPE, 
            STUPID_MATCH=True, DO_SWIPE=False, 
        )
        self.iSynth = IfftSynth(SR, PAGE_LEN)
        self.ifft_signal = None
    
    def errorRange(self, freq):
        return np.log(
            (freq + self.bin_freq) / freq
        ) / 2 * 17.312340490667562
    
    def eat(self, harmonics, base_spectrum=None, verbose=True, skipSort=False):
        if not skipSort:
            harmonics.sort(key=Harmonic.getFreq)
        low_harmonics = harmonics[:self.n_harmonics]
        high_harmonics = harmonics[self.n_harmonics:]
        if verbose and high_harmonics:
            print(
                'ifft error', 
                self.errorRange(high_harmonics[0].freq), 
                'semitones. '
            )
        n_blank_harmonics = self.n_harmonics - len(low_harmonics)
        for _ in range(n_blank_harmonics):
            low_harmonics.append(BLANK)
        self.hSynth.eat(low_harmonics)
        self.ifft_signal = self.iSynth.eat(
            high_harmonics, base_spectrum, 
        ).astype(self.DTYPE)
    
    def mix(self):
        return self.hSynth.mix() + self.ifft_signal
        # return self.ifft_signal
        # return self.hSynth.mix()

def test():
    import pyaudio
    SR = 22050
    PAGE_LEN = 1024
    HYBRID_QUALITY = 12
    hySynth = HybridSynth(HYBRID_QUALITY, SR, PAGE_LEN, np.float32)
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format = pyaudio.paFloat32, channels = 1, rate = SR, 
        output = True, frames_per_buffer = PAGE_LEN,
    )
    def pitch2freq(pitch):
        return np.exp((pitch + 36.37631656229591) * 0.0577622650466621)
    h = []
    # for p in [48, 53, 57]:
    for p in [53, 48, 57]:
        f0 = pitch2freq(p)
        h.append(Harmonic(f0 * 1, .05))
        h.append(Harmonic(f0 * 2, .03))
        h.append(Harmonic(f0 * 3, .04))
        h.append(Harmonic(f0 * 4, .005))
        h.append(Harmonic(f0 * 5, .007))
        h.append(Harmonic(f0 * 6, .01))
        h.append(Harmonic(f0 * 7, .01))
        h.append(Harmonic(f0 * 8, .005))
        h.append(Harmonic(f0 * 9, .002))
    while True:
        hySynth.eat(h)
        mixed = hySynth.mix()
        stream.write(mixed * .2, PAGE_LEN)

if __name__ == '__main__':
    test()
