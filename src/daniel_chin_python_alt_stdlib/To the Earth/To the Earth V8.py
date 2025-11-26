'''
A game by Daniel. 

My personal second / third python project. You can see a lot of bad coding styles. 

Updates description:
    V3:
        + Added: new weapon = Holy Sickle
            Acquired through Annoying Cat
            Ulti: ATK+1
            20% Vamparic.
        + Added: Personal high score.
        + Improved: Game over prompt.
    V4:
        Fixed: Holy Sickle works properly now.
    V5:
        Fixed: Now the game actually restarts when you die.
        + Added: Next Daily Hint
        Edit: Intro screen now uses black background
        Fixed: Daily Hint regarding the behavior of Annoying cat.
        + Added: drop weapon msg
        Fixed: DeltaHP now reflects the aggregate effect of healing and dmg
        Fixed: Easter item drop rate was higher than normal weapons'...
        Fixed: Critical Hit chance > 100%
        + Added: Holy Sickle now increase GamePace. 
        + Added: When Holy Sickle ATK=100, Ulti becomes IronMan
    V6:
        very hihg speed -> incredible hihg speed
    V7:
        First play will show kidding death msg
    V8:
        Changed the abbr of Space Corgi to " Corgi"
'''
print('Declaring global constants...')
WinSize=[76,18]
EarthDis=2017
MeditateSafe=15
Meditability=.1
TravelSafe=10
ProllyMaxLevel=120
StrikePerEnemy=5
ProllyLvUpKills=8
GoodWeaponRarity=5
LegendaryRarity=100
WalkPhase=['-','\\','|','/']
UltiFullCharge=10
GamePace=.3
HPperLv=4
mercy=.5
Cafeteria=1
LaserPower=19
print('Importing...')
from os import system as cmd
from random import randint as rand,uniform as UniRand
from time import sleep,time,gmtime as AggregateDemand
from pickle import dump,load
try:
    import msvcrt as KeyBuff
except:
    input('This game can only be played in Windows. ')
    input('Yeah. I\'m sorry. ')
    input('The game will quit now. ')
    input('I\'m really sorry. ')
    exit()
print('Loading functions...')
def listen(WaitUntilGet=False):
    if WaitUntilGet:
        op=listen()
        while op==None:
            op=listen()
        return op
    else:
        if KeyBuff.kbhit():
            try:
                return KeyBuff.getch().decode()
            except:
                return None
def draw(pos,text):
    printer[pos[1]]=printer[pos[1]][:pos[0]] + text +\
                    printer[pos[1]][pos[0]+len(text):]
def smart(pos,text,align='m'):
    Pos=list(pos)
    for i in range(2):
        if type(pos[i])==type(0.1):
            Pos[i]=min(int(pos[i]*WinSize[i]),WinSize[i]-1)
    if '\n' in text:
        TextList=text.split('\n')
        for i in range(len(TextList)):
            smart((Pos[0],Pos[1]+i),TextList[i])
    else:
        if align=='m':
            draw((Pos[0]-int(len(text)/2),Pos[1]),text)
        elif align=='r':
            draw((Pos[0]-len(text)+1,Pos[1]),text)
        else:
            draw(Pos,text)
