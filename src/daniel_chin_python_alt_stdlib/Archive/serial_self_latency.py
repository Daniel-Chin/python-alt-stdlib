'''
Measures the serial self-playback round trip time.  
'''

import os
from time import perf_counter

import serial

PORT = 'COM9'

def main():
    with serial.Serial(PORT, 9600 * 4, timeout=1) as s:
        print('\n\nSerial opened:', s.name)
        while True:
            r = os.urandom(1)
            start = perf_counter()
            s.write(r)
            assert s.read(1) == r
            stop = perf_counter()
            print(stop - start)

main()
