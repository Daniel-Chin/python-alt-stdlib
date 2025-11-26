from os import system as cmd

cmd('py -m pip install cocos2d')
try:
    import cocos
    input('Success! Hit Enter to quit...')
except:
    input('Fail! Hit Enter to quit...')
