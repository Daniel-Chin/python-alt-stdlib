from os import system as cmd
from pickle import load
from time import sleep
def DoIt():
    f=open('Punch Yourself.jpg','wb')
    t=open('trump.pickle','rb')
    f.write(load(t))
    f.close()
    t.close()
    cmd('explorer Punch Yourself.jpg')
    sleep(3)
    cmd('del "Punch Yourself.jpg"')
DoIt()
