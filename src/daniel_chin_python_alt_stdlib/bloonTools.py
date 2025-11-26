'''
automaitcally press 222222
'''

from time import sleep
from threading import Thread, Lock
import keyboard as kb
from holdKeyContext import HookRedirect

hr = None
rapid_2 = False

def rapid2():
    while rapid_2:
        kb.send('1')
        sleep(.1)
        kb.send('2')
        sleep(.1)
    print('rapid 2: stop')

def onKey(x):
    global rapid_2
    if x.event_type != 'down': 
        return
    if x.name == '1':
        rapid_2 = not rapid_2
        if rapid_2:
            print('rapid 2: start')
            Thread(target = rapid2).start()

def main():
    global hr
    hr = HookRedirect(onKey)
    print('Press 2 to rapid 2. ')
    print('Enter to quit. ')
    print('Good to go...')
    with hr:
        input()

if __name__ == '__main__':
    main()
