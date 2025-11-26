'''
Stellaris game assistant.  
Assignes hotkey to planet prev/next buttons and 
pop growth specification buttons.  
'''

DEFAULT_POS = [750, 100]
BUTTON_DISTANCE = 35

import mouse
import keyboard
from time import sleep

pos = DEFAULT_POS[:]

def main():
    keyboard.add_hotkey('p', clickPrev)
    keyboard.add_hotkey('[', clickNext)
    keyboard.add_hotkey(']', clickGrowing)
    keyboard.add_hotkey('\\', clickAssembling)
    keyboard.add_hotkey('shift+p', setPrev)
    # keyboard.block_key('m')
    print('go...')
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print('Ctrl+C received. Quiting...')
    finally:
        keyboard.unregister_all_hotkeys()
        print('All resources released. ')

def clickPrev():
    print('prev')
    mouse.move(*pos)
    sleep(.1)
    mouse.click()

def clickNext():
    print('next')
    mouse.move(pos[0] + BUTTON_DISTANCE, pos[1])
    sleep(.1)
    mouse.click()

def clickGrowing():
    print('assembling')
    mouse.move(pos[0] - 35, pos[1] + 280)
    sleep(.1)
    mouse.click()
    sleep(.1)
    #mouse.move(pos[0] + 200, pos[1] + 280)
    mouse.move(pos[0] + 200, pos[1] + 130)
    sleep(.1)
    mouse.click()

def clickAssembling():
    print('assembling')
    mouse.move(pos[0] + 20, pos[1] + 280)
    sleep(.1)
    mouse.click()
    sleep(.1)
    mouse.move(pos[0] + 200, pos[1] + 280)
    sleep(.1)
    mouse.click()

def setPrev():
    x, y = mouse.get_position()
    pos[0] = x
    pos[1] = y
    print(x, y)

main()
