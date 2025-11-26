from os import system as terminal

input('You need admin access to install dependencies. Continue? ')
terminal('sudo python -m pip install cocos2d')
try:
    import cocos
    input('Success! Hit Enter to quit...')
except:
    terminal('sudo -H python -m pip install cocos2d')
    try:
        import cocos
        input('Success! Hit Enter to quit...')
    except:
        input('Fail! Hit Enter to quit...')
