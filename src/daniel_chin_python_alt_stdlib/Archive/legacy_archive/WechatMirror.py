import socket
wechat="180.163.26.39"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 2334))
print("binded. listening")
s.listen(1)
(c, address) = s.accept()
S.settimeout(.05)
c.settimeout(.05)
print("Connection from client. ")
S.connect((wechat,80))
print("Connection from server. ")
#
r='.'
frm=c
to=S
while 1:
    try:
        r=frm.recv(1)
        if r=='':break
        print(r.decode(),end='')
        to.send(r)
    except:
        t=frm
        frm=to
        to=t
input('end')
