'''
HTTP man in middle. Prints all traffic. Useful for investigating how http works. Although Chrome Dev Tools prolly have something like this already.  
'''
target="www.banana.com"

import socket
S = socket.socket()
S.bind(("127.0.0.1", 80))
S.listen(1)
(c, address) = S.accept()
c.settimeout(.5)
s = socket.socket()
s.settimeout(5)
s.connect((target, 80))
print("Both parties ready. ")
print("It's started. ")
fake = 'GET / HTTP/1.1\r\nHost: ' + target + '\r\n'
print(fake)
fake=fake.encode()
chunk = b''
try:
    while not (len(chunk)>=5 and chunk[-1]=='\n' and chunk[-3]=='\n'):
        chunk+=c.recv(4096)
except:
    print(chunk)
chunk = chunk[chunk.index(b'\n'):]
chunk = chunk[chunk.index(b'\n'):]
print(chunk.decode())
s.send(fake)
s.send(chunk)
r=b' '
chunk=b''
while r!=b'':
    r=s.recv(4096)
    chunk+=r
print()
print(chunk.decode())
c.send(chunk)
s.close()
c.close()
input('end')