def HUD(ActionMenu=True):
    global traveled,EarthDis,DeltaEnemyHP,DeltaHP,DeltaTraveled,HP,EnemyHP,\
           nowHP,nowEnemyHP,Lv,hit,evade,critical,criticalDMG,WpName,ATK,\
           EnemyName,enemy,status,HighScore
    cls()
    draw((3,0),'-'*24+'===| To the Earth |==='+'-'*24)
    draw((4,2),'Distance from the Earth: '+str(EarthDis-traveled)+' / '+\
         str(EarthDis)+' miles'+\
         (' ('+format(-DeltaTraveled,'+')+')')*(DeltaTraveled!=0))
    bar=66
    draw((4,3),'['+ '|'*int(traveled/EarthDis*bar)+\
               '_'*(bar-int(traveled/EarthDis*bar))+']')
    draw((5+int(HighScore/EarthDis*bar),3),'R')
    draw((5+int(traveled/EarthDis*bar),3),WalkPhase[walking])
    if DeltaHP==None:
        ShownDelta='(They missed)'
    elif DeltaHP==0:
        ShownDelta=''
    else:
        ShownDelta=format(DeltaHP,'+')
    draw((4,5),'Your HP: '+str(nowHP)+' / '+str(HP)+\
               ' '+ShownDelta)
    bar=31
    draw((4,6),'['+ '#'*int(nowHP/HP*bar)+'_'*(bar-int(nowHP/HP*bar))+']')
    #draw borders
    box((4,8),(37,14))
    box((39,8),(71,11))
    #write
    draw((6,9),'Character Level:')
    draw((6,10),'Accuracy:')
    draw((6,11),'Evasion:')
    draw((6,12),'Critical Hit Chance:')
    draw((6,13),'Critical Dmg Multiplier:')
    smart((34,9),str(Lv),align='r')
    smart((34,10),str(hit),align='r')
    smart((34,11),str(evade),align='r')
    smart((34,12),format(critical,'.0%'),align='r')
    smart((34,13),str(criticalDMG),align='r')
    draw((41,9),'Weapon:')
    draw((41,10),'ATK:')
    smart((68,9),WpName,align='r')
    smart((68,10),str(ATK),align='r')
    if enemy:
        draw((4,16),status)
        if DeltaEnemyHP==None:
            ShownDelta='(You missed)'
        elif DeltaEnemyHP==0:
            ShownDelta=''
        else:
            ShownDelta=format(DeltaEnemyHP,'+')
        DisplayedEnemyName={\
                 'Prof. Dreamurr':'Dreamr',\
                 'Frenzy Nut':'F.Nut',\
                 'Space Corgi':' Corgi',\
                 'Unidentified Hostile Object':'UHO',\
                 'Broken iPhone':'bPhone',\
                 'Augmented Dalek':'DALEK',\
                 'John Snow':'John *',\
                 'Pigeon Finch':'Pi.Finch',\
                 'Sheldon Carboon':'Sheld.Coo',\
                 'Robot Bender':'Ro.Bender',\
                 'Sponge Dod':'Spo.Dod',\
                 'Sherlock Residu':'Shresidu',\
                 'Pickle Wreckage':'Pickle',\
                 'Dr. Kaboom':'Dr.Boom',\
                 'Dog':'Dog',\
                 'JediWoosh':'JediWoo'}[EnemyName]
        draw((39,5),DisplayedEnemyName+' HP: '+str(nowEnemyHP)+' / '+str(EnemyHP)+\
             ' '+ShownDelta)
        bar=30
        draw((39,6),'['+ 'X'*int(nowEnemyHP/EnemyHP*bar)+\
                    '_'*(bar-int(nowEnemyHP/EnemyHP*bar))+']')
        draw((39,12),'Action Menu:')
        draw((52,13),'w:     Walk away')
        draw((52,14),'Space: Attack')
        draw((52,15),'u:     Ultimate')
    else:
        if ActionMenu:
            draw((39,12),'Action Menu:')
            draw((52,12),'m:     Meditate')
            draw((52,13),'s:     Seek enemy')
            draw((52,14),'d:     To the Earth')
            draw((52,15),'a:     Step back')
def cls():
    global printer
    printer=[' '*WinSize[0]]*WinSize[1]
def LvInfo(Lv):
    HP=Lv*HPperLv+5
    hit=int(Lv*.5+9)
    evade=int(Lv*.5+1)
    return (HP,hit,evade)
def display():
    print('\n'.join(printer),flush=True)
def intro():
    cls()
    smart((.5,4),'As you sit in the audi, listening to Prof. Corpslake,')
    smart((.5,5),'eating your Exotic Sandwich -')
    smart((.5,6),'A thunder strikes.'.upper())
    smart((.5,8),'You find yourself teleported,')
    smart((.5,9),'to a galaxy far, far away.')
    smart((.5,10),'The loneliness is unspeakable.\nYour goal:')
    smart((.5,13),'To the Earth.')
    display()
    wait()
