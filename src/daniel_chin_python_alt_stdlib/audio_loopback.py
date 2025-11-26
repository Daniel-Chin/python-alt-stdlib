'''
Can be used as a loudspeaker.  
Wait, doesn't VoiceMeeter already do this?  
DUPLICATE: playback.py  
'''

import pyaudio

SR = 44100
DTYPE = pyaudio.paFloat32
PAGE_LEN = 256

def main():
    pa = pyaudio.PyAudio()
    outStream = pa.open(
        format = DTYPE, channels = 1, rate = SR, 
        frames_per_buffer = PAGE_LEN, 
        output = True, 
    )
    outStream.start_stream()
    inStream = pa.open(
        format = DTYPE, channels = 1, rate = SR, 
        frames_per_buffer = PAGE_LEN, 
        input = True, 
    )
    inStream.start_stream()
    try:
        while True:
            print('.', end='', flush=True)
            try:
                data = inStream.read(PAGE_LEN)
            except KeyboardInterrupt:
                print('bye')
                break
            outStream.write(data)
    finally:
        inStream.close()
        outStream.close()
        pa.terminate()

if __name__ == '__main__':
    main()
