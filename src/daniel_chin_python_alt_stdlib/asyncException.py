'''
Send exceptions to other threads.  
Based on Philippe F's https://stackoverflow.com/a/325528/8622053  
If the thread is busy in a system call (socket.accept(), ...), 
the exception is simply ignored.  
'''

from threading import Thread, ThreadError
from typing import Type
import inspect
import ctypes

def asyncRaise(thread: Thread, ExcType: Type[BaseException]):
    '''
    Raises an exception in the threads with id `tid`
    '''
    if not inspect.isclass(ExcType):
        raise TypeError("Only types can be raised (not instances)")
    if not thread.isAlive():
        raise ThreadError(f'Thread not alive: {thread}')
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread_id), ctypes.py_object(ExcType), 
    )
    if res == 0:
        raise ValueError(f'invalid thread id "{thread_id}"')
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread_id), None, 
        )
        raise SystemError("PyThreadState_SetAsyncExc failed")
