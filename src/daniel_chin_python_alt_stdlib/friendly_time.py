'''
Formatting time data in a friendly manner. 
'''
import time

def friendlyTime(raw_time=None):
    if raw_time is None:
        raw_time = time.time()
    LocalTimeTuple=['%02d' % x for x in time.localtime(raw_time)[0:6]]
    return '-'.join(LocalTimeTuple[0:3])+' '+\
           ':'.join(LocalTimeTuple[3:6])

if __name__=='__main__':
    print(friendlyTime())
    input('Enter...')
