import socket
def strict_recv(socket,size):
    chunk=b''
    while size>0:
        recved=socket.recv(size)
        size-=len(recved)
        chunk+=recved
    return chunk
#
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",2336))
print('Your IP = ',socket.gethostbyname(socket.gethostname()))
s.listen(2)
print('Waiting for connection...')
c=[0,0]
ip=[0,0]
port=[0,0]
for i in range(2):
    (c[i],(ip[i],port[i]))=s.accept()
    print('Connection established from',ip[i],'at port',port[i])
for i in range(2):
    c[i].send(format(len(ip[1-i]),'2').encode())
    c[i].send(ip[1-i].encode())
    print(ip[1-i].encode())
op=[0,0]
for i in range(2):
    op[i]=strict_recv(c[i],4)
print(op)
if op==[b'send',b'send'] or op==[b'recv',b'recv']:
    print('Error: Naughty users. ')
    c[0].close()
    c[1].close()
    s.close()
    input()
    exit()
elif op==[b'send',b'recv']:
    sender=c[0]
    recver=c[1]
elif op==[b'recv',b'send']:
    sender=c[1]
    recver=c[0]
else:    
    print('Error: All hell break loose. ')
    input()
    exit()
recved=sender.recv(1024)
while recved!=b'':
    recver.send(recved)
    recved=sender.recv(1024)
recver.close()
sender.close()
s.close()
print('end. ')
