from subprocess import Popen
from mysocket import findAPort
from os import path
from socket import socket
from threading import Thread, Lock
import logging
import traceback
from io import StringIO

PORT = 2342
HELPER_FILENAME = path.join(path.dirname(__file__), 'helper.bat')

class TerminalServer(dict):
    '''
    Use terminalServer[name] to access terminals.  
    '''
    def __init__(self):
        self.serverSocket, self.port = findAPort()
        self.serverSocket.listen(1)
        self.ps = []
        self.lock = Lock()
    
    def newTerminal(self, name, header = ''):
        portAllocator = socket()
        portAllocator.bind(('localhost', PORT))
        portAllocator.listen(1)
        with self.lock: # because listen queue = 1
            try:
                self.ps.append(Popen(['explorer', HELPER_FILENAME]))
            except FileNotFoundError:
                raise Exception('multi_term only works on Windows OS. ')
            sock, addr = portAllocator.accept()
            sock.send(str(self.port).encode())
            sock.send(b'\n')
            sock.close()
            portAllocator.close()
            sock, addr = self.serverSocket.accept()
        terminal = AnotherTerminal(name, sock, header)
        self[name] = terminal
        print(f'New terminal launched @ {addr}. ')
        return terminal
    
    def closeAll(self):
        [x.close() for x in self.values()]

class AnotherTerminal:
    def __init__(self, name, sock, header):
        self.name = name
        self.sock = sock
        self.logger = None
        self.delimiter = '<log_deli>'
        self.errorTerminal = None
        self.propagateTerminal = None
        self.header = header
        self.threads = []
        self.lock = Lock()
        self.print(name, header = '')
        self.print(f'\n\n--- Terminal "{name}" ---', header = '')
    
    def setLogger(self, name, filename, level):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.log_level = level
    
    def log(self, message):
        while self.delimiter in message:
            (self.errorTerminal or self).print(f'Terminal "{self.name}" encounters log delimiter collision! Sign of an attack! ')
            message = message.replace(self.delimiter, '')
        self.logger.__getattribute__(self.log_level.lower())(message + self.delimiter)
    
    def exception(self, message = ''):
        errorIO = StringIO()
        traceback.print_exc(file = errorIO)
        errorIO.seek(0)
        self.print(message + '\n' + errorIO.read(), end = '')
    
    def printall(self, text):
        self.logger and self.log(text)
        self.sock.sendall(text.encode())
    
    def print(self, *args, sep = ' ', end = '\n', flush = False, header = None):
        if header is None:
            header = self.header
        text = header + sep.join([str(x) for x in args]) + end
        with self.lock:
            self.threads.append(Thread(target = self.printall, args = [text]))
            self.threads[-1].start()
        if self.propagateTerminal is not None:
            self.propagateTerminal.print(text, end = '', header = '')
        with self.lock:
            for i, thread in reversed([*enumerate(self.threads)]):
                if not thread.isAlive():
                    thread.join()
                    self.threads.pop(i)
    
    def close(self):
        self.sock.close()

class TerminalThreePack(TerminalServer):
    def __init__(self, app_name, log_path):
        super().__init__()
        for name in ['warning', 'info', 'debug']:
            self.newTerminal(name, name.upper() + ' ').setLogger(
                f'{app_name}.{name}', 
                path.join(log_path, name + '.log'), name
            )
            self[name].errorTerminal = self['warning']
        self['warning'].propagateTerminal = self['info']
        self['info'].propagateTerminal = self['debug']
