print('Loading...')
from Daniel import jdt
from tkinter import Tk,filedialog
import socket
from os import path as os_path
#from os import system as cmd

def strict_recv(size):
    chunk=b''
    while size>0:
        recved=s.recv(size)
        size-=len(recved)
        chunk+=recved
    return chunk
def send(chunk):
    while chunk!=b'':
        chunk=chunk[s.send(chunk):]
def send_file():
    send(b'send')
    input('Press Enter and specify which file to send. ')
    Tk().withdraw()
    filename=filedialog.askopenfilename(title='Choose file to send')
    print('Sending file: ',filename)
    filesize=os_path.getsize(filename)
    send(format(filesize,'16').encode())
    file_nopath_name=filename.split('/')[-1]
    send(format(file_nopath_name,'64')[-64:].encode())    
    file=open(filename,'rb')
    total_MB=filesize//1024**2
    j=jdt.CommJdt(total_MB)
    for MB in range(total_MB):
        j.update(MB)
        for KB in range(1024):
            send(file.read(1024))
    send(file.read(filesize%1024**2))
    j.complete()
    print('File sent! ')
    file.close()
def recv_file():
    send(b'recv')
    print('Waiting for sender...')
    filesize=int(s.recv(16).decode())
    origin_name=s.recv(64).decode().rstrip()
    print('Sender wants to send file:',origin_name)
    print('Kind note: you might want to copy the file name.')
    input('Press Enter and specify where to store the file. ')
    Tk().withdraw()
    filename=filedialog.asksaveasfilename(initialfile=origin_name,defaultextension=origin_name.split('.')[-1])
    file=open(filename,'wb')
    recved=b'this string could be anything'
    recvsize=0
    total_MB=filesize//1024**2
    i=0
    j=jdt.CommJdt(total_MB)
    while recved!=b'':
        recved=s.recv(1024)
        file.write(recved)
        recvsize+=len(recved)
        i+=1
        if i==1024:
            i=0
            j.update(recvsize//1024**2)
    j.complete()
    if recvsize==filesize:
        print('File successfully received. ')
    else:
        print('File fragment received. There is somehow some loss of bytes. ')
        print('Loss:',((filesize-recvsize)/filesize,'4%'))
    file.close()
    print(filename)
#
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
abip='10.209.1.45'
dormip='10.209.23.186'
print('If Daniel is at AB, type \"a\". \nIf he is at dorm, type \"d\". ')
op= input('>> ').lower()
if op=='a':
    serverip=abip
elif op=='d':
    serverip=dormip
elif op=='daniel':
    serverip=input('Custom IP=')
elif op=='me':
    serverip='127.0.0.1'
else:
    print('Invalid. The App will quit now. ')
    input()
    exit()
print('Connecting...')
s.connect((serverip,2336))
print('Connected! ')
#Verify. 
enemy_ip_len=int(strict_recv(2).decode())
enemy_ip=strict_recv(enemy_ip_len).decode()
print('The other\'s IP =',enemy_ip)
print('If you don\'t want to send your beloved file to a stranger, ')
print('Verify the IP address! ')
valid=False
while not valid:
    print('To send file, type \"send\"')
    print('To receive file, type \"recv\"')
    print('To terminate connection, type Ctrl+Z')
    op=input('>> ')
    if op=='send':
        send_file()
        valid=True
    elif op=='recv':
        recv_file()
        valid=True
    else:
        print('Invalid input. Please try again: ')
s.close()
input('Thanks for using OneFileFly. Press Enter to exit app. ')
