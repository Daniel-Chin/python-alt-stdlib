'''
For a clean namespace.  
I later realized that this can be done with arguments to exec and eval.  
'''
def Kernal(__namespace = {}):
    from os import system as cmd
    from pprint import pprint
    from interactive import cls
    
    __file__ = None
    if __namespace:
        for __name in __namespace:
            if not __name.startswith('_'):
                exec(f'{__name}=__namespace["{__name}"]')
        del __name
        try:
            __file__ = __namespace['__file__']
        except KeyError:
            pass
    del __namespace
    def restart():
        '''
        runs __file__. This usually restarts the module. 
        You can use Ctrl + R to invoke this function too. 
        '''
        from sys import exit
        if __file__ is not None:
            cls()
            cmd('py ' + __file__)
            print('Ended.')
            exit(0)
        else:
            print('To use `restart()`, you have to supply a namespace with __file__, for example, globals().')
    while True:
        try:
            try:
                __command = yield
            except GeneratorExit:
                return
            if __command == 'exit':
                return
            try:
                yield eval([__command + '\r', exec('del __command')][0])
                # Tries to hide `__command` in dir(). 
                # doesn't work tho. 
                # But you have to admit, it's a clever try. 
                continue
            except SyntaxError:
                pass
            exec(__command + '\r')
            yield None
        except SystemExit:
            from sys import exit
            exit(0)
        except:
            import traceback
            traceback.print_exc()
            del traceback
            yield None

if __name__ == '__main__':
    kernal = Kernal({})
    next(kernal)
    while True:
        print(kernal.send(input('>> ')))
        next(kernal)