def greet(HintNo=None):
    cls()
    smart((.5,.4),'Welcome back.')
    smart((.5,.45),'======================')
    if AggregateDemand(time())[1:3]==(Cafeteria,LaserPower):
        smart((.5,.6),'\x48\x61\x70\x70\x79\x20\x62\x69\x72\x74\x68\x64\x61\x79\x20\x56\x45\x52\x41\x21')
        display()
    else:
        DailyHint={0:'Forks have a special magical affection to their owner.\n'+\
                     'They refuse to be your weapon.',\
                   1:'The beginning of the journey is the hardest part.\n'+
                     'The game gets easier and easier as you grow.',\
                   2:'Occasionally, enemies drop legendary items\n'+
                     'that enhance your Critical Hits.\n'+
                     'Strong Critical Hits will make your gameplay a lot easier.',\
                   3:'When you die, the game resets. Better be careful!',\
                   4:'Meditating heals.',\
                   5:'Meditation could be interrupted by enemies.',\
                   6:'The closer you get to the Earth,\n'+\
                     'the stronger the enemies will be.\n'+
                     'Do not proceed too hastily.',\
                   7:'Hit chance = Attacker\'s Accuracy - Attackee\'s Evasion',\
                   8:'Increase your ATK by hunting for good weapons.',\
                   9:'Increase your Accuracy and Evasion by leveling up.',\
                   10:'The best way to hunt for good weapons is:\n'+
                     'walk away from those wielding a Fork.',\
                   11:'Useful game tips are displayed on this screen.',\
                   12:'The game saves your progress automatically.',\
                   13:'Walk away success chance = 50%.',\
                   14:'If you die a lot, it means you are too ambitious.\n'+\
                      'Fight weaker enemies and level up a bit before moving on.',\
                   15:'2 Uses of Ultimate: to save your life when HP is near 0,\n'+\
                      'or to defeat enemies stronger than you\n'+\
                      '(to claim their weapon).',\
                   16:'Think about how you can hunt for better weapons:\n'+\
                      'First, the enemy\'s weapon should be better than yours.\n'+\
                      'So, to defeat someone with a better weapon than yours,\n'+\
                      'you need to prevail them in other aspects.\n'+\
                      'Conclusion: Use Ultimate properly!',\
                   17:'There is a Holy weapon in this game,\n'+\
                      'but it is not easy to find.',\
                   18:'Defeating an enemy charges your weapon by +1.'}
        if HintNo==None:
            RandHintNo=rand(0,len(DailyHint)-1)
            smart((.5,.6),'Daily Hint:\n-------------\n'+DailyHint[RandHintNo])
            display()
            print('Press Space to continue, \"n\" to see the next hint.',end='',flush=True)
            op=''
            while op not in (' ','n'):
                op=listen(WaitUntilGet=True)
            print()
            if op=='n':
                RandHintNo=(RandHintNo+1)%len(DailyHint)
                while greet(RandHintNo):
                    RandHintNo=(RandHintNo+1)%len(DailyHint)
        else:
            smart((.5,.6),'Daily Hint:\n-------------\n'+DailyHint[HintNo])
            display()
            print('Press Space to continue, \"n\" to see the next hint.',end='',flush=True)
            op=''
            while op not in (' ','n'):
                op=listen(WaitUntilGet=True)
            print()
            if op=='n':
                return True
def msg(text,DoWait=True):
    t=text.split('\n')
    top=int((WinSize[1]-len(t))/2)
    width=0
    for i in range(len(t)):
        width=max(width,len(t[i]))
    left=int((WinSize[0]-width)/2)
    box((left-3,top-2),(left+width+4,top+len(t)+1))
    for i in range(len(t)):
        smart((.5,top+i),t[i])
    display()
    if DoWait:
        wait()
def box(start,end):
    width=end[0]-start[0]
    draw(start,'-'*width)
    draw((start[0],end[1]),'-'*width)
    for i in range(start[1]+1,end[1]):
        draw((start[0],i),'|'+' '*(width-2)+'|')
def wait(char=' '):
    if char==' ':
        msg='Press Space to continue...'
    else:
        msg='Press \"'+char+'\" to continue...'
    print(msg,end='',flush=True)
    op=listen()
    while op!=char:
        op=listen()
    print()
