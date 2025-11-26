'''
Sets up a server, displays a QR code. Scan it to go to a web page. Exchange raw texts!  
Useful for sending a URL from the phone to the laptop.  
Warning: No authentication or encryption. Don't type in secrets. Don't assume who the remote is.  
'''
import os, sys
import urllib
from threading import Thread
import socket

import psutil
import qrcode

from myhttp import Server, OneServer, respond

PORT = 2339

def getLocalIPs():
    ips = set()
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ips.add(addr.address)
    return ips

def main():
    server = MyServer(MyOneServer, port=PORT)
    server.start()
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    potential_ips = getLocalIPs()
    imgs = []
    class ShowImgThread(Thread):
        def __init__(self, img):
            Thread.__init__(self)
            self.img = img
        
        def run(self):
            self.img.show()
    potential_ips -= {'127.0.0.1'}
    potential_ips -= {'192.168.56.1'} # Cisco Anyconnect shit
    print(potential_ips)
    for ip in potential_ips:
        addr = 'http://%s:%d' % (ip, PORT)
        try:
            imgs.append(qrcode.make(addr))
        except Exception as e:
            print('Error 198456', e)
        print(addr)
    [ShowImgThread(x).start() for x in imgs]
    try:
        input()
    except KeyboardInterrupt:
        print('Received ^C. ')
    finally:
        server.close()
        server.join()

class MyOneServer(OneServer):
    def handle(self, request):
        if request.target == '/':
            with open('page.html', 'rb') as f:
                respond(self.socket, f.read())
        elif request.target.startswith('/msg'):
            msg = urllib.parse.unquote(request.target[4:])
            print(msg)
            respond(self.socket, b'Yup')
        elif request.target in ['/favicon.ico']:
            pass
        else:
            print('Unknown request:', request.target)
        return True

class MyServer(Server):
    def handleQueue(self, intent):
        pass
    
    def interval(self):
        pass

    def onConnect(self, addr):
        pass

if __name__ == '__main__':
    main()
    sys.exit(0)
