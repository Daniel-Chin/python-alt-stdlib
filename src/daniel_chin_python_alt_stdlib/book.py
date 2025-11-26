'''
A file system.  
Encrypts the file system with Fernet.  
'''
print('Importing...')
import os
from base64 import urlsafe_b64encode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken
import platform
from io import BytesIO
from math import sqrt
import pickle
from os import system, listdir, urandom
from time import time
import interactive
from interactive import listen
interactive.msvcrt = None
from friendly_time import friendlyTime 
from getpass import getpass
import random
import string
import sys
from subprocess import run

if platform.system() == 'Windows':
    CLS_COMMAND = 'cls'
else:
    CLS_COMMAND = 'reset'
if platform.system() == 'Linux':
    PATH = '/sdcard/Daniel/book/'
else:
    PATH = ''
SALT_LEN = 16
KEY_LEN = 32
HASH_ITER = 100_000

print('Loading classes and functions...')

def main():
    print('MAIN')
    filename = loadFilename()
    password = getpass('?' * 666 + ' ')
    cls()
    book = Book()
    try:
        book._readFile(filename, password)
    except WrongPassword:
        print('Wrong password. ')
        return
    try:
        book._mainloop()
    except EOFError:
        pass
    finally:
        if book.unsaved_change:
            print('Type "save" to SAVE. ')
            print('Type "discard" to NOT save. ')
            op = ''
            while op not in ('save', 'discard'):
                op = input('I choose to ')
            if op == 'save':
                book.save()
                input('Press Enter... ')
            elif op == 'discard':
                print('It is NOT saved. ')
                input('Press Enter... ')
    cls()
    print('Beepher book ends. ')

def cls():
    system(CLS_COMMAND)

def loadFilename():
    if len(sys.argv) >= 2:
        return PATH + sys.argv[1]
    else:
        while True:
            print()
            print('o: open an existing book.')
            print('n: create a new book.')
            print('o/n >', end='', flush=True)
            op = input().lower().strip()
            if op in [*'on']:
                break
        if op == 'n':
            return newBook()
        if platform.system() == 'Linux':
            list_dir = [x.lower() for x in listdir(PATH)]
            [print(name) for name in list_dir]
            filename = input('filename=').lower()
            _, ext = os.path.splitext(filename)
            if ext.lower() != 'book':
                filename += '.book'
            assert filename in list_dir, 'No such file. '
            return os.path.join(PATH, filename)
        else:
            return input('path\\filename.beeph: ')

class Entry:
    def __init__(self):
        self.time = 0
        self.content = ''
    
    def copy(self):
        entry = Entry()
        entry.time = self.time
        entry.content = self.content
        return entry

