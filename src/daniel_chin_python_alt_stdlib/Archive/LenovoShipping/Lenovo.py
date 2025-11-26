from pickle_socket import PickleSocket
import sys
import rsa
from os import system as cmd
import os
import tree
import socket
from interactive import listen

def main():
    global s
    s=openPort()
    print('Enter to accept...')
    if listen() != b'\r':
        s.close()
        input('Aborted! Enter...')
        sys.exit(1)
    os.chdir('D:/')
    op=s.recvObj()
    while op != 'en':
        print(op)
        if op=='ls':
            ls()
        elif op=='cd':
            cd()
        elif op=='cf':
            cf()
        elif op=='tf':
            tf()
        elif op=='td':
            td()
        else:
            s.close()
            input('Error: Strange command! ')
        op=s.recvObj()
    s.close()
    input('Session ends. Enter...')

def openPort():
    print('Lenovo IP =',socket.gethostbyname(socket.gethostname()))
    ss=PickleSocket()
    ss.bind(('',2336))
    ss.listen(1)
    print('Listening...')
    s,addr=ss.accept()
    print('Connection from',addr)
    return s

def ls():
    global s
    s.sendObj(os.listdir())

def cd():
    global s
    try:
        os.chdir(s.recvObj())
        s.sendObj(os.getcwd())
    except Exception:
        s.sendObj(b'error')

def cf():
    global s
    filename=s.recvObj()
    if os.path.isfile(filename):
        s.sendObj(True)
        s.sendObj(os.path.getsize(filename))
    else:
        s.sendObj(False)

def tf():
    global s
    filename=s.recvObj()
    s.sendObj(os.path.getsize(filename))
    s.socket.sendfile(open(filename,'rb'))

def td():
    global s
    root=tree.mirror(os.getcwd())
    s.sendObj(root)
    if s.recvObj()=='y':
        sendFullDir(s,root)
        s.sendObj(b'ok')

def sendFullDir(pickleSocket,folder):
    for i in folder.sub_file:
        file_len=os.path.getsize(i.name)
        pickleSocket.sendObj(file_len)
        pickleSocket.socket.sendfile(open(i.name,'rb'))
    for i in folder.sub_folder:
        os.chdir(i.name)
        sendFullDir(pickleSocket,i)
        os.chdir('..')

main()
sys.exit(0)
