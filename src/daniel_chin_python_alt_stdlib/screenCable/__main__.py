'''
Playback a section of your screen.  
Useful for sharing PPT (with speaker notes on) over Tencent (VooV) Meeting.  
Hit `ESC` or `q` to quit.  
Hit `Spacebar` to refresh view.  
Click and drag to resize the window.  
'''
WINDOW = 'screenCable'

import numpy as np
import cv2
from mss import mss
from time import sleep

drag_state = None
rect = {
    'left': 585, 'top': 200, 
    'width': 1195, 'height': 675, 
}

def mouseEvent(event, x, y, flags, param):
    global drag_state
    if flags == cv2.EVENT_FLAG_LBUTTON:
        drag_state = 1
        rect['width'] = x
        rect['height'] = y
        cv2.resizeWindow(WINDOW, x, y)
    if event == cv2.EVENT_LBUTTONUP:
        drag_state = 2

def main():
    global drag_state
    drag_state = 2
    try:
        while True:
            session()
            sleep(.2)
            drag_state = 0
    except KeyboardInterrupt:
        print('exiting...')
    finally:
        cv2.destroyAllWindows()
        print('ok')

def session():
    global drag_state
    with mss() as sct:
        cv2.imshow(
            WINDOW, 
            np.array(sct.grab(rect)), 
        )
        cv2.setMouseCallback(WINDOW, mouseEvent)
        cv2.waitKey(300)
        while True:
            if drag_state == 0:
                cv2.imshow(
                    WINDOW, 
                    np.array(sct.grab(rect)), 
                )
            key_press = cv2.waitKey(33) & 0xFF
            rect['left'], rect[
                'top'
            ], _, __ = cv2.getWindowImageRect(WINDOW)
            if key_press in (
                ord('q'), 
                27, 
            ):
                raise KeyboardInterrupt
            elif key_press == ord(' ') or drag_state == 2:
                break
    cv2.destroyWindow(WINDOW)

main()
