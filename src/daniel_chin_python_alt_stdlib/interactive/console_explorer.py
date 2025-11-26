'''
An android-friendly console file explorer. 
'''
from os import path
import os
from .cls import cls

def isAndroid():
    return 'ANDROID_DATA' in os.environ

class AbortionError:
    pass

class File:
    def __init__(self, name = None):
        self.name = name
    
    def __str__(self):
        return self.name

class Dir:
    def __init__(self, name = None):
        self.name = name
    
    def __str__(self):
        return self.name

class Parent:
    name = '..'

class Track:
    def __init__(self, _path):
        self.list = [Parent()]
        self.selected = 0
        for i in os.listdir(_path):
            if path.isdir(path.join(_path, i)):
                self.list.append(Dir(i))
            elif path.isfile(path.join(_path, i)):
                self.list.append(File(i))
            else:
                assert False, 'An item is neither file nor dir! '
        self._hide_next_print = False
    
    def select(self, i):
        self.selected = i
    
    def up(self):
        self.selected = (self.selected - 1) % len(self.list)

    def down(self):
        self.selected = (self.selected + 1) % len(self.list)
    
    def print(self):
        if self._hide_next_print:
            self._hide_next_print = False
            return
        form = str(len(str(len(self.list))))
        for i, item in enumerate(self.list):
            if i == self.selected:
                print('@ ', end = '')
            else:
                print('  ', end = '')
            print(format(i, form), end = '')
            if type(item) is Parent:
                print('..')
            elif type(item) is Dir:
                print('+', item.name)
            elif type(item) is File:
                print('-', item.name)
            else:
                assert False
    
    def hideNextPrint():
        self._hide_next_print = True

def askForFile(cd = None):
    if cd is None:
        if isAndroid():
            cd = '/sdcard/' 
        else:
            cd = os.getcwd()
    stop = False
    track = Track(cd)
    while not stop:
        print('='*10)
        track.print()
        print()
        print('Now selected:', track.list[track.selected].name)
        op = input(cd + '>').lower()
        if op == '':
            track.down()
        elif op == 'e':
            item = track.list[track.selected]
            if type(item) in (Parent, Dir):
                cd = path.abspath(path.join(cd, item.name))
                track = Track(cd)
            elif type(item) is File:
                return path.join(cd, item.name)
            else:
                assert False
        elif op == 's':
            kw = input('keyword: ')
            matches = [x for x in track.list if kw.lower() in x.name.lower()]
            choosed = chooseFromEntries(matches)
            if choosed is not None:
                track.selected = track.list.index(choosed)
        elif op == 'cls':
            cls()
        elif op == 'abs':
            new_cd = input('Abs path: ')
            if path.isdir(new_cd):
                cd = new_cd
                track = Track(cd)
            else:
                print('Not a dir. ')
        elif op == 'help':
            print('Enter to next')
            print('"e" to enter')
            print('"s" to search')
            print('num to id')
            print('"abort", "abs", "cls"')
        elif op == 'abort':
            raise AbortionError
        else:
            try:
                id = int(op)
                if id in range(len(track.list)):
                    track.selected = id
            except:
                print('No such command. ')

def askSaveWhere(cd = None, initialfile = None):
    if cd is None:
        if isAndroid():
            cd = '/sdcard/download/' 
        else:
            cd = os.getcwd()
    stop = False
    track = Track(cd)
    while not stop:
        print('='*10)
        track.print()
        print()
        print('Now selected:', track.list[track.selected].name)
        op = input(cd + '>').lower()
        if op == '':
            track.down()
        elif op == 'e':
            item = track.list[track.selected]
            if type(item) in (Parent, Dir):
                cd = path.abspath(path.join(cd, item.name))
                track = Track(cd)
            elif type(item) is File:
                print('It is a file, not a dir. ')
            else:
                assert False
        elif op == 'this':
            filename = None
            if initialfile is not None:
                print('Do you want to use', initialfile, 'as filename?')
                op = input('y/n >').lower()
                if op == 'y':
                    filename = initialfile
            if filename is None:
                filename = input('Save as filename: ')
            return path.join(cd, filename)
        elif op == 's':
            kw = input('keyword: ')
            matches = [x for x in track.list if kw.lower() in x.name.lower()]
            choosed = chooseFromEntries(matches)
            if choosed is not None:
                track.selected = track.list.index(choosed)
        elif op == 'cls':
            cls()
        elif op == 'abs':
            new_cd = input('Abs path: ')
            if path.isdir(new_cd):
                cd = new_cd
                track = Track(cd)
            else:
                print('Not a dir. ')
        elif op == 'help':
            print('Enter to next')
            print('"e" to enter')
            print('"this" to return cd')
            print('"s" to search')
            print('num to id')
            print('"abort", "abs", "cls"')
        elif op == 'abort':
            raise AbortionError
        else:
            try:
                id = int(op)
                if id in range(len(track.list)):
                    track.selected = id
            except:
                print('No such command. ')

def chooseFromEntries(entries):
    if not entries:
        print('No match! ')
        return None
    digit_len = len(str(len(entries)))
    [print(format(i, str(digit_len)), x) for i, x in enumerate(entries)]
    op = input('type ID or search with keyword >').lower()
    if op.isnumeric():
        try:
            return entries[int(op)]
        except IndexError:
            print('Invalid ID')
            return None
    filtered = [x for x in entries if op in str(x).lower()]
    if len(filtered) == 0:
        print('No match. Try again. ')
        return chooseFromEntries(entries)
    if len(filtered) == 1:
        return filtered[0]
    return chooseFromEntries(filtered)

if __name__ == '__main__':
    print(askSaveWhere('a.jpg'))
    input('enter...')
