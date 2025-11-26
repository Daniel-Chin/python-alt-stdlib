'''
Time-based round robin scheduling.  
'''
from time import perf_counter
import numpy as np

def roundRobinSched(n_workers):
    ages = np.zeros((n_workers, ))
    while True:
        elected = ages.argmin()
        start = perf_counter()
        yield elected
        end   = perf_counter()
        ages[elected] += end - start

if __name__ == '__main__':
    from time import sleep
    from random import random
    tasks = []
    for i in range(2):
        t = random() * .1
        tasks.append(t)
    for i in roundRobinSched(len(tasks)):
        t = tasks[i]
        sleep(t)
        print('slept for', t)
