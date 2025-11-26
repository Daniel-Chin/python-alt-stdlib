import platform
from interactive import inputChin
from .kernal import Kernal
import random

def console(namespace = {}, prompt = '>>> ', use_input = False, fixer = None):
    if random.randint(0, 5) == 0:
        print('console.console Warning: no support for reassigning module global variables. ')
    else:
        print('No global. ')
    history = []
    kernal = Kernal(namespace)
    next(kernal)
    while True:
        if use_input:
            try:
                command = input(prompt)
            except EOFError:
                command = 'exit()'
        else:
            try:
                command = inputChin(prompt, '', history, kernal)
            except EOFError:
                command = 'exit()'
            except KeyboardInterrupt:
                command = 'print("KeyboardInterrupt")'
            if not command:
                continue
            stripped = command.strip()
            long_string = stripped.count("'''") % 2 == 1
            if long_string or stripped[:1] == '@' or stripped[-1:] in ':({[\\': 
                # `:1` so blank input doesnt trigger IndexError
                got = command
                while True:
                    history.append(got)
                    try:
                        got = inputChin('... ', '', history, kernal)
                    except KeyboardInterrupt:
                        command = 'print("KeyboardInterrupt")'
                        break
                    command += '\n' + got
                    if long_string:
                        if got.count("'''") % 2 == 1:
                            break
                    else:
                        if not got:
                            break
        if fixer is not None:
            command = fixer(command)
        if command in ('exit', 'exit()'):
            try:
                kernal.send('exit')
            except StopIteration:
                return
            assert False
        if command == '':
            continue
        if command == '\x12':   #^R
            command = 'restart()'
        if command == 'help':
            print('Module `console`:')
            print(__doc__)
        history.append(command.split('\n')[-1])
        result = kernal.send(command)
        next(kernal)
        if result is not None:
            print(result)
