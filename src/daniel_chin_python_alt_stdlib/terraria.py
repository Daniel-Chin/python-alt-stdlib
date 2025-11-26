'''
Terraria bot.  Automated fishing.  
Vision: bait catching, and defending invasions.  
Result: Failed! This macro does not work on Terraria!  
'''

print('Loading...')
import mouse
import keyboard
from macro import Failsafe
import time
from console import console

DO = 'fish()'

failsafe = None

def interact():
    console(globals())

def sleep(x):
    assert failsafe is None or failsafe.green
    time.sleep(x)
    assert failsafe is None or failsafe.green

def fish():
    global failsafe
    failsafe = Failsafe()
    failsafe.start()
    while True:
        for i in range(16):
            mouse.click()
            sleep(3)
            mouse.click()
            sleep(.3)
        keyboard.press_and_release('2')
        sleep(.3)
        keyboard.press_and_release('4')
        sleep(.3)

print('Done. Now:', DO)
exec(DO)
