import sys
import socket
import pyaudio
Daniel_IP = ('10.209.0.218', '10.209.23.186')

def main():
    s = connect()
    wire(s)

def connect():
    s = socket.socket()
    s.bind(('',2333))
    s.listen(1)
    c, addr = s.accept()
    c.settimeout(5)
    return c

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
            data = stream.read(1024)
            s.sendall(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()

main()
