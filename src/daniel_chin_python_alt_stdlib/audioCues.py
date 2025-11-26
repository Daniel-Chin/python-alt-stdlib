'''
Play audio cues. 
'''

from functools import lru_cache
import numpy as np
import pyaudio as pa

PAGE_LEN = 1024
SR = 44100

SILENCE = object()
SIN = object()
LADOLADO = object()

class AudioCues:
    def __init__(self) -> None:
        p = pa.PyAudio()
        self.p = p
        self.stream = p.open(
            format = pa.paFloat32, 
            channels = 1, 
            rate = SR, 
            output = True, 
            stream_callback = self.callback, 
        )
        self.stream.start_stream()
        self.mode = SILENCE
        self.phase = 0
        self.freq = 440
        self.amp = 1
        self.meta_mode = None
        self.lado_phase = 0
        self.lado_period = 1
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
    def callback(
        self, in_data, frame_count, time_info, status, 
    ):
        self.loop()
        if self.mode is SILENCE:
            return (self.getZeros(frame_count), pa.paContinue)
        elif self.mode is SIN:
            x = self.phase + np.arange(
                frame_count + 1, dtype=np.float32, 
            ) / SR * self.freq
            self.phase = x[-1] % 1
            return (
                self.amp * np.sin(x * 2 * np.pi), 
                pa.paContinue, 
            )
    
    @lru_cache(4)
    def getZeros(self, frame_count):
        return np.zeros((frame_count, ))
    
    def startSin(self, freq = 440, amp = 1):
        self.freq = freq
        self.amp = amp
        self.mode = SIN
    
    def mute(self):
        self.mode = SILENCE
        self.meta_mode = None
    
    def startLado(self, period = .4, amp = 1):
        self.meta_mode = LADOLADO
        self.mode = SIN
        self.amp = amp
        self.lado_period = period

    def loop(self):
        if self.meta_mode is LADOLADO:
            period_frames = SR * self.lado_period
            self.lado_phase += PAGE_LEN
            self.lado_phase %= period_frames
            if self.lado_phase < period_frames // 2:
                self.freq = 440
            else:
                self.freq = 554.365

def test():
    from time import sleep

    aC = AudioCues()
    for i in range(5):
        print(i)
        aC.startLado(.4, np.exp(-i))
        sleep(1)
        aC.mute()
        sleep(1)
    aC.close()

if __name__ == '__main__':
    test()
