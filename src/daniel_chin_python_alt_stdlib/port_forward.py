'''
Provides fake p2p, port forwarding. 

Ignored the thread-danger of sockets. 
Expect unexpected behaviors. 
'''
__all__ = ['Forwarder', 'fakeP2P', 'portForward', 'bothForward']
import socket
from threading import Thread
from interactive import listen
from time import sleep
import os
import signal

CHUNK = 4096

class Forwarder(Thread):
    SPF = 0.1
    id = 0
    
    def __init__(self, fro, to, description = ''):
        Thread.__init__(self)
        self.to = to
        self.fro = fro
        if description == '':
            self.description = str(__class__.id)
            __class__.id += 1
        else:
            self.description = description
    
    def run(self):
        while True:
            try:
                data = self.fro.recv(CHUNK)
            except:
                data = b''
            if data == b'':
                self.to.close()
                self.fro.close()
                break
            else:
                try:
                    self.to.sendall(data)
                except:
                    break
        print('Forwarder', str(self), 'has stopped. ')
    
    def __str__(self):
        return '<Forwarder %s>' % str(self.description)

def bothForward(socket_1, socket_2, addr):
    forwarder_1 = Forwarder(socket_1, socket_2, addr)
    forwarder_2 = Forwarder(socket_2, socket_1)
    forwarder_1.start()
    forwarder_2.start()
    return (forwarder_1, forwarder_2)

def fakeP2P(port = 2333):
    s = socket.socket()
    s.bind(('', port))
    s.listen(2)
    print('Listening... ')
    p_1, addr = s.accept()
    print(addr)
    p_2, addr = s.accept()
    print(addr)
    forwarders = bothForward(p_1, p_2)
    print('Go! ')
    print('Enter to end...')
    [x.join() for x in forwarders]
    input('Ended. Enter... ')

def portForward(inside_port, inbound_port, afraid = False):
    '''
    Set `afraid` to True to manually accept connections. 
    '''
    outServerSocket = socket.socket()
    outServerSocket.bind(('', inbound_port))
    outServerSocket.listen(afraid and 1 or 10)
    allForwarders = []
    allSockets = []
    try:
        while True:
            print('listening at port %d...' % inbound_port)
            outSocket, addr = outServerSocket.accept()
            print('Inbound connection from', addr)
            if afraid == True:
                print('Accept? y/n')
                if listen(['y', 'n']) != b'y':
                    outSocket.close()
                    print('Refused. ')
                    continue
            inSocket = socket.socket()
            allSockets.append(outSocket)
            allSockets.append(inSocket)
            print('Connecting inside port', inside_port)
            inSocket.connect(('localhost', inside_port))
            allForwarders += bothForward(outSocket, inSocket, addr)
            print('-= ESTABLISHED =-')
            print()
    except KeyboardInterrupt:
        print('Ctrl+C received. ')
    finally:
        print('Closing all sockets...')
        [x.close() for x in allSockets]
        outServerSocket.close()
        print('Joining...')
        panic = Panic()
        panic.start()
        for forwarder in allForwarders:
            forwarder.join()
        print('All have joined. ')
        panic.all_is_fine = True

class Panic(Thread):
    def __init__(self):
        super(__class__, self).__init__()
        self.all_is_fine = False
    
    def run(self):
        print('Panic starts. ')
        sleep(0.3)
        if self.all_is_fine:
            print('Panic sooths. ')
        else:
            print('Panic!!! SIG KILL')
            os.kill(os.getpid(), signal.SIGKILL)

if __name__ == '__main__':
    print(__all__)
    from console import console
    console(globals())
