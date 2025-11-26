'''
Synthesize sound with harmonics.  
Interpolate between frames smartly.  

commit 490dd5810f39fc322a61cd444c581374323d8803 removed 
accelerated approach to correct mag. So now it only works 
if harmonic list input is stable in sequence. 
'''
import numpy as np

TWO_PI = np.pi * 2
LOG_SMOOTH = .0001

class Harmonic:
    __slot__ = ['freq', 'mag']

    def __init__(self, freq, mag):
        self.freq = freq
        self.mag = mag
    
    def getMag(self):
        return self.mag
    
    def getFreq(self):
        return self.freq
    
    def __repr__(self):
        return f'Harmonic({self.freq}, {self.mag})'
    
    def __iter__(self):
        return iter((self.freq, self.mag))

class HarmonicSynth:
    def __init__(
        self, n_harmonics, SR, PAGE_LEN, DTYPE, 
        STUPID_MATCH, DO_SWIPE, CROSSFADE_RATIO = None, 
    ):
        self.PAGE_LEN = PAGE_LEN
        self.STUPID_MATCH = STUPID_MATCH
        self.DO_SWIPE = DO_SWIPE
        self.SR = SR
        self.n_harmonics = n_harmonics
        if CROSSFADE_RATIO is not None:
            print()
            print('harmonicSynth Warning! CROSSFADE_RATIO is deprecated.')
            print()

        self.signal_2d = np.zeros((n_harmonics, PAGE_LEN), DTYPE)
        self.harmonics = [
            Harmonic(261.63, 0) for i in range(n_harmonics)
        ]
        self.osc = [Osc(
            i, self, h
        ) for i, h in enumerate(self.harmonics)]
    
    def mix(self):
        return np.sum(self.signal_2d, 0) * 4
        # I don't really know why *2 is needed here
        # Another *2 for the hann window
    
    def eat(self, harmonics):
        assert len(harmonics) >= self.n_harmonics
        # print(*[
        #     format(x, '4.0f') for x, _ in harmonics
        # ])
        if self.STUPID_MATCH:
            [osc.eat(*h, self.DO_SWIPE) for osc, h in zip(self.osc, harmonics)]
        else:
            harmonics.sort(key=Harmonic.getMag)
            unmatched_log_f = [
                np.log(freq)
                for freq, _ in harmonics
            ]
            unmatched = harmonics[:]
            harmonics = []
            # for i, ((freq, _), osc) in enumerate(zip(self.harmonics, self.osc)):
            for (freq, _), osc in zip(self.harmonics, self.osc):
                log_freq = np.log(freq)
                i_max = np.argmax(- np.abs(np.array(unmatched_log_f) - log_freq))
                loss = abs(log_freq - unmatched_log_f.pop(i_max))
                swipe_this = loss < .006
                # swipe_this = True
                # swipe_this = i_max < 3
                # print(format(loss, '6.3f'), end = '')
                harmonics.append(unmatched.pop(i_max))
                osc.eat(
                    *harmonics[-1], 
                    swipe = self.DO_SWIPE and swipe_this, 
                )
            # print()
        self.harmonics = harmonics

class Osc():
    def __init__(self, i, synth, harmonic):
        self.LINEAR = np.arange(synth.PAGE_LEN + 1) * TWO_PI / synth.SR
        self.freq = harmonic.freq
        self.mag = harmonic.mag
        self.phase = 0
        self.i = i
        self.synth = synth
    
    def eat(self, new_freq, new_mag, swipe = True):
        if swipe:
            # print('swipe', end='')
            tau = self.LINEAR * np.linspace(
                self.freq, (new_freq + self.freq) * .5, self.synth.PAGE_LEN + 1
            )
            mask = np.exp(np.linspace(np.log(self.mag + LOG_SMOOTH), np.log(new_mag + LOG_SMOOTH), self.synth.PAGE_LEN)) - LOG_SMOOTH
        else:
            tau = self.LINEAR * new_freq
            mask = np.exp(np.linspace(np.log(self.mag + LOG_SMOOTH), np.log(new_mag + LOG_SMOOTH), self.synth.PAGE_LEN)) - LOG_SMOOTH
        self.synth.signal_2d[self.i] = np.sin(
            tau[:-1] + self.phase
        ) * mask
        self.freq = new_freq
        self.mag = new_mag
        self.phase = (tau[-1] + self.phase) % TWO_PI

def test():
    import pyaudio
    import time
    SR = 22050
    PAGE_LEN = 1024
    hSynth = HarmonicSynth(
        6, SR, PAGE_LEN, np.float32, True, False, 
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format = pyaudio.paFloat32, channels = 1, rate = SR, 
        output = True, frames_per_buffer = PAGE_LEN,
    )
    while True:
        h = [
            Harmonic(220 * 1, .05), 
            Harmonic(220 * 2, .03), 
            Harmonic(220 * 3, .04), 
            Harmonic(220 * 4, .005), 
            Harmonic(220 * 5, .007), 
            Harmonic(220 * 6, .01), 
        ]
        hSynth.eat(h)
        mixed = hSynth.mix()
        stream.write(mixed, PAGE_LEN)
        # time.sleep(PAGE_LEN / SR * .9)

if __name__ == '__main__':
    test()
