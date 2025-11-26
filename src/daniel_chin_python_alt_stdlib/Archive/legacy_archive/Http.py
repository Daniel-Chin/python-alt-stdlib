import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 80))
s.listen(1)
(c, address) = s.accept()
r='a'
while r!='':
    r=c.recv(1).decode()
    print(r,end='')
'''
r=input('')
while r!='':
    print("#"*c.send(r.encode()))
    r=input('')
c.shutdown
c.close
s.close
'''
input('end')
