'''
My misc little tools.  
- @profileFrequency() decorates a function to measure how often it's called.  
- @profileDuration() decorates a function to report how long it took to run.
'''
import os
import time

class ChangeDir:
    def __init__(self, path):
        print('Warning: deprecated in favor of chdir_context.py')
        self.path = path
        self.home = []
    
    def __enter__(self):
        self.home.append(os.getcwd())
        os.chdir(self.path)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.home.pop(-1))

def debug(func, *args, **kw):
    try:
        func(*args, **kw)
    except Exception:
        import traceback
        traceback.print_exc()
        input('Enter...')

def profileFrequency(interval: float = 1.0, format_str: str = '.2e'):
    def decorator(func):
        last_time = time.time()
        acc = 0
        def decorated(*args, **kw):
            nonlocal last_time, acc
            acc += 1
            now = time.time()
            if now - last_time > interval:
                print(f'''{func.__name__}: {format(
                    acc / interval, format_str, 
                )} Hz''')
                acc = 0
                last_time = now
            return func(*args, **kw)
        return decorated
    return decorator

def profileDuration(format_str: str = '.2e'):
    def decorator(func):
        def decorated(*args, **kw):
            start = time.perf_counter()
            ret = func(*args, **kw)
            dt = time.perf_counter() - start
            print(f'{func.__name__}: {format(dt, format_str)} sec')
            return ret
        return decorated
    return decorator
