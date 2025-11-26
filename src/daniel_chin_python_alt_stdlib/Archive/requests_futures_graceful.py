'''
Does requests_futures interrupt the sockets on exit?  
Conclusion: even socket is graceful!
'''

from __future__ import annotations

from typing import *
from time import sleep
from threading import Thread
import concurrent.futures as futures
from requests import Response

from requests_futures.sessions import FuturesSession

def main():
    with FuturesSession(max_workers=1) as session:
        class T(Thread):
            def run(self):
                while True:
                    print('starting req...')
                    f: futures.Future[Response] = session.get(
                        # 'https://www.google.com', 
                        'http://localhost', 
                        headers = {
                            'Host': 'www.google.com',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
                            'Accept': '*/*',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Referer': 'https://www.google.com/',
                            'Origin': 'https://www.google.com',
                            'Connection': 'keep-alive',
                            'TE': 'Trailers',
                        }, 
                    )
                    futures.wait([f])
                    response = f.result()
                    print(response.text[:64])
                    sleep(1)
        
        T().start
        input('...')

    print('session closed.')

def whatAboutSockets():
    import socket
    server = socket.socket()
    server.bind(('localhost', 2333))
    server.listen(1)
    a = socket.socket()
    a.connect(('localhost', 2333))
    b, _ = server.accept()
    def f():
        try:
            while True:
                print('a recv', a.recv(999))
        finally:
            print('recver finally')
    Thread(target=f).start()
    input('...0')
    b.send(b'asd')
    input('...1')
    a.close()
    print('closed')
    input('...2')

# main()
whatAboutSockets()
