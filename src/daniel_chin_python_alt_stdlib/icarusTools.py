'''
1. automaitcally press FFFFFFFF  
2. Auto running with stamina management.  
'''

# No flatbread
RUN_TIME = 13
REST_TIME = 7
RUN_F_INTERVAL = 1

from time import sleep
from threading import Thread, Lock
import keyboard as kb
from audioCues import AudioCues
from holdKeyContext import HookRedirect

aC = None
hr : HookRedirect = None

rapid_f = False

auto_run = False
runLock = Lock()

def rapidF():
    with hr.holdKeyContext('f'):
        while rapid_f:
            sleep(.5)
    print('rapid f: stop')

def autoRun():
    n_f_run  = RUN_TIME  // RUN_F_INTERVAL
    n_f_rest = REST_TIME // RUN_F_INTERVAL
    def waitWhileF(n_f):
        for _ in range(n_f):
            if runLock.acquire(timeout = RUN_F_INTERVAL):
                runLock.release()
            if not auto_run:
                return
            kb.send('f')
    try:
        with hr.holdKeyContext('w'):
            waitWhileF(n_f_rest)
            if not auto_run:
                return
            while True:
                with hr.holdKeyContext('shift'):
                    waitWhileF(n_f_run)
                    if not auto_run:
                        return
                    with hr.holdKeyContext('space'):
                        sleep(.3)
                if not auto_run:
                    return
                waitWhileF(n_f_rest)
                if not auto_run:
                    return
    finally:
        print('auto run: stop')

def onKey(x):
    global rapid_f, auto_run
    if x.event_type != 'down': 
        return
    if x.name in '-_':
        rapid_f = not rapid_f
        if rapid_f:
            print('rapid f: start')
            Thread(target = rapidF).start()
    elif x.name in '/?':
        if not auto_run:
            auto_run = True
            print('auto run: start')
            runLock.acquire()
            Thread(target = autoRun).start()
        else:
            auto_run = False
            runLock.release()
    elif x.name == 'space':
        pass
    else:
        # print('got else', x.name)
        if auto_run:
            auto_run = False
            runLock.release()
    if rapid_f or auto_run:
        aC.startLado(amp = .01)
    else:
        aC.mute()

def main():
    global aC, hr
    hr = HookRedirect(onKey)
    print('Press - to rapid f. Press / to auto run.')
    print('Enter to quit. ')
    print('Good to go...')
    aC = AudioCues()
    try:
        with hr:
            input()
    finally:
        aC.close()

if __name__ == '__main__':
    main()
