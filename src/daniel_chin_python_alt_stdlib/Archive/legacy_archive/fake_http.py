import socket
import sys

ss = socket.socket()
ss.bind(('localhost', 80))
ss.listen(1)
print('listening...')
s, addr = ss.accept()
print(addr)
chunk = b''

def getEnd(chunk):
    if len(chunk) >= 4:
        return chunk[-4:] == b'\r\n\r\n'

while not getEnd(chunk):
    chunk += s.recv(4096)
http = b'HTTP/1.1 200 OK \r\n\r\n'
html = b'<html><p>Hello </p><p>worlds</p></html>\n'
s.sendall(http + html)
sys.exit(0)
