from . import PORT
from socket import socket, timeout
from os import system

PAGE = 4096

def main():
    sock = socket()
    sock.connect(('localhost', PORT))
    sock.settimeout(1)
    buffer = b''
    while b'\n' not in buffer:
        try:
            buffer += sock.recv(8)
        except timeout:
            pass
    sock.close()
    port = int(buffer.decode().strip())
    sock = socket()
    sock.connect(('localhost', port))
    buffer = b''
    while b'\n' not in buffer:
        try:
            buffer += sock.recv(1)
        except timeout:
            pass
    title = buffer.decode().strip()
    system(f'title {title}')
    while True:
        try:
            recved = sock.recv(PAGE)
            if recved == b'':
                break
            print(recved.decode(), end = '', flush = True)
        except timeout:
            pass
        except ConnectionResetError:
            break
    print('--- End of Transmission ---')

main()
