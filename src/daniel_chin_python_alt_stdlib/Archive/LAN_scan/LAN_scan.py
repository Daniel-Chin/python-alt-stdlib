import sys
from os import system as cmd
from time import time
from socket import socket, timeout as SockTimeout
from threading import Lock

from tqdm import tqdm

from forcemap import forceMap
from pickle_socket import PickleSocket
from console import console

PING_NOT_PORT = False
PORT = 22
TIMEOUT = .5
THREADS = 128

def main():
    ss = PickleSocket()
    ss.bind(('localhost', 2333))
    ss.listen(1)
    print('listening...')
    displaySock, addr = ss.accept()
    displaySock.shakeHands()
    with tqdm(total=256**2) as pbar:
        # progress = 0
        lock = Lock()
        def acc():
            # nonlocal progress
            with lock:
                # progress += 1
                pbar.update(1)
        result = forceMap(
            lambda i : ping(displaySock, acc, i), 
            range(256**2), THREADS, 
        )
    hosts = [x for x in result if x is not None]
    cmd('cls')
    print('There are:', len(hosts))
    console(globals())

def ping(displaySock: PickleSocket, acc, i):
    # ip = '10.209'
    ip = '192.168'
    ip += '.' + str(i // 256)
    ip += '.' + str(i % 256)

    if PING_NOT_PORT:
        start = time()
        cmd('ping ' + ip)
        if time() - start < TIMEOUT:
            is_up = True
        else:
            is_up = False
    else:
        s = socket()
        s.settimeout(TIMEOUT)
        try:
            s.connect((ip, PORT))
        except (SockTimeout, ConnectionRefusedError, OSError):
            is_up = False
        else:
            is_up = True
    displaySock.sendObj((is_up, ip))
    acc()
    return ip if is_up else None

main()
sys.exit(0)
