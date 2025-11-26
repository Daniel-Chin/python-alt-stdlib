import os
import platform

def cls():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