class Book:
    '''
    All public methods can be called by user thru input(). 
    '''
    def __init__(self):
        self.unsaved_change = False
        self.now = None
        self.dict = {}
    
    def _readFile(self, filename, password):
        self.filename = filename
        print('Reading file...', end = '\r', flush = True)
        with open(filename, 'rb') as f:
            self.salt = f.read(SALT_LEN)
            assert len(self.salt) == SALT_LEN
            crypt = f.read()
        print('File loaded.   ')
        self.fernet = self._getFernet(password, self.salt)
        print('Decrypting...', end = '\r', flush = True)
        try:
            data = self.fernet.decrypt(crypt)
        except InvalidToken:
            raise WrongPassword
        print('Decryption success. ')
        print('Unpickling...', end = '\r', flush = True)
        pickleIO = BytesIO()
        pickleIO.write(data)
        pickleIO.seek(0)
        try:
            self.dict = pickle.load(pickleIO)
        except:
            raise WrongPassword
        print('Unpickling done.')
        print('Entry count:', len(self.dict))
    
    def _getFernet(self, password, salt):
        print('Deriving key...', end = '\r', flush = True)
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(), 
            length = KEY_LEN, 
            salt = salt, 
            iterations = HASH_ITER, 
            backend = default_backend(), 
        )
        key = urlsafe_b64encode(kdf.derive(password.encode()))
        print('Key derived.   ')
        return Fernet(key)
    
    def _mainloop(self):
        while True:
            print()
            if self._smartEntryCheck():
                print('Now operating:', self.now)
            op = input(">> ")
            methods = self.help(do_print = False)
            name = op.split(' ')[0]
            try:
                method = methods[name]
                try:
                    method(*op.split(' ')[1:])
                except TypeError:
                    help(method)
                    print('Oops. You gave wrong params. ')
                continue
            except KeyError:
                pass
            if op == '':
                self.cls()
            elif op == 'exit':
                break
            else:
                self.silentSearch(op, loud = True)
                if self.now is not None:
                    self.show()
    
    def help(self, do_print = True):
        methods = {}
        for name in dir(self):
            attr = getattr(self, name)
            if name[0] != '_' and callable(attr):
                methods[name] = attr
        if do_print:
            print('Commands: ')
            [print('>', name) for name in methods]
        return methods
    
    def cls(self):
        cls()
        print()
        self.isModified()
    
    def gen(self, *args):
        print(gen(*args))
        input('Enter... ')
        cls()
    
    def genDigit(self, *args):
        print(genDigit(*args))
        input('Enter... ')
        cls()
    
    def genLegacy(self, *args):
        print(genLegacy(*args))
        input('Enter... ')
        cls()
    
    def isModified(self):
        if self.unsaved_change:
            print('Book is MODIFIED! ')
        else:
            print('Book is not modified.')
    
    def _smartEntryCheck(self):
        if self.now is None:
            print("No entry selected. ")
            return False
        else:
            return True
    
    def new(self, entry_name = None):
        if entry_name is None:
            print('Entry name: ')
            entry_name = input('|: ')
        if self.__isValidEntryName(entry_name):
            self.dict[entry_name] = Entry()
            print('Content: ')
            self.dict[entry_name].content = multilineInput()
            cls()
            self.dict[entry_name].time = time()
            self.now = entry_name
            print('Entry established. ')
            self.unsaved_change = True
    
    def __isValidEntryName(self, entry_name):
        if entry_name == '':
            msg = 'Error: Entry name cannot be blank. '
        elif entry_name in self.dict:
            msg = 'Error: Entry ' + entry_name + ' already exists. '
        elif entry_name in self.help(do_print = False):
            msg = 'Error: Reserved keyword: ' + entry_name
        else:
            return True
        print(msg)
        return False
    
    def show(self):
        if self._smartEntryCheck():
            buffer = '\n'
            buffer += '|: ' + self.now + '\n'
            buffer += 'last modified at ' + friendlyTime(
                self.dict[self.now].time) + '\n'
            buffer += self.dict[self.now].content + '\n'
            run('less', input = buffer.encode())
    
    def list(self):
        print('Enter to list by name, "t" to list by time. >')
        if listen((b't', b'\r')) == b't':
            sortedDict = self.__sort('last modified')
        else:
            sortedDict = self.dict
        page_pos=0
        for key, entry in sortedDict.items():
            print(friendlyTime(entry.time), '|:', key)
            page_pos += 1
            if page_pos == 20:
                page_pos = 0
                if input('Enter to show more... ') != '':
                    break
    
    def __sort(self, sort_by):
        assert sort_by == 'last modified'
        keys = list(self.dict)
        entrys = []
        for i in keys:
            entrys.append(self.dict[i])
        for i in range(len(keys)-1, 0, -1):
            for k in range(i):
                if entrys[k].time < entrys[k+1].time:
                    entrys[k+1],entrys[k] = entrys[k],entrys[k+1]
                    keys[k],keys[k+1] = keys[k+1],keys[k]
        return dict(zip(keys, entrys))
    
    def silentSearch(self, keyword = None, loud = False):
        if keyword is None:
            keyword = input('Keyword: ').lower()
        matches = [x for x in self.dict.keys() if keyword in x.lower()]
        try:
            if not loud:
                raise ValueError
            i = [x.lower() for x in matches].index(keyword)
            self.now = matches[i]
        except ValueError:
            self.now = chooseFromEntries(matches)
    
    def save(self):
        pickleIO = BytesIO()
        pickle.dump(self.dict, pickleIO)
        pickleIO.seek(0)
        data = pickleIO.read()
        crypt = self.fernet.encrypt(data)
        with open(self.filename, 'wb') as f:
            f.write(self.salt)
            f.write(crypt)
        self.unsaved_change = False
        print('Saved. ')
    
    def rename(self, new_name = None):
        if self._smartEntryCheck():
            if new_name is None:
                new_name = input('|: ')
            if self.__isValidEntryName(new_name):
                self.dict[new_name] = self.dict.pop(self.now)
                self.now = new_name
                self.unsaved_change = True
    
    def delete(self):
        if self._smartEntryCheck():
            print('Really delete:', self.now, '?')
            print('Type entry name to confirm deletion. ')
            if input('I delete: ') == self.now:
                self.dict.pop(self.now)
                print('Entry', self.now, 'deleted! ')
                self.now = None
                self.unsaved_change = True
            else:
                print('Did NOT delete. ')
    
    def copy(self, new_entry_name = None):
        if self._smartEntryCheck():
            print('Copy to? ')
            if new_entry_name is None:
                new_entry_name = input('|: ')
            if not self.__isValidEntryName(new_entry_name):
                print('Did not copy. ')
            else:
                self.dict[new_entry_name] = self.dict[self.now].copy()
                print('Copied', self.now, 'to', new_entry_name, '. ')
                self.unsaved_change=True
    
    def searchByContent(self, keyword = None):
        if keyword is None:
            keyword = input('keyword: ')
        matches = []
        for name, entry in self.dict.items():
            if keyword.lower() in entry.content.lower():
                matches.append(name)
        self.now = chooseFromEntries(matches)
        if self.now is not None:
            self.show()
    
    def edit(self):
        if self._smartEntryCheck():
            print('"m" to modify current line. ')
            print('"i" to insert line before current line. ')
            print('"d" to delete current line. ')
            print('Enter (\\r) to navigate to the next line. ')
            print()
            print('|:', self.now)
            edited = []
            for line in self.dict[self.now].content.split('\n'):
                print(line + "> ", end='', flush=True)
                op = listen((b'm',b'i',b'd',b'\r',b'\n'))
                if op == b'm':
                    print('\r', ' '*len(line), '\r', end='', flush = True)
                    edited.append(inputWithGen())
                elif op == b'i':
                    print('\r', ' '*len(line), '\r', end='')
                    edited.append(multilineInput())
                    edited.append(line)
                    print(line)
                elif op==b'd':
                    print("\r---Line deleted---", ' '*len(line))
                elif op in b'\r\n':
                    edited.append(line)
                    print()
            cls()
            edited = '\n'.join(edited)
            print('Old version: ')
            print(self.dict[self.now].content)
            print()
            print('New version: ')
            print(edited)
            print('Save? "y" to save, "n" to discard. >', end = '', flush = True)
            op = listen((b'y', b'n'))
            if op == b'y':
                self.dict[self.now].content = edited
                self.dict[self.now].time = time()
                cls()
                print('Entry edited. ')
                self.unsaved_change = True
            else:
                cls()
                print('Change discarded. ')
    
    def append(self):
        if self._smartEntryCheck():
            print('Append: ')
            to_append = multilineInput()
            cls()
            self.dict[self.now].content += '\n' + to_append
            self.dict[self.now].time = time()
            self.unsaved_change = True
            print('Append success. ')
    
    def changePass(self):
        print('Setting password.')
        try:
            mismatch = True
            password1 = getpass('New password:')
            password2 = getpass('Repeat:')
            assert password1 == password2
            password3 = getpass('Type in reverse:')
            assert password1 == ''.join(reversed(password3))
            mismatch = False
            print('Confirm to set new password?')
            assert listen(['y', 'n']) == b'y'
        except AssertionError:
            if mismatch:
                print('Password mismatch.')
            print('Abort. Did not set new password.')
            return False
        self.salt = urandom(SALT_LEN)
        self.fernet = self._getFernet(password1, self.salt)
        self.unsaved_change = True
        print('Password loaded. ')
        return True

