'''
AFK tool for Minecraft.  
Punch the air every 5 seconds so you don't get kicked for inactivity.  
'''
import mouse
from time import sleep

def main():
    print('When we start, you will have 5 seconds to switch to Minecraft.')
    input('Press Enter to start..')
    print('Press Ctrl+C to stop.')
    sleep(5)
    print('Clicking...')
    while True:
        sleep(5)
        mouse.click()

main()