def NewEnemy():
    global traveled,enemy,EnemyName,EnemyATK,EnemyEvade,EnemyHit,EnemyHP,\
           EnemyWp,ProllyMaxLevel,StrikePerEnemy,EarthDis,nowEnemyHP,status
    enemy=True
    EnemyName=\
        {0:'Prof. Dreamurr',\
         1:'Frenzy Nut',\
         2:'Space Corgi',\
         3:'Unidentified Hostile Object',\
         4:'Broken iPhone',\
         5:'Augmented Dalek',\
         6:'John Snow',\
         7:'Pigeon Finch',\
         8:'Sheldon Carboon',\
         9:'Robot Bender',\
         10:'Sponge Dod',\
         11:'Sherlock Residu',\
         12:'Pickle Wreckage',\
         13:'Dr. Kaboom',\
         14:'JediWoosh'}[rand(0,14)]
    if rand(0,10)==0:  #if drop
        if rand(0,9)==0:  #if easter egg
            EnemyWp=\
                {0:'Frisk\'s Stick',\
                 1:'P.Y.T.H.O.N.',\
                 2:'Legendary Artifact',\
                 3:'Glove of Iron Man'}[rand(0,3)]
        else:
            EnemyWp=\
                {0:'Popsicle Sword',\
                 1:'Eyes of Vera',\
                 2:'Electric Clarinet',\
                 3:'Doctor\'s Spoon',\
                 4:'Blue Glowing Spear',\
                 5:'Offensive Mac Pro',\
                 6:'Very Sharp Ball',\
                 7:'Space Cadillac',\
                 8:'Domestic Sandwich'}[rand(0,8)]
    else:
        EnemyWp='Fork'
    EnemyLv=int(traveled/EarthDis*ProllyMaxLevel)
    (EnemyHP,EnemyHit,EnemyEvade)=LvInfo(EnemyLv)
    EnemyATK=int(EnemyHP/StrikePerEnemy)
    nowEnemyHP=EnemyHP
    status='Enemy encountered: '+EnemyName+'!'
    cmd('color 0e')
    HUD()
    msg('You encounter a '+EnemyName+'!\nThey are wielding a '+EnemyWp+\
        ' of an ATK = '+str(EnemyATK))
    cmd('color 0f')
    if EnemyWp!='Fork':
        cmd('color 0d')
        if rand(0,GoodWeaponRarity)==0:
            EnemyATK=int(1.5*EnemyATK)
            msg('You see that the '+EnemyWp+' is a rare one!\n'+\
                'You reevaluate it\'s ATK. Now you understand.\n'+\
                'It\'s ATK is '+str(EnemyATK)+'!',DoWait=False)
        else:
            msg('The '+EnemyWp+' boasts an ATK of\n'+str(EnemyATK),DoWait=False)
        wait(char='q')
        cmd('color 0f')
def attack(NoMiss=False):
    global ATK,nowEnemyHP,hit,EnemyEvade,critical,criticalDMG,DeltaEnemyHP,\
           WpName,nowHP,HP,DeltaHP
    HitChance=min(max((hit-EnemyEvade)/10,0),1)
    if UniRand(0,1)<HitChance or NoMiss:
        multiplier={True:criticalDMG,False:1}[UniRand(0,1)<critical]
        DeltaEnemyHP=-ATK*multiplier
        nowEnemyHP+=DeltaEnemyHP
        if WpName=='Holy Sickle':
            DeltaHP=-int(DeltaEnemyHP*.2)
            nowHP=min(HP,nowHP+DeltaHP)
        CheckEnemyDeath()
    else:
        DeltaEnemyHP=None
