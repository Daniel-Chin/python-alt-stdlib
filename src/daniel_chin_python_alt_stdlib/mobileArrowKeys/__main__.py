'''
WARNING: Running this may open vulnerabilities for your computer. 
Don't run this if you don't know what you are doing. 
Only run this if you are in a safe network, or inside a firewall. 
I am not responsible if someone attacks your computer through this server. 
'''
print('Loading...')
import keyboard
from interactive import listen
import sys
from myhttp import *
import os
from time import sleep
import qrcode
from threading import Thread
from local_ip import getLocalIP

PORT = 2347

trusted_ip = None

def main():
    server = MyServer(MyOneServer, PORT)
    server.start()
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    potential_ip = getLocalIP()
    imgs = []
    class ShowImgThread(Thread):
        def __init__(self, img):
            Thread.__init__(self)
            self.img = img
        
        def run(self):
            self.img.show()
    
    potential_ip = {*potential_ip} - {'192.168.56.1'}
    # Cisco Anyconnect shit
    for ip in potential_ip:
        addr = 'http://%s:%d' % (ip, PORT)
        try:
            imgs.append(qrcode.make(addr))
        except Exception as e:
            print('Error 198456', e)
        print(addr)
    print('Ctrl+C to stop.')
    print('Q to display QR code for phone scan.')
    try:
        while True:
            op = listen(timeout = 1)
            if op == b'\x03':
                raise KeyboardInterrupt
            elif op == b'q':
                [ShowImgThread(x).start() for x in imgs]
                print('Loading image.')
            elif op == b'\r':
                print()
    except KeyboardInterrupt:
        print('Received ^C. ')
    finally:
        server.close()
        server.join()

class MyOneServer(OneServer):
    def handle(self, request):
        if request.target == '/':
            with open('index.html', 'rb') as f:
                respond(self.socket, f.read())
        elif request.target == '/style.css':
            with open('style.css', 'rb') as f:
                respond(self.socket, f.read())
        elif request.target == '/script.js':
            with open('script.js', 'rb') as f:
                respond(self.socket, f.read())
        elif request.target in ['/favicon.ico']:
            pass
        else:
            num = request.target.lstrip('/')
            if num in [*'1234567890']:
                if num in '123':
                    keyboard.send('up')
                elif num in '4':
                    keyboard.send('left')
                elif num in '6':
                    keyboard.send('right')
                elif num in '789':
                    keyboard.send('down')
                respond(self.socket, b'Yup')
            else:
                respond(self.socket, b'Dirty Hacker')
                print('Unknown request:', request.target)

class MyServer(Server):
    def onConnect(self, addr):
        global trusted_ip
        if trusted_ip is None:
            trusted_ip = addr[0]
        elif addr[0] != trusted_ip:
            print('SOMEONE IS ATTACKING!', addr)
            self.close()

if __name__ == '__main__':
    main()
    sys.exit(0)
