'''
Read from a PIPE async.  
See https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python  
'''

import subprocess as sp
from threading import Thread
from io import BytesIO

class Reader(Thread):
    def __init__(self, pipe: BytesIO) -> None:
        super().__init__()
        self.pipe = pipe
        self._buffer = BytesIO()
    
    def run(self):
        try:
            for line in iter(self.pipe.readline, b''):
                self._buffer.write(line)
        except BrokenPipeError:
            return
    
    def get(self):
        self.join()
        self._buffer.seek(0)
        return self._buffer

class PopenAsyncStd(sp.Popen):
    def __init__(self, *args, **kw):
        super().__init__(
            *args, 
            stdout=sp.PIPE, stderr=sp.PIPE, 
            **kw, 
        )
        self.outReader = Reader(self.stdout)
        self.errReader = Reader(self.stderr)
        self.outReader.start()
        self.errReader.start()
    
    def reportCollectedOutErr(self):
        print(self, 'out:')
        print(self.outReader.get().read().decode())
        print(self, 'err:')
        print(self.errReader.get().read().decode())

def test():
    with PopenAsyncStd(['python']) as p:
        p.wait()
    p.reportCollectedOutErr()

if __name__ == '__main__':
    test()
