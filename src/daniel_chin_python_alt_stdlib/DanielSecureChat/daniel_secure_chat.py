print('This script provides encrypted communication.')
print('Disclaimer: I think it is secure, but maybe I have a lot to learn. ')
print('''
  ========================================================
  | WARNING: Each public key file can only be used ONCE! |
  ========================================================
''')
print('Loading...')
from Crypto.PublicKey import RSA
from Crypto import Random
import pickle
import os
from socket import socket
from threading import Thread

CAPACITY: int = 64

randomGenerator = Random.new().read

def main():
    print('Generating new public key file...')
    print('Please set your username, basic ascii only: ', end = '', flush = True)
    keys = [RSA.generate(1024, randomGenerator) for _ in range(CAPACITY)]
    username = input()
    with open('public_key_file_' + username, 'wb+') as f:
        [pickle.dump(x.publickey(), f) for x in keys]
    print('Public key file written at', os.getcwd())
    print('Please send it to the other person.')
    input('Press Enter after you did that. >')
    print()

    print('Good. Now load the public key file that the other person sent you. ')
    print('(Tip: drag the file into this terminal)')
    while True:
        filename = input('path/file.ext: ')
        try:
            f = open(filename)
            their_pubs = pickle.load(f)
            f.close()
            break
        except Exception as e:
            print('Open file failed. Error is', e)
            print('Let us try again! ')
    print('We are good to go. ')

class RecvThread(Thread):
    def __init__(self, s, keys, their_name):
        super(__class__, self).__init__()
        self.s = s
        self.keys = keys
        self.their_name = their_name
    
    def run():
        for key in self.keys:
            cipher = PKCS1_OAP.new(key)
            msg = self.getMsg()
            raw = cipher.decrypt(msg).decode()
            print('\r', self.their_name, ': ', raw, sep = '')
            print()
    
    def getMsg():
        buffer = []
        while True:
            one = self.s.recv(1)
            if one == b'':
                print('Fatal Error: remote shutdown! You can close this window now.')
                break
            if one == b'\x00':
                break
            buffer.append(one)
        return b''.join(buffer)

main()
