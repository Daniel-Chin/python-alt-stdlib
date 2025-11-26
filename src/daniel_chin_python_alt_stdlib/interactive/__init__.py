'''
Terminal interactivity utils.  

`listen`: waits for key press.  
`inputChin`: It does everything. There are too many features to describe. Reading the source code is the only way.  
`Universe`: `x in Universe()` always returns `True` no matter what `x` is.  
`inputUntilValid`: re-asks if not valid.  
`multiLineInput`: user may input multi lines. Terminate with ^Z.  

Demo:  
Define in `__main__.py`. Run it, or run the module.  

Issues:  
* On Linux, Stopping the job and bringing it back to foreground messes up the terminal setting up (?)  

Future work:  
    Stop telling lies in `help(getFullCh)` on Linux.  
    https://stackoverflow.com/questions/48039759/how-to-distinguish-between-escape-and-escape-sequence  
'''
__all__ = ['listen', 'strCommonStart', 'AbortionError', 
    'cls', 'askForFile', 'askSaveWhere', 'inputChin', 'multiLineInput', 
    'inputUntilValid', 
]

from .console_explorer import *
from .cls import cls
from colorama import init, Back, Fore, Style
init()
import string
from time import monotonic as monoTime, sleep
from sys import stdout
import platform

from ..terminalsize import get_terminal_size
from ..graphic_terminal import *

from .kbhit import KBHit
from . import key_codes as KEY_CODE

FPS = 30
CURSOR_WRAP = Back.GREEN + Fore.WHITE + '%s' + Style.RESET_ALL
if platform.system().lower() == 'windows':
    DISPLAY_WIN_Z_LINUX_D = '^Z'
else:
    DISPLAY_WIN_Z_LINUX_D = '^D'

if platform.system().lower() == 'windows':
    def getFullCh(priorize_esc_or_arrow = False):
        kbHit = KBHit()
        first = kbHit.getch()
        if first == b'\x1b':   # ESC
            if priorize_esc_or_arrow:
                full_ch = first
            else:
                full_ch = first + kbHit.getch()
        elif first[0] in range(1, 128): # regular
            full_ch = first
        else:   # \x00 \xe0 multi bytes scan code
            full_ch = first + kbHit.getch()
        kbHit.set_normal_term()
        return full_ch
else:
    def getFullCh(priorize_esc_or_arrow = False):
        '''
        Problem: 
            on Linux, function keys and arrow keys  
            scan code is multi bytes, starting with \x1b.  
            However, ESC scan code is single byte \x1b,  
            which means it is impossible to differentiate.  
            The caller of this function has to know in advance 
            whether the user is expected to press ESC or 
            arrow keys.  
            Set `priorize_esc_or_arrow` to True or False.  
        Solution:  
            Maybe let the user double press ESC!  
            Set `priorize_esc_or_arrow` to False  
            and check for b'\x1b\x1b'.  
        The parsing scheme of function keys is derived from testing.  
        Please open an issue if you have the spec of Linux scan codes.  
        '''
        kbHit = KBHit()
        ch = kbHit.getch()
        if ch == b'\x1b':
            if not priorize_esc_or_arrow:
                new = kbHit.getch()
                ch += new
                if new in b'[O': 
                    new = b''
                    while new in b';' + string.digits.encode():
                        new = kbHit.getch()
                        ch += new
                    assert new in b'~' + string.ascii_uppercase.encode()
                else:
                    pass    # alt + regular, and esc esc
        kbHit.set_normal_term()
        return ch

def tryGetch(timeout = None, priorize_esc_or_arrow = False):
    '''
    `timeout`: 0 is nonblocking, None is wait forever.  
    Return None if timeout.  
    '''
    if timeout is None:
        return getFullCh(priorize_esc_or_arrow)
    if timeout < 0:
        raise ValueError(f'timeout must > 0, got {timeout}')
    kbHit = KBHit()
    try:
        for _ in range(int(timeout * FPS) + 1):
            if kbHit.kbhit():
                return getFullCh(priorize_esc_or_arrow)
            sleep(1 / FPS)
    finally:
        kbHit.set_normal_term()
    return None

class Universe:
    def __contains__(self, x):
        return True

