from multi_term import *
from console import console
from os import path
from time import sleep

def demo_old():
    terminals = TerminalServer()
    terminals.newTerminal('debug')
    terminals.newTerminal('warning')
    term_3 = terminals.newTerminal('error') # also returns the terminal
    terminals['debug'].print('1+1=2\n' * 10)    # just like a dict
    term_3.print('1/0=?')
    terminals['warning'].print('Warning! Everything is OK! ')
    print('Try doing `term_3.print("lol")`')
    print('^Z to close.')
    console({**locals(), **globals()})
    term_3.close()  # you can close a specific
    terminals.closeAll()    # or close all

def main():
    t = TerminalThreePack('Example App', path.join(path.dirname(__file__), 'demo_logs'))
    t['info'].print('Demonstrating anti-injection feature...')
    t['info'].print(f'user input = <log_<log_deli>deli>')
    sleep(1)
    t['info'].print('Start demonstrating main features! ')
    try:
        for i in range(99):
            for k in range(-i, i):
                try:
                    p = i / k
                    t['debug'].print(i, '/', k, '=', p)
                except Exception as e:
                    t['warning'].exception()
                sleep(.5)
            t['info'].print(f'Rank {i} test complete! ')
    except KeyboardInterrupt:
        print('I hope that was fun!')
        print("Now it's your turn. ")
        console({**globals(), **locals()})

main()
