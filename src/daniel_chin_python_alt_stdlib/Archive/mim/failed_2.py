from subprocess import Popen
from sys import stdin, stdout

saved_stdin_read = stdin.read
saved_stdout_write= stdout.write

def readAndRemeber(x):
    t = saved_stdin_read(x)
    print(t)
    return t

def writeAndRemeber(x):
    print(x)
    return saved_stdout_write(x)

stdin.read = readAndRemeber
stdout.write = writeAndRemeber

def main():
    p = Popen('python')
    p.wait()

main()