def CheckEnemyDeath():
    global nowEnemyHP,Lv,EnemyWp,EnemyATK,EnemyName,enemy,WpName,\
           UltiCharge,UltiFullCharge,Lv,ATK,HP,EnemyHP,critical,criticalDMG,\
           nowHP
    if nowEnemyHP<=0:
        nowEnemyHP=0
        status=''
        HUD()
        display()
        msg(EnemyName+' is neutralized!')
        enemy=False
        if UltiCharge==UltiFullCharge-1:
            cmd('color 6f')
            msg(WpName+'\'s Ultimate is ready!',DoWait=False)
            wait(char='q')
            cmd('color 0f')
        UltiCharge=min(UltiCharge+1,UltiFullCharge)
        if rand(0,int(ProllyLvUpKills*.8**((EnemyHP-HP+1)/HPperLv)))==0:
            Lv+=1
            nowHP=HP
            msg('You leveled up!',DoWait=False)
            wait(char='q')
            HUD()
            DeltaHit={0:'+1',1:'+0'}[Lv%2]
            msg('You are now Lv '+str(Lv)+'.\n\nHP +'+\
                str(HPperLv)+'\nAccuracy '+DeltaHit+\
                '\nEvasion '+DeltaHit)
        if EnemyWp!='Fork':
            msg('The enemy dropped a weapon!')
            msg('The enemy was wielding a '+EnemyWp+\
                '.\nIt\'s ATK = '+str(EnemyATK)+\
                '.\nYour weapon\'s ATK = '+str(ATK)+\
                '.\nPress \"t\" to take, \"d\" to discard.',DoWait=False)
            op=''
            while op not in ('t','d'):
                op=listen(WaitUntilGet=True).lower()
            if op=='t':
                msg('New weapon get: '+EnemyWp)
                ATK=EnemyATK
                WpName=EnemyWp
                if WpName=='Legendary Artifact':
                    UltiCharge=0
                else:
                    UltiCharge=UltiFullCharge
            else:
                msg(EnemyWp+' discarded.')
        if rand(0,LegendaryRarity)==0:
            cmd('color 1f')
            msg('A legendary item is dropped!\nYou absorb it.',DoWait=False)
            wait(char='q')
            if critical>=.95 or rand(0,2)==0:
                critical=1
                criticalDMG+=1
                msg('Your Critical Hit Dmg Multiplier +1!')
            else:
                msg('Your Critical Hit Chance +10%!')
                critical+=.1
            cmd('color 0f')
def EnemyTurn():
    global EnemyATK,nowHP,EnemyHit,evade,DeltaHP,EnemyName,status,EnemyWp,\
           NewHighScore,HighScore,died
    HitChance=min(max((EnemyHit-evade)/10,0),1)
    if nowHP<=EnemyATK and UniRand(0,1)<mercy:
        HitChance=0
    if UniRand(0,1)<HitChance:
        DeltaHP-=EnemyATK
        nowHP-=EnemyATK
        if nowHP<=0:
            HUD()
            ClearSaveFile()
            msg('You died...',DoWait=False)
            wait(char='q')
            if NewHighScore and not FirstPlay:
                msg('But guess what?\nYou broke your personal record!')
                msg('New Highscore\n\nDistance from the Earth\n'+str(EarthDis-HighScore))
                msg('Let\'s try to challenge that!')
            else:
                msg('But worry not!')
                msg('Let\'s just start from the beginning!')
            died=True
    else:
        DeltaHP=None
    status={0:EnemyName+' is dashing towards you!',\
            1:EnemyName+' is playing with their '+EnemyWp,\
            2:'Something seems to be distracting '+EnemyName+'.',\
            3:EnemyName+' is whistling.',\
            4:'Stars from afar shine upon '+EnemyName+'.',\
            5:EnemyName+' is rolling in space.',\
            6:EnemyName+' is trying to look cute.'}[rand(0,6)]
def ClearSaveFile(ClearHighScore=False):
    global HighScore
    with open('Pickle','wb') as SaveFile:
        dump(('clear',{False:HighScore,True:0}[ClearHighScore]),SaveFile)
        SaveFile.close()
def FastTravel(destination,direction):
    global traveled,walking,DeltaTraveled,HighScore,NewHighScore,enemy
    enemy=False
    if destination<0:
        destination=0
    elif destination>=EarthDis:
        destination=EarthDis-1
    while traveled!=destination:
        traveled+=direction
        walking=(walking+direction)%4
        HUD(ActionMenu=False)
        display()
        sleep(.05)
    if traveled>HighScore:
        HighScore=traveled
        if not NewHighScore:
            NewHighScore=True
            msg('You just surpassed your personal record\nof how close you ever got to the Earth!')    
