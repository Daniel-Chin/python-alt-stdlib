'''
Uses the `keyboard` package to hold down a key.  
1. `with ...` clause avoids forgetting to release a key.  
2. Blocks the held key, and redirect it to your hook.  
'''

import keyboard as kb

class HookRedirect:
    def __init__(self, callback = None):
        self.userCallback = callback
        self.hook_returned = None
        self.holdKeyContext = self.notReady
    
    def notReady(self):
        raise Exception('You must enter the HookRedirect context first.')
    
    def setHook(self, callback):
        self.userCallback = callback
        return self
    
    def __enter__(self):
        self.holdKeyContext = self.__holdKeyContext
        self.hook_returned = kb.hook(self.userCallback)
        return self
    
    def __exit__(self, _, __, ___):
        kb.unhook(self.hook_returned)
        self.holdKeyContext = self.notReady
    
    def __holdKeyContext(self, key_name):
        return self.__HoldKeyContext(self, key_name)

    class __HoldKeyContext:
        def __init__(self, root, key_name) -> None:
            self.key_name = key_name
            self.root = root
            self.status = 0
        
        def __enter__(self):
            kb.hook_key(
                self.key_name, self.callbackWrapper, 
                suppress=True, 
            )
            kb.press(self.key_name)
        
        def __exit__(self, _, __, ___):
            kb.release(self.key_name)
            kb.unhook_key(self.key_name)
            for _ in range(self.status):
                kb.press(self.key_name)
            for _ in range(- self.status):
                kb.release(self.key_name)
        
        def callbackWrapper(self, event):
            '''
            `keyboard` package incorrectly (I think) unhooks 
            callbacks without a stack. So you need a wrapper 
            anyways. 
            '''
            if event.event_type == 'down':
                self.status += 1
            if event.event_type == 'up':
                self.status -= 1
            self.root.userCallback(event)

def test():
    from time import sleep
    print('baseline:')
    def onKey(x):
        if x.event_type != 'down': 
            return
        if x.name == 'p':
            kb.press('f')
            try:
                sleep(1)
            finally:
                kb.release('f')
        if x.name == 'f':
            print('t')
    kb.hook(onKey)
    try:
        input()
    finally:
        kb.unhook_all()

    print('ours:')
    hr = HookRedirect()
    def onKey(x):
        if x.event_type != 'down': 
            return
        if x.name == 'p':
            with hr.holdKeyContext('f'):
                sleep(1)
        if x.name == 'f':
            print('t')
    with hr.setHook(onKey):
        input()

if __name__ == '__main__':
    test()
