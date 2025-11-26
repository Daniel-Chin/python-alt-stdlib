'''
To test the security of getpass.  
'''
import subprocess
from time import sleep
from sys import stdout

def main():
    p = subprocess.Popen(('python'), stdin=subprocess.PIPE, stdout = stdout)
    p.stdin.write(b'from getpass import getpass;raise Exception(getpass())\r\n')
    p.stdin.close()
    print('waiting...')
    p.wait()

main()
