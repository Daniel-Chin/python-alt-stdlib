'''
Auto bin number.  
'''
import numpy as np

def autoBin(data):
    data_range = np.max(data) - np.min(data)
    return int(np.ceil(data_range / (np.std(data) / 3)))
