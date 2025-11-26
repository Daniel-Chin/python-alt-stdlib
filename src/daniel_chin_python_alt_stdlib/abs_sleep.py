'''
Sleep on an absolute schedule.  
'''

from time import sleep, perf_counter

class AbsSleep:
    def __init__(self):
        self.last_wake = perf_counter()
    
    def sleep(self, duration: float):
        self.last_wake += duration
        to_sleep = self.last_wake - perf_counter()
        if to_sleep >= 0:
            sleep(to_sleep)
        else:
            print('Warning: missed the schedule by', - to_sleep, 'sec')
