from safe_http import main as safeMain, BaseHandler
import os
from os import path
from io import StringIO
from urllib.parse import quote, unquote
from time import time

SUPRESS = ['favicon.ico']

def main():
    safeMain(Handler, log_dir = path.join(path.dirname(__file__), 'logs'))

class Handler(BaseHandler):
    def __init__(self, request, *args, **kw):
        super().__init__(request, *args, **kw)
        assert request.command == 'GET'
        if request.target == '/':
            self.prepareResponse = self.prepareListDir
        else:
            self.prepareResponse = self.prepareFile
    
    def prepareListDir(self, debug, info, warning):
        self.response_content.write(b'<h1>Safe and Simple File Server</h1>')
        self.response_content.write(b'<br />\n'.join([f'<a href="/{quote(x)}">{x}</a>'.encode() for x in os.listdir() if path.isfile(x)]))
        self.content_length = self.response_content.tell()
        self.response_content.seek(0)
        return 'done'
    
    def prepareFile(self, debug, info, warning):
        target = unquote(self.request.target)[1:]
        all_files = [x for x in os.listdir() if path.isfile(x)]
        if target not in all_files:
            if target not in SUPRESS:
                warning.print(self.addr, "requested unknown file:", target)
            return 'close'
        self.response_content = open(target, 'rb')
        self.content_length = path.getsize(target)
        self.content_type = 'application/octet-stream'
        return 'done'
    
    def unlink(self):
        self.response_content.close()
