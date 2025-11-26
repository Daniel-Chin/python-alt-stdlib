from time import time, sleep

import mouse
import keyboard as kb

SPEED = 1000
FPS = 60

is_active = False

def onKey(x):
    global is_active
    if x.name == '3' and x.event_type == 'down':
        is_active = not is_active
kb.hook(onKey)

print('Good to go...')
t = time()
try:
    while True:
        dt = time() - t
        t += dt
        x, y = mouse.get_position()
        if is_active:
            mouse.move(x + SPEED * dt, y)
        sleep(1 / FPS)
except KeyboardInterrupt:
    print('bye')
finally:
    kb.unhook_all()
