'''
Stream-based median filter.  
'''

import numpy as np

class MedianFilter:
    '''
    Bad time complexity. Easy to implement.  
    '''
    def __init__(self, window_size):
        self.window_size = window_size
        self.buffer = np.zeros(window_size)
        self.cursor = 0
        self.is_filled = False
    
    def next(self, x: float):
        self.buffer[self.cursor] = x
        self.cursor += 1
        if self.cursor == self.window_size:
            self.cursor = 0
            self.is_filled = True
        if not self.is_filled:
            return None
        return np.median(self.buffer)
