import msvcrt
from time import sleep

def GetFullCh():
    first=msvcrt.getch()
    if first in (b'\x00', b'\xe0'):
        return first + msvcrt.getch()
    else:
        return first

def listen(choice=None,wait=0):
    '''
    choice can be a list of choices or a single choice. 
    Elements can be b'' or ''.
    If wait=0, it's blocking. 
    wait is in second. 
    '''
    if choice is not None:
        if type(choice) in (bytes, str):
            choice=choice,
        bChoice=[]
        for i in choice:
            if type(i) is bytes:
                bChoice.append(i)
            else:
                bChoice.append(i.encode())
    print('',end='',flush=True)
    if wait != 0:
        fps=30
        for i in range(int(wait*fps)):
            if msvcrt.kbhit():
                break
            sleep(1/fps)
        else:
            return None
    op=GetFullCh()
    while not (choice is None or op in bChoice):
        op=GetFullCh()
    return op

if __name__=='__main__':
    from IPython import embed
    embed()
