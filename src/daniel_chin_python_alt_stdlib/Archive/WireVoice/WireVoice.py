import sys
from os import system as cmd
import socket
from threading import Thread, Condition
from interactive import listen
Daniel_IP = ('10.209.0.218', '10.209.23.186')

def main():
    if len(sys.argv)==2 and sys.argv[1]=='second':
        try:
            import pyaudio
        except ImportError:
            print('To run this py, you need the package PyAudio. ')
            print('Press Enter to install. ')
            print('Close the window to quit. ')
            input('...')
            cmd('python -m pip install PyAudio')
            try:
                import pyaudio
            except ImportError:        
                print("Somehow, installation isn't successful. ")
                input('Enter to quit...')
                sys.exit(1)
        print('Import PyAudio success. ')
        global PyAudio
        PyAudio = pyaudio.PyAudio
        s = connect()
        wire(s)
    else:
        cmd('python '+__file__+' second')

def connect():
    print('Connecting to server... ')
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect((Daniel_IP[0],2333))
    except:
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((Daniel_IP[1],2333))
        except:
            print('Ah oh. Daniel is not online. ')
            input('Enter to quit...')
            sys.exit(1)
    s.setblocking(True)
    assert s.recv(2) == b'OK'
    s.settimeout(5)
    return s

def wire(s):
    WIDTH = 2
    CHANNELS = 2
    
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=44100,
                    input=True,
                    output=True,
                    frames_per_buffer=1024)
    
    print('Channel is open! ')
    sender = Sender(s, stream)
    recver = Recver(s, sender.condition, stream)
    input('Enter to abort... ')
    
    with sender.condition:
        sender.condition.stop=True
        while not sender.condition.has_stopped:
            sender.condition.wait()
    with recver.condition:
        recver.condition.stop=True
        while not recver.condition.has_stopped:
            recver.condition.wait()
    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()

class Sender(Thread):
    def __init__(self, s, stream):
        Thread.__init__(self)
        self.s=s
        self.condition=Condition()
        self.condition.stop = False
        self.condition.has_stopped = False
        self.stream = stream
        self.start()
    
    def dontStop(self):
        with self.condition:
            return not self.condition.stop
    
    def run(self):
        while self.dontStop():
            for i in range(43):
                data = self.stream.read(1024)
                self.s.sendall(data)
        with self.condition:
            self.condition.has_stopped=True
            self.condition.notify()

class Recver(Thread):
    def __init__(self, s, senderCondition, stream):
        Thread.__init__(self)
        self.s=s
        self.condition=Condition()
        self.condition.stop = False
        self.condition.has_stopped = False
        self.senderCondition = senderCondition
        self.stream = stream
        self.start()
    
    def dontStop(self):
        with self.condition:
            print(self.condition.stop)
            return not self.condition.stop
    
    def run(self):
        while self.dontStop():
            for i in range(43):
                try:
                    data = self.s.recv(4096)
                except:
                    data = b''
                if data == b'':
                    with self.condition:
                        self.condition.stop = True
                    with self.senderCondition:
                        self.senderCondition.stop = True
                    print('The other one terminated connection. ')
                    print('Please hit ENTER now. ')
                else:
                    self.stream.write(data, 1024)
        with self.condition:
            self.condition.has_stopped=True
            self.condition.notify()

main()
