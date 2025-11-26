from pickle_socket import PickleSocket
import sys

def main():
    s = PickleSocket()
    s.connect(('localhost', 2333))
    s.shakeHands()
    for i in range(256 ** 2):
        is_up, ip = s.recvObj()
        if is_up:
            print('Host up:', ip, ' ' * 10)
        else:
            print('down:', ip, '    ', end = '\r')
    input('Done. enter...')

main()
sys.exit(0)