def listen(choice = set(), timeout = None, priorize_esc_or_arrow = False):
    '''
    `choice`:  
        can be an iterable of choices or a single choice.   
        Elements can be byte or string.  
        If empty, accepts anything.  
    `timeout`:  
        in seconds. None is blocking. 
    Supports non-windows.  
    The function returns bytes; None if timeout.  
    The user has to double press ESC, return b'\x1b' * 2  
    '''
    if choice:
        bChoice = set()
        for option in choice:
            if type(option) is str:
                option = option.encode()
            elif type(option) is int:
                option = bytes([option])
            if type(option) is not bytes:
                raise TypeError('`choice` argument type mismatch')
            bChoice.add(option)
    else:
        bChoice = Universe()
    
    stdout.flush()
    
    if timeout is not None:
        deadline = monoTime() + timeout
    while True:
        full_ch = tryGetch(
            timeout and max(0, deadline - monoTime()), 
            priorize_esc_or_arrow = priorize_esc_or_arrow, 
        )
        if full_ch == KEY_CODE.CTRL_C:
            raise KeyboardInterrupt
        if full_ch and full_ch in bChoice:
            return full_ch
        if timeout is not None and monoTime() > deadline:
            return None

def strCommonStart(list_strs, known_len = 0):
    '''
    Find the common start for a list of strings. 
    Useful for auto-complete for the user. 
    `known_len` is known length of common start - for performance. 
    '''
    columns = zip(* list_strs)
    i = -1  # in case one string is ''
    for i, column in enumerate(columns):
        if i >= known_len:
            shifted_column = iter(column)
            next(shifted_column)
            if not all(x == y for x, y in zip(column, shifted_column)):
                i -= 1
                break
    return list_strs[0][:i + 1]

def chooseFromEntries(matches):
    input('Warning: interactive/__init__/chooseFromEntries will be deprecated!!! Enter...')
    if len(matches)==1:
        return matches[0]
    elif matches==[]:
        print("No match. ")
        return None
    else:
        print("Multiple matches: ")
        no=0
        for i in matches:
            print(no,": ",i.name)
            no+=1
        print("Type entry ID to select. Enter to abort search. ")
        try:
            return matches[int(input("Entry ID: "))]
        except:
            print("Search aborted. ")
            return None

def printabilize(x):
    return x.replace(
        KEY_CODE.WIN_Z_LINUX_D.decode(), DISPLAY_WIN_Z_LINUX_D
    ).replace('\x12', '^R')