def chooseFromEntries(matches):
    if len(matches)==1:
        return matches[0]
    elif matches==[]:
        print("No match. ")
        return None
    else:
        print("Multiple matches: ")
        no=0
        for i in matches:
            print(no,": ",i)
            no+=1
        print("Type entry ID to select. Enter to abort search. ")
        try:
            return matches[int(input("Entry ID: "))]
        except:
            print("Search aborted. ")
            return None

def multilineInput():
    buffer = []
    content = inputWithGen()
    while content != '':
        buffer.append(content)
        content = inputWithGen()
    return '\n'.join(buffer)

def genLegacy(length = 10, population = 'ascii'):
    length = int(length)
    if population == 'ascii':
        population = [*string.ascii_letters, *string.digits, '-']
        def isValid(word):
            has_lower = False
            has_upper = False
            has_num = False
            has_sym = False
            for char in word:
                has_lower |= char.islower()
                has_upper |= char.isupper()
                has_num |= char.isnumeric()
                has_sym |= char == '-'
            return has_lower and has_upper and has_num and has_sym
    elif population == 'digit':
        population = [*string.digits]
        isValid = lambda _: True
    elif population == 'alphanumeric':
        population = [*string.ascii_letters, *string.digits]
        isValid = lambda _: True
    else:
        population = [*population]
        isValid = lambda _: True
    [population.remove(x) for x in '0O1Il' if x in population]
    for _ in range(64):
        candidate = ''.join([random.choices(population)[0] for _ in range(length)])
        if isValid(candidate):
            break
        else:
            candidate = 'FAILED'
    else:
        print('Failed to generate. Maybe length not long enough. ')
    return candidate

