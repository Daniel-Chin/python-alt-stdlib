import keyboard as kb
import mouse
from time import time, sleep

state = True
def onKey(x):
    global state
    if x.name == 'v' and x.event_type == 'up':
        state = not state

kb.hook(onKey)
print('Good to go. Press V...')
try:
    while True:
        sleep(.5)
        if not state:
            print('passed')
            continue
        mouse.click()
        print('clicked')
        sleep(9)
        if not state:
            print('passed')
            continue
        kb.send('esc')
except KeyboardInterrupt:
    print('bye')
finally:
    kb.unhook_all()
