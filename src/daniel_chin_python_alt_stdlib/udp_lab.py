'''
Interactive shell to test UDP.  
'''

print('loading...')

import socket
from threading import Thread

from console import console

# IP = 'localhost'
IP = '192.168.0.178'
PORT = 2352

def udpSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = udpSocket()
client = udpSocket()

server.bind((IP, PORT))

class MyThread(Thread):
    def run(self):
        while True:
            print('\n', server.recvfrom(1024))

def quickSend(msg):
    client.sendto(msg, (IP, PORT))

MyThread().start()

print(dir())
console(globals())

print('Bye! Except you need to close this window manually, because I\'m too lazy to clean up properly.')
