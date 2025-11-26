'''
A game by Daniel
'''
print('Loading game...')
height=22
width=80
DogNo=12
import msvcrt as KeyBuff
from random import randint as rand
from time import sleep,time
def VoidFunc(trash=None):
    a=1
try:
    from os import system as cmd
except:
    cmd=VoidFunc
def cls():
    global HighGraphic
    if HighGraphic:
        cmd('cls')
    else:
        print('\n'*height)
def DisplayIntro():
    cls()
    intro='''


                       #    ####  #  #   # ###   ###  # #
                      # #   #    # # ## ## #     #  # # #
                      ###   # ## ### # # # ###   ###   #
                      # #   #  # # # # # # #     #  #  #
                      # #   #### # # # # # ###   ###   #
                    
                          ###   #  #   # ### ### #
                          #  # # # ##  #  #  #   #
                          #  # ### # # #  #  ### #
                          #  # # # #  ##  #  #   #
                          ###  # # #   # ### ### ###


'''
    for i in intro:
        print(i,flush=True,end='')
        if HighGraphic:
            sleep(.002)
        else:
            if i=='\n':
                sleep(.2)
    del intro
    print('Press Enter to play')
    cmd('color 5f')
    input()
    cls()
    cmd('color 0e')
    print('\n'*6)
    print(' '*20+'Your goal is to find Vera. ')
    print(' '*20+'However, you are surrounded by '+\
                 'a lot of non-Vera objects. ')
    print()
    print(' '*20+'You will be spawned at the center of the screen. ')
    print(' '*20+'You look like this: @ ')
    print(' '*20+'Remember what you look like. ')
    print()
    print(' '*20+'Use W, A, S, D to play. ')
    print(' '*20+'Press Enter to start...')
    input()
class ClsDog:
    def __init__(self):
        names=['a Small Corgi',\
               'a Corgi',\
               'a Large Corgi',\
               'a Small Husky',\
               'a Husky',\
               'a Large Husky',\
               'a Golden Retriever',\
               'a Border Collie',\
               'a German Shepherd',\
               'a Australian Shepherd',\
               'a Toby',\
               'a Samoyed']
        self._name=names[rand(0,len(names)-1)]
        self.image=chr(rand(33,122))
        self.pos=[0,0]
        self.pos[0]=rand(0,width-1)
        self.pos[1]=rand(0,height-1)
        self.v=[0,0]
        self.v[0]=rand(-1,1)
        self.v[1]=rand(-1,1)
        self.Vera=False
    def name(self):
        if self.Vera:
            return 'Vera'
        else:
            return self._name
    def move(self):
        supos=[0,0]
        for i in range(2):
            supos[i]=self.pos[i]+self.v[i]
            if supos[i]<0 or supos[i]>={0:width,1:height}[i]:
                self.v[i]=-self.v[i]
            self.pos[i]+=self.v[i]
        if collide()==self:
            msg(self.name()+' meets you! ')
def update(text=None):
    if text!=None:
        MsgHeight=5
        MsgTop=int((height-MsgHeight)/2)
        TextLen=len(text)
        indent=' '*int((width-TextLen-4)/2)
        printed=False
    ToPrint=''
    cls()
    for row in range(height):
        if text==None or row not in range(MsgTop,MsgTop+MsgHeight):
            RelevantDogs=[]
            for i in dog:
                if i.pos[1]==row:
                    RelevantDogs.append(i)
            PlayerInRow=player[1]==row
            for col in range(width):
                image=' '
                for i in RelevantDogs:
                    if i.pos[0]==col:
                        image=i.image
                if PlayerInRow:
                    if player[0]==col:
                        image='@'
                ToPrint+=image
            ToPrint+='\n'
        else:
            if not printed:
                ToPrint+=(indent+'*'*(TextLen+4)+'\n')
                ToPrint+=(indent+'* '+' '*TextLen+' *'+'\n')
                ToPrint+=(indent+'* '+    text   +' *'+'\n')
                ToPrint+=(indent+'* '+' '*TextLen+' *'+'\n')
                ToPrint+=(indent+'*'*(TextLen+4)+'\n')
                printed=True
    print(ToPrint)
    if text != None:
        input('Press Enter to continue...')
def collide():
    for i in dog:
        if i.pos==player and i not in MetDogs:
            if not i.Vera:
                MetDogs.append(i)
            return i
    return None
def msg(text):
    update(text)
cmd('title Find Vera')
print('Game launcher: ')
HighGraphic=False
if 'win' in input('Are you using Windows or Mac? \nI\'m using ').lower():
    print('Think about how good your CPU is. ')
    print('Now decide: do you wish to run this game in high graphic? ')
    print('Or high frame rate? ')
    print('If you have experienced lag in previous playthroughs, '+\
          'consider high frame rate. ')
    print('Type \"g\" for high graphic. ')
    print('Type \"f\" for high frame rate. ')
    if input().lower()=='g':
        HighGraphic=True
        print('High graphic mode! ')
    else:
        print('High frame rate mode! ')
input('Press Enter to launch the game...')
cls()
cmd('mode con: cols='+str(width)+' lines='+str(height+1))
DisplayIntro()
#Initialize
dog=[]
for i in range(DogNo):
    dog.append(ClsDog())
dog[rand(0,DogNo-1)].Vera=True
player=[int(width/2),int(height/2)]
MetDogs=[]
#Main loop
win=False
while not win:
    #Machine's turn
    for i in dog:
        i.move()
    update()
    #Your turn
    birth=time()
    while time()-birth<1:
        if KeyBuff.kbhit():
            op=KeyBuff.getch().decode().lower()
            for i in range(2):
                player[i]+={'w':[0,-1],\
                            's':[0,1],\
                            'a':[-1,0],\
                            'd':[1,0]}[op][i]
                player[i]=max(player[i],0)
                player[i]=min(player[i],{0:width-1,1:height-1}[i])
            update()
            meeter=collide()
            if meeter!=None:
                msg('You meet '+meeter.name()+'! ')
                if meeter.Vera:
                    msg('You found Vera! You win! ')
                    win=True
cls()
print('You won! ')
print()
print('There are',DogNo-1,'dogs in total, ')
print('you met',len(MetDogs),'of them. ')
print('The dogs that you met include: ')
print()
for i in MetDogs:
    print('\"'+i.image+'\":', i.name())
print()
input('Thanks for playing. ')
