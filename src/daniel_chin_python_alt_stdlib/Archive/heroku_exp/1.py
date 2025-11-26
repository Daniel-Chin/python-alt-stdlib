from socket import socket

ip = '52.20.199.44'
m = '''GET / HTTP/1.1
Host: world-of-blogs.herokuapp.com\n\n'''.replace('\n', '\r\n').encode()

s = socket()
s.connect((ip, 80))
s.send(m)
print(s.recv(9999))
input('Enter...')
