from subprocess import Popen
from io import TextIOWrapper

class FakeStdin(TextIOWrapper):
    def __init__(self):
        self.my_buffer = []
    
    def read(self, x):
        return ''.join([self.my_buffer.pop(0) for i in range(x)])
    
    def getInput(self):
        return input('>>> ')

class FakeStdout():
    def write(self, s):
        print(s)

def main():
    stdin = FakeStdin()
    stdout = FakeStdout()
    p = Popen('python', stdin = stdin, stdout = stdout)
    p.wait()

main()
