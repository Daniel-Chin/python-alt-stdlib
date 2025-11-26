'''
PySerial already has a CLI monitor, but when it receives 
color formatting codes, it tries to print unprintable 
characters. Let's fix that.  
Features: 
- Color formatting.  
- Attach a time stamp to each line.  
- Merge multiple ports into one terminal.  
'''
from typing import *
from time import sleep, time
from datetime import datetime
import argparse
from threading import Thread, Lock
from io import BytesIO

import serial
import colorama

MAX_LINE_WAIT_TIME = .3

printLock = Lock()
should_exit = False

class ArgParser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-b', '--baud-rate', type=int, 
        )
        parser.add_argument(
            '-p', '--port-names', type=str, nargs='+', 
        )
        args = parser.parse_args()

        self.baud_rate: int = args.baud_rate
        self.port_names: str = args.port_names

def syncPrint(*args, **kw):
    with printLock:
        print(*args, **kw)

def main(port_names: List[str], baud_rate: int):
    global should_exit

    colorama.init()
    threads = []
    for port_name in port_names:
        thread = OnePort(port_name, baud_rate)
        thread.start()
        threads.append(thread)
    try:
        while True:
            syncPrint('Enter "q" to quit.')
            if input().lower() == 'q':
                break
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        print('releasing...')
        should_exit = True
        for thread in threads:
            thread.join()
        print('released.')

class OnePort(Thread):
    def __init__(self, port_name: str, baud_rate: int):
        super().__init__()
        self.port_name = port_name
        self.baud_rate = baud_rate
    
    def run(self):
        colorama.init()
        sleep(.5)   # for the user to read the instructions
        last_e_repr = None
        same_e_acc = 0
        while not should_exit:
            try:
                with serial.Serial(
                    self.port_name, self.baud_rate, 
                    timeout=MAX_LINE_WAIT_TIME, 
                ) as s:
                    syncPrint(
                        '', 
                        f'Serial opened: {s.name}', 
                        f'Baud rate: {self.baud_rate}', 
                        '==============', 
                        sep='\n', 
                    )
                    bIO = BytesIO()
                    line_birth = None
                    def flush():
                        nonlocal line_birth

                        timestamp = datetime.fromtimestamp(
                            line_birth, 
                        ).strftime('%H:%M:%S')
                        line_birth = None
                        bIO.seek(0)
                        line = bIO.read().decode('unicode-escape')
                        bIO.truncate(0)
                        bIO.seek(0)
                        syncPrint(
                            timestamp, self.port_name, line, 
                            end='', 
                        )
                    while not should_exit:
                        if line_birth is not None and time() - line_birth > MAX_LINE_WAIT_TIME:
                            flush()
                        if s.in_waiting == 0:
                            try:
                                data = s.read(1)
                            except serial.SerialTimeoutException:
                                continue
                        else:
                            data = s.read(s.in_waiting)
                        iData = iter(data)
                        for byte in iData:
                            if line_birth is None:
                                line_birth = time()
                            bIO.write(bytes([byte]))
                            if byte == ord('\n'):
                                flush()
            except serial.serialutil.SerialException as e:
                e_repr = f'{e} {e.args}'
                if last_e_repr == e_repr:
                    same_e_acc += 1
                    syncPrint(f'The above exception repeated {same_e_acc} times. ', end='\r', flush=True)
                else:
                    last_e_repr = e_repr
                    syncPrint('\n\n', e_repr, '\n', sep='')
                    same_e_acc = 0
                sleep(1)

if __name__ == '__main__':
    argParser = ArgParser()
    main(argParser.port_names, argParser.baud_rate)
