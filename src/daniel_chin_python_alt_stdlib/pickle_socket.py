'''
A socket that supports object transmission. 
'''
from socket import socket
import pickle
from io import BytesIO
import sys
__all__ = ['PickleSocket', 'RemoteClosedDuringPickle']

PAGE = 4096

class PickleSocket():
    def __init__(self, upon_this_socket=None):
        if upon_this_socket is None:
            self.socket=socket()
        else:
            self.socket=upon_this_socket
        for name in dir(self.socket):
            if name[:2] != '__' and name not in dir(__class__):
                self.__setattr__(name, self.socket.__getattribute__(name))
    
    def shakeHands(self,banner='This is a pickleSocket by Daniel Chin. ',verbose=True):
        self.sendObj(banner)
        recved=self.recvObj()
        if recved==banner:
            if verbose:
                print('Shake hands success.')
        else:
            print('Error: Shake hands failure! ')
            print('Banner:',banner)
            print('Received:',recved)
            input('Enter to exit...')
            sys.exit(1)
    
    def sendObj(self,obj):
        io_obj=BytesIO()
        pickle.dump(obj,io_obj)
        size=io_obj.tell()
        io_obj.seek(0)
        try:
            sent=self.socket.sendfile(io_obj)
            while sent<size:
                sent+=self.socket.sendfile(io_obj)
        except AttributeError:
            to_read = size
            while to_read > 0:
                read = io_obj.read(PAGE)
                to_read -= len(read)
                self.socket.sendall(read)
    
    def recvObj(self):
        return pickle.load(IoSocket(self.socket))
    
    def accept(self):
        s, addr = self.socket.accept()
        return __class__(s), addr

class IoSocket:
    def __init__(self,socket):
        self.socket=socket
    
    def read(self,count=1):
        read=self.socket.recv(count)
        if read==b'':
            raise RemoteClosedDuringPickle 
        return read
    
    def readline(self):
        read=b''
        buffer=b''
        while read !=b'\n':
            read=self.read(1)
            buffer+=read
        return buffer
    
    def readinto(self, b):
        b[0] = self.read()
        return 1

class RemoteClosedDuringPickle(BaseException):
    pass

if __name__ == '__main__':
    from console import console
    console(globals())
