'''
Move cursor with Pro Controller.  
'''

VELOCITY = .3
SPF = .016
DEADZONE = .25

SCALE = VELOCITY / SPF

from threading import Thread
from time import sleep
import pygame
import mouse
import keyboard

class Worker(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.dx = 0
        self.dy = 0
        self.go_on = True
    
    def run(self):
        while self.go_on:
            move(self.dx, self.dy)
            sleep(SPF)

def main():
    pygame.init()
    worker = Worker()

    print('Controllers:')
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        j = pygame.joystick.Joystick(i)
        print(' ', j.get_name())
        j.init()
        joysticks.append(j)

    print('main loop...')
    try:
        worker.start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print(event.button)
                    if event.button in (0, 7, 8, 9, 10):
                        print('press')
                        mouse.press()
                    elif event.button == 11:
                        keyboard.press_and_release('up')
                    elif event.button == 12:
                        keyboard.press_and_release('down')
                    elif event.button == 13:
                        keyboard.press_and_release('left')
                    elif event.button == 14:
                        keyboard.press_and_release('right')
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button in (0, 7, 8, 9, 10):
                        print('release')
                        mouse.release()
                elif event.type == pygame.JOYAXISMOTION:
                    axis, value = event.axis, event.value
                    # print('    ' * (axis + 1), value)
                    value = value ** 3 * abs(value) ** 1
                    value *= SCALE
                    if axis in (0, 2):
                        if abs(value) < DEADZONE:
                            worker.dx = 0
                        else:
                            worker.dx = value
                    if axis in (1, 3):
                        if abs(value) < DEADZONE:
                            worker.dy = 0
                        else:
                            worker.dy = value
                print(worker.dx, '\t', worker.dy)
    finally:
        worker.go_on = False
        worker.join()
        print('bye')

def move(dx, dy):
    x, y = mouse.get_position()
    x += dx
    y += dy
    mouse.move(x, y)

main()