_abbr = '...'
ABBR = [*'...']
ABBR[0] = Back.MAGENTA + Fore.WHITE + ABBR[0]
ABBR[-1] += Style.RESET_ALL
ABBR_LEN = len(_abbr) + 1
def printWithCursor(prompt, line, cursor):
    if cursor == len(line):
        line += ' '
    chars, [cursor] = eastAsianStrSparse(line, [cursor])
    chars[cursor] = CURSOR_WRAP % chars[cursor]
    width = get_terminal_size()[0] - eastAsianStrLen(prompt) - 1
    offset = min(cursor - width // 2, len(chars) - width)
    if offset > 0:
        chars = chars[offset + ABBR_LEN:]
        if chars[0] == '':
            chars.pop(0)
        chars = ABBR + [' '] + chars
    offset = len(chars) - width
    if offset > 0:
        if chars[-offset] == '':
            offset += 1
        chars = chars[:-offset - ABBR_LEN]
        chars += [' '] + ABBR
    line = ''.join(chars)
    print(prompt, printabilize(line), end = '\r', flush = True, sep = '')

def inputChin(prompt = '', default = '', history = [], kernal = None, cursor = None):
    '''
    `kernal` for tab key auto complete.  
    '''
    default = str(default)
    line = default
    if cursor is None:
        cursor = len(line)
    history_selection = len(history)
    while True:
        printWithCursor(prompt, line, cursor)
        op = listen()
        last_len = len(line)
        if op in b'\r\n':
            clearLine()
            print(prompt + printabilize(line))
            if KEY_CODE.WIN_Z_LINUX_D.decode() in line:  # ^Z ^D
                raise EOFError(f'"{printabilize(line)}"')
            return line
        elif op == KEY_CODE.BACKSPACE:
            if cursor >= 1:
                line = line[:cursor - 1] + line[cursor:]
                cursor -= 1
        elif op == KEY_CODE.DEL:
            if cursor <= len(line):
                line = line[:cursor] + line[cursor + 1:]
        elif op == KEY_CODE.UP:
            history_selection -= 1
            if history_selection in range(len(history)):
                line = history[history_selection]
                cursor = len(line)
            else:
                history_selection += 1
        elif op == KEY_CODE.DOWN:
            history_selection += 1
            if history_selection in range(len(history)):
                line = history[history_selection]
                cursor = len(line)
            else:
                history_selection -= 1
        elif op == KEY_CODE.LEFT:
            cursor -= 1
            if cursor not in range(len(line) + 1):
                cursor += 1
        elif op == KEY_CODE.RIGHT:
            cursor += 1
            if cursor not in range(len(line) + 1):
                cursor -= 1
        elif op == KEY_CODE.HOME:
            cursor = 0
        elif op == KEY_CODE.END:
            cursor = len(line)
        elif op == KEY_CODE.CTRL_LEFT:
            cursor = wordStart(line, cursor)
        elif op == KEY_CODE.CTRL_RIGHT:
            cursor = wordEnd(line, cursor)
        elif op == KEY_CODE.CTRL_BACKSPACE:
            old_cursor = cursor
            cursor = wordStart(line, cursor)
            line = line[:cursor] + line[old_cursor:]
        elif op == KEY_CODE.CTRL_DELETE:
            old_cursor = cursor
            cursor = wordEnd(line, cursor)
            line = line[:old_cursor] + line[cursor:]
            cursor = old_cursor
        elif op == b'\t':
            # auto complete
            if kernal is not None:
                legal_prefix = string.ascii_letters + string.digits + '_'
                reversed_names = []
                name_end = cursor
                name_start = cursor - 1
                while True:
                    if name_start >= 0 and line[name_start] in legal_prefix:
                        name_start -= 1
                    else:
                        reversed_names.append(line[name_start + 1:name_end])
                        name_end = name_start
                        name_start -= 1
                        if name_start < 0 or line[name_end] != '.':
                            break
                keyword = reversed_names.pop(0)
                names = reversed(reversed_names)
                to_search = kernal.send('dir(%s)' % '.'.join(names)) or []
                if len(reversed_names) == 0:
                    # include builtins
                    to_search += dir(__builtins__)
                next(kernal)
                candidates = [x for x in to_search if x.startswith(keyword)]
                if len(candidates) >= 1:
                    if len(candidates) == 1:
                        to_become = candidates[0]
                    if len(candidates) > 1:
                        clearLine()
                        print('auto-complete: ', end = '')
                        [print(x, end = '\t') for x in candidates]
                        print()
                        to_become = strCommonStart(candidates, len(keyword))
                    to_insert = to_become[len(keyword):]
                    line = line[:cursor] + to_insert + line[cursor:]
                    cursor += len(to_insert)
        elif op == KEY_CODE.ESC:
            line = ''
            cursor = 0
        elif KEY_CODE.isInvalidToInputChin(op):
            pass
        else:   # typed char
            try:
                op_decode = op.decode('utf-8')
            except:
                op_decode = op.decode('gbk')
            line = line[:cursor] + op_decode + line[cursor:]
            # I used ANSI in a previous version. Still don't know why I did that  
            cursor += 1
        clearLine()

def wordStart(line, cursor):
    word_started = False
    i = cursor
    for i in range(cursor - 1, -1, -1):
        if line[i].isalpha():
            word_started = True
        else:
            if word_started:
                i += 1
                break
    return i

def wordEnd(line, cursor):
    word_started = False
    word_ended = False
    i = cursor
    for i in range(cursor, len(line)):
        if line[i].isalpha():
            if word_ended:
                break
            else:
                word_started = True
        else:
            if word_started:
                word_ended = True
    else:
        i = len(line)
    return i

def multiLineInput(toIO = None):
    '''
    Terminate input with ^Z (on Windows)
    '''
    if toIO is None:
        buffer = []
        def append(s):
            buffer.append(s)
    else:
        def append(s):
            toIO.write(s)
            toIO.write('\n')
    try:
        while True:
            append(input())
    except EOFError:
        if toIO is None:
            return '\n'.join(buffer)
        else:
            return toIO

def inputUntilValid(prompt, validator, case_sensitive = False, legalize = None):
    '''
    `validator` can be a function returning boolean, or an iter.  
    '''
    try:
        if not case_sensitive:
            validator = [x.lower() for x in validator]
        else:
            validator = {*validator}
        is_iter = True
        prompt += ' ' + '/'.join(validator) + ' > '
    except TypeError:
        is_iter = False
    while True:
        candidate = input(prompt)
        if platform.system().lower() != 'windows':
            print() # Linux input() does not break line
        if not case_sensitive:
            candidate = candidate.lower()
        if legalize is not None:
            try:
                candidate = legalize(candidate)
            except:
                continue
        if (is_iter and candidate in validator) or (not is_iter and validator(candidate)):
            return candidate
