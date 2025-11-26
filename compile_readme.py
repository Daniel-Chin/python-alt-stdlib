'''
Iterate through all files in this repo
build a readme.md for Github. 
'''
SUPPRESS = [
    'reqirements.txt',
    'Archive/catch_eof/1.py',
    'Archive/hash_math/1.py', 
    'Archive/Magic.py', 
    'Beer on the Wall/Data/bamboozle.py', 
    'Beer on the Wall/Data/English.py', 
    'Beer on the Wall/Data/main.py', 
    'Beer on the Wall/Data/Song.py', 
    'Beer on the Wall/Data/Sound.py', 
    'Beer on the Wall/Data/troll.py', 
    'Color_Tiles/Mac_Install.py', 
    'Color_Tiles/Mac_Launcher.py', 
    'Color_Tiles/Read_Me.txt',
    'Color_Tiles/Windows_Install.py', 
    'console/__main__.py', 
    'console_explorer.py', 
    'DanielSecureChat/daniel_secure_chat.py', 
    'Find Vera/CharFinder.py', 
    'Find Vera/Chars.txt', 
    'Find Vera/flush_test.py', 
    'interactive/cls.py', 
    'interactive/__main__.py', 
    'listen.py', 
    'resize_image.py', 
    'To the Earth/dev/Design.txt', 
    'To the Earth/dev/Draft-Ab.txt', 
    'To the Earth/dev/Draft.txt', 
    'To the Earth/dev/EditSave.py', 
    'To the Earth/dev/Weapons.txt', 
    'multi_term/another_term.py', 
    'multi_term/__main__.py', 
    'interactive/legacy/charGettor_demo.py', 
    'interactive/key_codes.py', 
    'tkinter_async/__main__.py',
    'tkinter_async/__init__.py',
    'dchin_log/demo.py', 
]

import sys
import os
from os import path
import urllib.parse

def main():
    os.chdir(path.dirname(path.abspath(__file__)))
    with open('README.md', 'w', encoding='utf-8') as out:
        with open('readme_head.md', 'r', encoding='utf-8') as f:
            out.write(f.read())
        
        print(file=out)
        print('## Environment', file=out)
        print('If you require this package, specify the correct extras yourself.  ', file=out)
        print(file=out)
        print('If you are me, run:  ', file=out)
        print('`' + command_to_sync_all_optionals() + '`  ', file=out)

        print(file=out)
        print('## Documentation', file=out)
        os.chdir('./src/daniel_chin_python_alt_stdlib')
        documentate('', out, depth = 1)
    input('Done. Enter...')

def command_to_sync_all_optionals():
    with open('./pyproject.toml', 'r') as f:
        for line in f:
            if line.strip() == '[project.optional-dependencies]':
                break
        optional_features = list[str]()
        for line in f:
            line = line.strip()
            if line == '' or line[0] == '[':
                break
            feature, _ = line.split(' = ', 1)
            optional_features.append(feature)
    buf = ['uv', 'sync']
    for feature in optional_features:
        buf.append('--extra')
        buf.append(feature)
    return ' '.join(buf)

def documentate(cd, out, depth, folder_documented = False):
    if depth >= 2:
        try:
            with open('readme.md', 'r', encoding='utf-8') as f:
                print('###', cd, file = out)
                doc = f.read().strip()
                if len(doc) < 3:
                    print('EMPTY README', cd)
                out.write(doc)
                out.write('\n\n')
                out.write(f'[source code folder](./src/daniel_chin_python_alt_stdlib/{urllib.parse.quote(cd)})')
                out.write('\n\n')
            folder_documented = True
        except:
            pass
    for node in sorted(os.listdir()):
        if path.isfile(node):
            ext = path.splitext(node)[-1]
            if ext in ('.py', '.txt', 'pyw'):
                # print('Processing', cd + node)
                with open(node, 'r', encoding='utf-8') as f:
                    documented = False
                    for line in f:
                        line = line.strip('\r\n')
                        if line == "'''":
                            documented = True
                            break
                        if line == '' or line[0] == '#' or line.startswith('from __future__ import'):
                            continue
                        break
                    if documented:
                        print('###', cd+node, file = out)
                        buffer = []
                        for line in f:
                            line = line.strip('\r\n')
                            if line == "'''":
                                break
                            buffer.append(line)
                        print(*buffer, file = out, end = '\n\n', sep = '  \n')
                        out.write(f'[source code](./src/daniel_chin_python_alt_stdlib/{urllib.parse.quote(cd + node)})')
                        out.write('\n\n')
                    else:
                        identifier = cd + node
                        if identifier not in SUPPRESS and not folder_documented:
                            print('No doc for file', identifier)
        else:   # isdir
            if node in ('.git', '__pycache__'):
                continue
            os.chdir(node)
            documentate(cd + node + '/', out, depth + 1, folder_documented)
            os.chdir('..')

main()
sys.exit(0)