INITIALS = [*{
    *'BDPTGKMNZCSJQXFHLRYW', 'Zh', 'Ch', 'Sh', 
}]
FINALS = [*{
    'i', 'e', 'a', 'ei', 'ai', 'ou', 'ao', 'en', 'an', 'ong', 
    'eng', 'ang', 'ie', 'ia', 'iu', 'iao', 'in', 'ian', 
    'iong', 'ing', 'iang', 'u', 'uo', 'ua', 'ui', 'uai', 
    'un', 'uan', 'uang', 'v', 've', 'vn', 'vuan', 
}]
FINALS_JQXY = [
    x for x in FINALS if 
    not x.startswith('e') and 
    not x.startswith('a') and 
    not x.startswith('o') and 
    not x.startswith('v')
]
FINALS_W = [
    x for x in FINALS if 
    not x.startswith('i') and 
    (not x.startswith('u') or x == 'u')
]
def gen(n_char = 5):
    # the new gen, based on PinYin
    n_char = int(n_char)
    buffer = []
    ton = None
    for i in range(n_char):
        if i == 2:
            buffer.append('-')
        ini = random.sample(INITIALS, k=1)[0]
        if ini in 'JQXY':
            fin = random.sample(FINALS_JQXY, k=1)[0]
        elif ini == 'W':
            fin = random.sample(FINALS_W, k=1)[0]
        else:
            fin = random.sample(FINALS, k=1)[0]
        if ton == '3':
            ton = random.sample('124', k=1)[0]
        else:
            ton = random.sample('1234', k=1)[0]
        buffer.append(ini + fin + ton)
    return ''.join(buffer)

def genDigit(length = 6):
    length = int(length)
    return genLegacy(length, 'digit')

def inputWithGen(prompt = ''):
    op = input(prompt)
    if op.split(' ')[0] == 'gen':
        return gen(*op.split(' ')[1:])
    elif op.split(' ')[0] == 'genDigit':
        return genDigit(*op.split(' ')[1:])
    elif op.split(' ')[0] == 'genLegacy':
        return genLegacy(*op.split(' ')[1:])
    else:
        return op

def newBook():
    book = Book()
    assert book.changePass()
    while True:
        book.filename = input('path/file.ext = ')
        try:
            with open(book.filename, 'wb+') as f:
                f.write(b'test')
            break
        except EOFError:
            print('^Z received. Abort. ')
            return
        except Exception as e:
            print('Exception:', e)
            print("Let's try again. ")
            continue
    print('Saving the new book... ')
    book.save()
    return book.filename

class WrongPassword(Exception):
    pass

if __name__ == '__main__':
    main()
    sys.exit(0)
