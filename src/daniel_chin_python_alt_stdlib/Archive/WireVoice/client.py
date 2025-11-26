import sys
import socket
import pyaudio
from time import sleep
Daniel_IP = ('10.209.23.186', '10.209.0.218')

def main():
    s = connect()
    wire(s)

def connect():
    print('Connecting to server... ')
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect((Daniel_IP[0],2333))
    except:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((Daniel_IP[1],2333))
        except:
            print('Ah oh. Daniel is not online. ')
            input('Enter to quit...')
            sys.exit(1)
    s.settimeout(5)
    return s

def wire(s):
    WIDTH = 2
    CHANNELS = 2
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=44100,
                    input=True,
                    output=True,
                    frames_per_buffer=1024)
    
    print('Channel is open! ')
    for _ in range(10):
        for i in range(43):
            data = b''
            while len(data) < 4096:
                data += s.recv(4096-len(data))
            stream.write(data, 1024)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()

main()
