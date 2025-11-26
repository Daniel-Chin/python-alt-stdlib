from interactive import charGettor
from time import sleep

print('Demo of normal functionalities')
print('Waiting for a key press, timeout = 1')
t = charGettor.consume(timeout = 1)
if t is None:
    print('No key was pressed.')
else:
    print(t)
print('===========\n')

print('Waiting for a key press, infinite wait')
print(charGettor.consume())
print('===========\n')

print('I will be doing other stuff.')
print('Press one key at any time, while I am doing other stuff. ')
input('Enter to continue... ')
for i in range(5):
    sleep(.5)
    print('Busy doing other stuff...')
print('Waiting for a key press, timeout = 1')
t = charGettor.consume(timeout = 1)
if t is None:
    print('No key was pressed.')
else:
    print(t)
print('This works because `getch` deals with keyboard buffer.')
print('===========\n')

print('Now, a loop.')
while True:
    print('Waiting for a key press, timeout = 1')
    t = charGettor.consume(timeout = 1)
    if t is None:
        pass
    else:
        print(t)
        break
print('===========\n')

print('Try Ctrl + C.')
print('Waiting for a key press, infinite wait')
print(charGettor.consume())

print('Try Ctrl + C. We should see consistent results.')
while True:
    print('Waiting for a key press, timeout = 1')
    t = charGettor.consume(timeout = 1)
    if t is None:
        pass
    else:
        print(t)
        break
print('Confused? Search "\\x03" in ./__init__.py')
print('===========\n')

try:
    import msvcrt
    print('''Run this script on a non-Windows platform 
to demo problems specific to them.''')
    input('Enter to exit...')
    exit()
except ImportError:
    pass
print('Now, demo of problems with charGettor on non-Windows. ')
print('Problem 1: timeout = 0 does not guarantee to read ' 
      + 'from the keyboard buffer.')
input('Enter to continue...')
print('Please press a key while I am doing other stuff.')
input('Enter to start...')
for i in range(5):
    sleep(.5)
    print('Busy doing other stuff...')
print('Now, if you pressed a key, there should be a key ' + 
      'in the keyboard buffer waiting to be read.')
sleep(1)
print("Let's see what happens when we do `timeout` = 0.")
sleep(1)
print('Waiting for a key press, timeout = 0')
t = charGettor.consume(timeout = 0)
if t is None:
    print('No key was pressed.')
else:
    print(t)
print('99% of the time, we fail to detect your key press. ')
print('For reasons, read source code. ')
print('However, there is a way of using this library to avoid this problem.')
print('''Note. Now I will wait for key press again, 
without you pressing anything.''')
sleep(1)
print('Waiting for a key press, timeout = 0')
t = charGettor.consume(timeout = 0)
if t is None:
    print('No key was pressed.')
else:
    print(t)
print('It received the previous key press.')
print('Conclusion: you are fine if you do `timeout`=0 in a loop. ')
print('===========\n')

print('Problem 2: eaten input.')
print("Please don't press anything when you see 'NO PRESS'. ")
input('Enter to continue... ')
print('NO PRESS')
print('Waiting for a key press, timeout = 1')
t = charGettor.consume(timeout = 1)
if t is None:
    print('No key was pressed.')
else:
    print(t)
print("If no key was pressed, the next `input()` will miss the first char.")
print('`input` returned:', input('Please type "1234" and Enter: '))
print('The "1" is redirected to charGettor. See:')
print('Waiting for a key press, timeout = 1')
t = charGettor.consume(timeout = 1)
print('===========\n')

print('Problem 3: ESC conflicts with arrow keys')
print('see `help(charGettor.getFullCh)`')
print('When we expect ESC but you press arrow key:')
print('(Please press an arrow key)')
print('Waiting for a key press, infinite wait')
print(charGettor.consume(priorize_esc_or_arrow = True))
print('We mistake your arrow key for an ESC. ')
print('Also, future calls to `consume` gives extra chars.')
print('Waiting for a key press, infinite wait')
print(charGettor.consume())
print('Waiting for a key press, infinite wait')
print(charGettor.consume())
print('===========\n')
input('Enter to continue...')
print('When we expect arrow keys but you press ESC,')
print('We will block infinitely.')
print('(Please press ESC)')
print('(Rescue the blocking by pressing 2 letter keys.)')
print('Waiting for a key press, infinite wait')
print(charGettor.consume(priorize_esc_or_arrow = False))
print('===========\n')

print('Problem 4: Program exit may be blocked')
print("Please don't press anything when you see 'NO PRESS'. ")
input('Enter to continue... ')
print('NO PRESS')
print('Waiting for a key press, timeout = 1')
t = charGettor.consume(timeout = 1)
if t is None:
    print('No key was pressed.')
else:
    print(t)
print("""We are now exiting. 
But the deamon thread won't join until you press a key.""")
