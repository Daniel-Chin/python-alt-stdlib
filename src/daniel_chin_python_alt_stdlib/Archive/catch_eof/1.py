for i in range(4):
    try:
        input('Press ^Z: ')
    except Exception:
        print('except')
    finally:
        print('finally')
input('again?')
print('more execution')
import time
time.sleep(1)
print('last line')
