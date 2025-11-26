'''
Progress bar.  
Did you know about `tqdm`?  

Usage:  
```python
with Jdt(500, 'loading...') as j:
    for i in range(500):
        j.acc()
        doJob(i)
```

Run this file to see demo.  

Set `override_terminal_width` when using Jupyter Notebook with jdt. 
'''
from time import time
from math import log
from terminalsize import get_terminal_size
from graphic_terminal import clearLine

override_terminal_width = None

def effectiveTermWidth():
    return override_terminal_width or get_terminal_size()[0]

class JdtAlreadyClosedError(BaseException):
    '''Cannot update Jdt after complete. '''

def smartUnit(size, is_speed=False):
    '''
    n_byte => 6-char string with smart unit (KB, MG, GB)
    '''
    if size == 0:
        return '   0  '
    if is_speed:
        magnitude = int(log(size, 1024))
    else:
        magnitude = int(log(size / 9, 1024))
    magnitude = min(magnitude, 3)
    return format(size / 1024**magnitude, '4.0f') + \
         {0: 'B ', 1: 'KB', 2: 'MB', 3: 'GB'}[magnitude]

class Jdt:
    MIN_BAR_WIDTH = 6

    def __init__(self, goal, msg='', width=None, UPP = 1):
        self.active = True
        self.goal = goal
        self.msg = msg
        if width is not None:
            print('jdt Warning: argument `width` is deprecated. ')
        self.done = 0
        self.UPP = UPP
        self.UPP_count = 0
        # updates per print
        self.print_mode = False

    def getSuffix(self, done, progress):
        return '%s Total: %d Done: %d' % (
            format(progress, '4.0%'), 
            self.goal, 
            done
        )

    def update(self, new_done, symbol = '*', getSuffix = None, flush = False):
        if not self.active:
            raise JdtAlreadyClosedError
        self.done = new_done
        if not flush and self.UPP_count > 0:
            self.UPP_count -= 1
            return
        self.UPP_count = self.UPP - 1
        if self.goal == 0:
            progress = 1
        else:
            progress = new_done / self.goal
        terminal_width = effectiveTermWidth() - 4
        if getSuffix is None:
            getSuffix = self.getSuffix
        suffix = getSuffix(new_done, progress)
        msg_and_bar_width = terminal_width - len(suffix)
        msg_width = min(len(self.msg), int(msg_and_bar_width / 2))
        msg_to_print = self.msg[-msg_width:]
        bar_width = msg_and_bar_width - msg_width
        if bar_width < self.MIN_BAR_WIDTH:
            bar_width = terminal_width - 2
            msg_to_print = ''
            suffix = ''
        bar_inner_width = bar_width - 2
        bar_fill_width = int(bar_inner_width * progress)
        bar_empty_width = bar_inner_width - bar_fill_width
        print('\r', msg_to_print, ' ', 
              '[', symbol * bar_fill_width, '_'*bar_empty_width, ']', 
              ' ', suffix, 
              sep = '', end='',flush=True)
        self.print_mode = False

    def acc(self):
        self.update(self.done + 1)
    
    def complete(self):
        def getSuffix(done, progress):
            return 'Complete! Total: %d' % self.goal
        self.update(self.goal, symbol = '#', getSuffix = getSuffix, flush = True)
        self.active = False
        print()
    
    def print(self, *args, **kw):
        if not self.print_mode:
            self.print_mode = True
            clearLine()
            print()
            print(f'jdt {self.done} / {self.goal}')
        print(*args, **kw)
    
    def __enter__(self):
        return self
    
    def __exit__(self, e_type, e_value, e_trace):
        if e_type is None:
            self.complete()

class CommJdt(Jdt):
    def __init__(self, *argv, **kw):
        super(__class__, self).__init__(*argv, **kw)
        self.last_time = time()
    
    def update(self, new_done, *argv, **kw):
        delta_time = time() - self.last_time
        self.last_time += delta_time
        delta_done = new_done - self.done
        self.done = new_done
        if delta_time == 0:
            speed = 999999999
        else:
            speed = delta_done / delta_time
        def getSuffix(done, progress):
            nonlocal speed
            return '%s Total: %s Done: %s Speed: %s/s' % (
                format(progress, '4.0%'), 
                smartUnit(self.goal), 
                smartUnit(done), 
                smartUnit(speed, is_speed = True)
            )
        kw['getSuffix'] = getSuffix
        super(__class__, self).update(new_done, *argv, **kw)

def jdtIter(iterable, msg='', width = None, UPP = 1, goal = None):
    '''
    `iterable` must provide `__len__()`. 
    '''
    goal = goal or len(iterable)
    with Jdt(goal, msg, width, UPP) as j:
        for x in iterable:
            yield x
            j.acc()

if __name__=='__main__':
    from time import sleep
    j=CommJdt(10240000, '/sdcard/download/browser/file.jpg')
    for i in range(0,10240000,32345):
        j.update(i)
        sleep(0.01)
    j.complete()

    with Jdt(500, 'launching game') as j:
        for i in range(500):
            if i == 200:
                j.print('Something happens!')
                j.print('Logging information')
                j.print('more information haha')
            if i == 300:
                j.print('Something else happens!')
                j.print('Logging information')
            sleep(0.01)
            j.acc()

    for i in jdtIter(range(500), 'jdtIter test'):
        sleep(0.01)
    input('Enter..')
