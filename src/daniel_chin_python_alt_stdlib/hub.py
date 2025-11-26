'''
Hub: forward all socket messages. 
Connect, sendall(b'OK'), forward...
'''
# fake: CHUNK = 1024
import socket
from threading import Thread, Condition, Lock
from queue import Queue, Empty
from interactive import listen

def hub(port = 2333, size = 2):
    s = socket.socket()
    s.bind(('', port))
    s.listen(size)
    queue = Queue()
    list_recver = []
    print('Listening... ')
    for i in range(size):
        client, addr = s.accept()
        print(i+1, '/', size, ': ', addr, sep='')
        list_recver.append(Recver(client, queue))
    print('Go! ')
    queue.put(b'OK')
    for recver in list_recver:
        recver.start()
    sender = Sender(list_recver, queue)
    print('Enter to end...')
    while listen([b'\r'],.5) is None:
        pass
    with sender.condition:
        sender.do_stop = True
        while not sender.has_stopped:
            sender.condition.wait()
    del sender
    for recver in list_recver:
        with recver.condition:
            recver.do_stop = True
            while not recver.has_stopped:
                recver.condition.wait()
        del recver
    input('Ended. Enter... ')

class Sender(Thread):
    def __init__(self, list_recver, queue):
        Thread.__init__(self)
        self.list_recver = list_recver
        self.queue = queue
        self.condition = Condition()
        self.do_stop = False
        self.has_stopped = False
        self.start()
    
    def goOn(self):
        with self.condition:
            return not self.do_stop
    
    def run(self):
        while self.goOn():
            try:
                data = self.queue.get(timeout = .2)
                for i, recver in enumerate(self.list_recver.copy()):
                    with recver.condition:
                        if recver.has_stopped:
                            del self.list_recver[i]
                            print('No.', i, 'closed. ')
                            print(len(self.list_recver), 'remaining. ')
                            continue
                    recver.client.sendall(data)
            except Empty:
                for i, recver in enumerate(self.list_recver.copy()):
                    with recver.condition:
                        if recver.has_stopped:
                            print(self.list_recver, i)
                            del self.list_recver[i]
                            print('No.', i, 'closed. ')
                            print(len(self.list_recver), 'remaining. ')
        with self.condition:
            self.has_stopped = True
            self.condition.notify()

class Recver(Thread):
    def __init__(self, client, queue):
        Thread.__init__(self)
        self.client = client
        self.queue = queue
        self.condition = Condition()
        self.do_stop = False
        self.has_stopped = False
    
    def goOn(self):
        with self.condition:
            return not self.do_stop
    
    def run(self):
        while self.goOn():
            try:
                data = self.client.recv(1024)
            except:
                data = b''
            if data == b'':
                with self.condition:
                    self.do_stop = True 
            else:
                self.queue.put(data)
        with self.condition:
            self.has_stopped = True
            self.client.close()
            self.condition.notify()

if __name__ == '__main__':
    hub()
