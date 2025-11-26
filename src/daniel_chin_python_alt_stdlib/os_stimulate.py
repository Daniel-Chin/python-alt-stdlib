'''
My laptop is weird. Running this script makes opening and terminating processes faster. 
Speculation: Taking CPU time away from Windows Defender? 
'''
DEFAULT_INTERVAL = 5
print('Interval =', DEFAULT_INTERVAL, end = '\r')
print('Interval = ', end = '', flush = True)
from subprocess import Popen
from time import sleep
from os import kill

SIGKILL: int = 9

def main(): 
    try: 
        interval: int = int(input())
        assert interval > 0
    except:
        interval = DEFAULT_INTERVAL
    while True:
        print('open')
        p: Popen = Popen('taskmgr')
        sleepLoud(interval)
        print('kill')
        kill(p.pid, SIGKILL)
        sleepLoud(2)

def sleepLoud(length):
    assert type(length) is int
    for i in range(length):
        print(i, end = '', flush = True)
        sleep(1)

if __name__ == '__main__':
    main()
