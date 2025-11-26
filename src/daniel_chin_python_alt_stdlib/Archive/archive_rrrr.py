'''
To archive http://rrrrthats5rs.com
'''
from requests import get
from os import chdir
from graphic_terminal import clearLine
from indentprinter import *
import re

def main():
    chdir('d:/rrrr/')
    print('getting the list of games...')
    with indentPrinter:
        response = get('http://www.rrrrthats5rs.com')
        if response.status_code == 200:
            print('Got response. ')
        else:
            print('Error', response.status_code)
            return
        with open('index.html', 'wb+') as f:
            f.write(response.content)
        games = [x.split('/"', 1)[0] for x in response.text.split('/games/')[1:]]
        print('all games:')
        with indentPrinter:
            [print(x) for x in games]
    oks = [getGame(x) for x in games].count(True)
    print('All is done.', oks, '/', len(games), 'success.')

def getGame(game):
    print('getting', game, '...')
    with indentPrinter:
        response = get('http://www.rrrrthats5rs.com/games/%s/' % game)
        if response.status_code == 200:
            print('Got response. ')
        else:
            print('Error', response.status_code)
            return
        with open('game_pages/%s.html' % game, 'wb+') as f:
            f.write(response.content)
        parts = response.text.split('embedSWF("')
        if len(parts) != 2:
            print('Error', 'cannot find swf address. splitted into', len(parts), 'parts.')
            return
        address = parts[1].split('"', 1)[0]
        print('swf address:', address)
        print('Getting swf...', end = '', flush = True)
        response = get('http://www.rrrrthats5rs.com' + address)
        clearLine()
        if response.status_code == 200:
            print('Got swf. ')
        else:
            print('Error', response.status_code)
            return
        with open('swfs/%s.swf' % game, 'wb+') as f:
            f.write(response.content)
    return True

main()