#Main
win=False
while not win:
    print('Initializing...')
    died=False
    status=''
    printer=[' '*WinSize[0]]*WinSize[1]
    Lv=1
    (HP,hit,evade)=LvInfo(Lv)
    nowHP=HP
    WpName='Exotic Sandwich'
    ATK=1
    traveled=0
    DeltaTraveled=0
    DeltaHP=0
    EnemyHP=1
    EnemyATK=0
    EnemyHit=0
    EnemyEvade=0
    DeltaEnemyHP=0
    nowEnemyHP=0
    critical=0.1
    criticalDMG=2
    enemy=False
    meditating=False
    EnemyName=''
    EnemyWp=''
    walking=0
    UltiCharge=0
    HighScore=0
    NewHighScore=False
    cmd('mode con: cols='+str(WinSize[0]+1)+' lines='+str(WinSize[1]+1))
    cmd('color 0f')
    cmd('title To the Earth')
    print('Loading SaveFile...')
    try:
        with open('Pickle','rb') as SaveFile:
            save=load(SaveFile)
            SaveFile.close()
        if save[0]=='clear':
            #New game
            HighScore=save[1]
            intro()
            FirstPlay=False
        else:
            #continue
            (traveled,Lv,nowHP,WpName,ATK,critical,criticalDMG,\
             enemy,EnemyName,EnemyATK,EnemyEvade,EnemyHit,EnemyWp,\
             nowEnemyHP,EnemyHP,UltiCharge,HighScore)=save
            greet()
            FirstPlay=False
    except Exception as err:
        #First game
        intro()
        NewHighScore=True
        FirstPlay=True
    #Main loop
    while not died and not win:
        (HP,hit,evade)=LvInfo(Lv)
        HUD()
        display()
        if meditating:
            cmd('color 0a')
            meditating=False
        else:
            cmd('color 0f')
        #Save
        with open('Pickle','wb') as SaveFile:
            dump((traveled,Lv,nowHP,WpName,ATK,critical,criticalDMG,\
                  enemy,EnemyName,EnemyATK,EnemyEvade,EnemyHit,EnemyWp,\
                  nowEnemyHP,EnemyHP,UltiCharge,HighScore),SaveFile)
            SaveFile.close()
        if WpName=='Holy Sickle':
            sleep(GamePace/3)
        else:
            sleep(GamePace)
        listen()#clear buffer
        if enemy:
            ValidKeys=('w',' ','u')
        else:
            ValidKeys=('a','s','d','m')
        op=''
        while op not in ValidKeys:
            op=listen(WaitUntilGet=True).lower()
        cmd('color 0f')
        DeltaEnemyHP=0
        DeltaHP=0
        DeltaTraveled=0
        if enemy:
            if 'w' == op:
                if rand(0,1)==0:
                    cmd('color 0b')
                    msg('You escaped from '+EnemyName+'!\n'+\
                        EnemyName+' laughs at you...')
                    cmd('color 0f')
                    enemy=False
                else:
                    cmd('color 0c')
                    msg('You try to walk away,\nbut '+EnemyName+\
                        ' decides not to let you go...')
                    cmd('color 0f')
                    EnemyTurn()
            elif op==' ':
                attack()
                if enemy:
                    EnemyTurn()
            elif op=='u':
                if UltiCharge==UltiFullCharge:
                    msg(WpName+':\nUltimate Ability\n\n-= '+\
                        {'Popsicle Sword'       :'Lick',\
                            'Eyes of Vera'      :'Melt the Enemy',\
                            'Electric Clarinet' :'Recital',\
                            'Doctor\'s Spoon'   :'Scoop and Eat',\
                            'Frisk\'s Stick'    :'Throw',\
                            'P.Y.T.H.O.N.'      :'Mysterious Ability',\
                            'Legendary Artifact':'Summon Something Annoying',\
                            'Blue Glowing Spear':'NGAHHHH',\
                            'Offensive Mac Pro' :'Offend the Enemy',\
                            'Very Sharp Ball'   :'Slash',\
                            'Glove of Iron Man' :'Propel',\
                            'Space Cadillac'    :'Drive at a Very Hihg Speed',\
                            'Domestic Sandwich' :'Bite',\
                            'Annoying Cat'      :'Sit on Enemy\'s weapon',\
                            'Exotic Sandwich'   :'Enjoy',\
                            'Holy Sickle'       :'Upgrade',\
                         }[WpName]+' =-\n\nPress \"y\" to activate\n'+\
                        'Press \"n\" to cancel',DoWait=False)
                    op=''
                    while op not in ('y','n'):
                        op=listen(WaitUntilGet=True).lower()
                    if op=='y':
                        UltiCharge=0
                        if WpName=='Popsicle Sword':
                            DeltaHP=22
                            nowHP=min(HP,nowHP+DeltaHP)
                            HUD()
                            cmd('color 0a')
                            msg('Your '+WpName+' tastes good.\nYou healed 22 HP.')
                        elif WpName=='Eyes of Vera':
                            DeltaEnemyHP=-nowEnemyHP
                            nowEnemyHP=0
                            HUD()
                            msg('Instant kill. Nice and clean.')
                            CheckEnemyDeath()
                        elif WpName=='Electric Clarinet':
                            msg('You play your '+WpName+'.\n'+EnemyName+\
                                ' seems to be enjoying the music.')
                            FUN=rand(1,100)
                            if FUN==100:
                                msg('sans is selling tickets.')
                            del FUN
                            DeltaHP=HP-nowHP
                            DeltaEnemyHP=EnemyHP-nowEnemyHP
                            nowHP+=DeltaHP
                            nowEnemyHP+=DeltaEnemyHP
                            HUD()
                            cmd('color 0a')
                            msg('Everyone is fully healed!')
                        elif WpName=='Doctor\'s Spoon':
                            attack(NoMiss=True)
                            DeltaHP=-DeltaEnemyHP
                            nowHP=min(HP,nowHP+DeltaHP)
                            HUD()
                            msg(EnemyName+' tastes good.')
                            CheckEnemyDeath()
                        elif WpName=='Frisk\'s Stick':
                            msg('You throw away '+WpName+'...')
                            msg(EnemyName+' catches '+WpName+' and...')
                            msg('teleports it back to your hands.')
                            EnemyName='Dog'
                            status='A doggy.'
                            HUD()
                            msg('The enemy finally understands the pleasure of being a dog.'+\
                                '\nThey decide to be a Dog.')
                        elif WpName=='P.Y.T.H.O.N.':
                            msg('...')
                            msg('......')
                            msg(WpName+' starts to tremble in your hands!')
                            msg('Behold!\n'+WpName+' is activating!')
                            cmd('start python')
                            msg('A new Python window is launched!')
                            cls()
                            HUD()
                            msg('bamboozled'.upper(),DoWait=False)
                            print('Press Space to continue...',end='',flush=True)
                            op=''
                            while op!=' ':
                                op=listen()
                                cmd('color '+hex(rand(0,15))[-1]+hex(rand(0,15))[-1])
                                sleep(.6)
                            print()#fix end='' aftermathh
                            cmd('color 0f')
                        elif WpName=='Legendary Artifact':
                            msg('An Annoying Cat appears and absorbs your '+WpName+'...')
                            WpName='Annoying Cat'
                        elif WpName=='Blue Glowing Spear':
                            DeltaEnemyHP=int(nowEnemyHP/2)-nowEnemyHP
                            nowEnemyHP+=DeltaEnemyHP
                            HUD()
                            msg(EnemyName+'\'s HP is halved!',DoWait=False)
                            cmd('color b0')
                            sleep(.1)
                            cmd('color 0f')
                            wait()
                            CheckEnemyDeath()
                        elif WpName=='Offensive Mac Pro':
                            DeltaEnemyHP=-rand(1,int(EnemyHP*.9))
                            nowEnemyHP=max(0,nowEnemyHP+DeltaEnemyHP)
                            HUD()
                            msg('Your '+WpName+' attacked and dealt '+\
                                str(-DeltaEnemyHP)+' HP damage.')
                            CheckEnemyDeath()
                        elif WpName=='Very Sharp Ball':
                            msg('The '+WpName+' starts to spin at a very high speed!'+\
                                '\nIt is slashing everyone! Ouch!')
                            DeltaEnemyHP=-nowEnemyHP
                            nowEnemyHP=0
                            DeltaHP=1-nowHP
                            nowHP+=DeltaHP
                            HUD()
                            msg('Basically, this Ultimate Ability\nkills the enemy and leaves you with 1 HP.')
                            CheckEnemyDeath()
                        elif WpName=='Glove of Iron Man':
                            msg('You are propelled through the galaxies!')
                            msg(EnemyName+' is shook!')
                            msg(EnemyName+' cannot move!')
                            msg('(But of course,\n'+EnemyName+' couldn\'t have kept up with your speed anyway...)')
                            msg('In a word, fate has seperated you and the '+EnemyName+'.')
                            enemy=False
                            cls()
                            HUD()
                            msg('Now you get to choose which direction to travel\n'+\
                                '(at a very high speed).\n\n'+\
                                'Press \"d\" to be propelled 70 miles towards the Earth.\n'+\
                                'Press \"a\" to be propelled 70 miles away from the Earth.',DoWait=False)
                            op=''
                            while op not in ('d','a'):
                                op=listen(WaitUntilGet=True).lower()
                            if op=='d':
                                direction=1
                                destination=traveled+70
                            else:
                                direction=-1
                                destination=traveled-70
                            cmd('color 0b')
                            DeltaTraveled=70*direction
                            FastTravel(destination,direction)
                        elif WpName=='Space Cadillac':
                            EnemyHit-=5
                            msg('You start driving at incredible hihg speed\n '+\
                                EnemyName+'\'s Accuracy -5')
                        elif WpName=='Domestic Sandwich':
                            DeltaHP=int(.7*(HP-nowHP))
                            nowHP+=DeltaHP
                            HUD()
                            cmd('color 0a')
                            msg('70% of you wound is healed.')
                        elif WpName=='Annoying Cat':
                            msg(WpName+' sits on '+EnemyName+'\'s '+\
                                EnemyWp+' and won\'t let go!\n'+\
                                EnemyName+' becomes impatient!\nThey abandon their '+EnemyWp+\
                                '.\n'+EnemyName+' takes out the Holy Sickle from their pocket!')
                            EnemyWp='Holy Sickle'
                            EnemyATK+=20
                            status='The Holy Sickle finally appears.'
                        elif WpName=='Exotic Sandwich':
                            msg('You try your '+WpName+'...')
                            cmd('color 0a')
                            DeltaHP=HP
                            nowHP=HP
                            HUD()
                            msg('Whooaaa!\n\nYou feel alive.')
                        elif WpName=='Holy Sickle':
                            if ATK==100:
                                msg('The Holy Sickle cannot get any sharper.\n'+\
                                    'So it decides to open a worm hole.')
                                DeltaTraveled=100
                                FastTravel(traveled+100, 1)
                            else:
                                ATK+=1
                                HUD()
                                msg('The Holy Sickle shines with black light.\n\nATK +1')
                else:
                    msg(WpName+':\nUltimate not ready yet.\nCharge = '+\
                        str(UltiCharge)+' / '+str(UltiFullCharge))
        else:
            if 'm' == op:
                if nowHP<HP:
                    if rand(0,MeditateSafe)==0:
                        NewEnemy()
                    else:
                        DeltaHP=int(HP*Meditability)+1
                        nowHP=min(HP,nowHP+DeltaHP)
                        meditating=True
            elif 's' == op:
                NewEnemy()
            elif 'a' == op:
                DeltaTraveled=-1
                traveled=max(0,DeltaTraveled+traveled)
                walking=(walking-1)%4
                if rand(0,TravelSafe)==0:
                    NewEnemy()
            elif 'd'==op:
                DeltaTraveled=1
                traveled+=DeltaTraveled
                if traveled>HighScore:
                    HighScore=traveled
                    if not NewHighScore:
                        NewHighScore=True
                        msg('You just surpassed your personal record\nof how close you ever got to the Earth!')
                walking=(walking+1)%4
                if EarthDis==traveled:
                    win=True
                else:
                    if rand(0,TravelSafe)==0:
                        NewEnemy()
ClearSaveFile(ClearHighScore=True)
msg('You have reached the Earth!')
cls()
msg('Lv = '+str(Lv)+'\nCritical Hit Chance = '+format(critical,'.0%')+\
    '\nCritical Dmg Multiplier = '+str(criticalDMG)+\
    '\n\nYour final weapon: '+WpName+'\nATK = '+str(ATK))
cls()
msg('To the Earth\n\nA game by Daniel\n\nThank you for playing.')
