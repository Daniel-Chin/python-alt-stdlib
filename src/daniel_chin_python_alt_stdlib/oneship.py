'''
一嗖传
Transmit files over the internet / LAN
No encryption! Consider everything you transmit broadcast to the entire network. 
'''
print('importing...')
from mysocket import recvFile, sendFileJdt
from interactive import listen
from pickle_socket import PickleSocket
try:
    from tkinter import Tk,filedialog
except ImportError:
    Tk = None
    from interactive.console_explorer import askForFile, askSaveWhere
from socket import gethostname,gethostbyname
import sys
from os.path import getsize, basename, isfile, splitext, dirname
import platform
from local_ip import getLocalIP

print('loading...')
port=2337
professional = False
last_dir = None

def main():
    global professional
    if len(sys.argv) == 2 and sys.argv[1] == '!':
        print('Professional mode. ')
        professional = True
    s=PickleSocket()
    print('My IP =',gethostbyname(gethostname()))
    print('or...', getLocalIP())
    server = None
    try:
        print('Server or Client? s/c')
        if listen((b's',b'c')) == b's':
            s.bind(('',port))
            s.listen(1)
            print('Listening...')
            server = s
            s,addr=server.accept()
            print('Connection from',addr)
            print('Accept? y/n')
            if listen((b'y',b'n')) == b'n':
                s.close()
                s = None
                input('Aborted. Enter to exit...')
                sys.exit(1)
        else:
            ip=input('Connect to IP: ')
            print('Connecting...')
            s.connect((ip,port))
        print('Connected! Waiting for response... ')
        s.shakeHands('One ship python by Daniel Chin. ')
        
        esc=b'\x1b'
        op=b''
        while op != esc:
            if op==b's':
                send(s)
            elif op==b'r':  #Cannot use ELSE, cuz op maybe b''.
                recv(s)
            print()
            print('Send, receive, or exit? s/r/esc')
            op=listen((b's',b'r',esc))
    finally:
        if s:
            s.close()
        if server:
            server.close()

def send(s):
    global last_dir
    if professional:
        print('input "raw" to send raw text data. ')
        filename = input('path/file.ext = ').strip('"')
        if filename == 'raw':
            print('Raw text: ')
            buffer = []
            op = input()
            while op != '':
                buffer.append(op)
                op = input()
            data = '\n'.join(buffer).encode()
            print('Sending...')
            s.sendObj('raw.txt')
            s.sendObj(len(data))
            s.socket.sendall(data)
            print('Succeed. ')
            return
    else:
        if Tk:
            root=Tk()
            root.withdraw()
            root.update()
            filename=filedialog.askopenfilename(title='Choose file to send',initialdir='D:/')
        else:
            filename = askForFile(last_dir)
            last_dir = dirname(filename)
    if filename=='':
        s.sendObj(0)
        return None
    size=getsize(filename)
    print('Sending...')
    s.sendObj(basename(filename))
    s.sendObj(size)
    sendFileJdt(s.socket, open(filename,'rb'))
    print('File sent:',filename)

def recv(s):
    global last_dir
    print('Waiting for sender...')
    basename=s.recvObj()
    size=s.recvObj()
    path = {
                'Windows': 'D:/downloads/', 
                'Linux': '/sdcard/download/',
                'Darwin': '/'
           }[platform.system()]
    print('Default receive path:',path)
    print('Use it, or change? Enter/c')
    if listen((b'c',b'\r'))==b'c':
        if professional:
            filename = input('path/file.ext = ')
        else:
            if Tk:
                root=Tk()
                root.withdraw()
                root.update()
                filename=filedialog.asksaveasfilename(title='Where to receive',initialdir='D:/',initialfile=basename)
            else:
                filename = askSaveWhere(last_dir, initialfile = basename)
                last_dir = dirname(filename)
        if filename=='':
            s.close()
            input('Error: filename="". Enter to exit...')
            sys.exit(1)
    else:    
        filename = path + basename
    while isfile(filename):
        base,ext=splitext(filename)
        base+='2'
        filename=base+ext
    recvFile(s.socket,size,filename)
    print('File received:',filename)

if __name__=='__main__':
    main()
    sys.exit(0)
