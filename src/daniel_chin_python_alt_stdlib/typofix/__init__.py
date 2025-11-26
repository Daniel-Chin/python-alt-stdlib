from typofix.keyboard import *
import pickle
from itertools import combinations_with_replacement, product
from colorama import Back, Fore, Style, init
init()
from graphic_terminal import clearLine
from interactive import inputChin, listen
from string import printable, ascii_letters
SYMBOLS = ''.join({*printable} - {*ascii_letters})
from os import path

PEEK_LEN = 30
MAX_N_ERROR = 8
LONGEST_TO_FIX = 16
CORRECT = 1
NOT_A_WORD = 2
TOO_LONG = 3

def packagePath(filename):
    return path.join(path.dirname(__file__), filename)

with open(packagePath('words.pickle'), 'rb') as f:
    all_words = pickle.load(f)
with open(packagePath('my_personal_dict_that_is_public_on_github.txt'), 'r') as f:
    for line in f:
        all_words.add(line.strip())

def fixNoSwap(word, addFix = None, score_offset = 0):
    len_word = len(word)
    guessed = [guess(x) for x in word]
    for score in range(1, min(int(len_word / 1.5) + 2, MAX_N_ERROR) + score_offset):
        for combination in combinations_with_replacement(range(len_word), score):
            char_scores = [0] * len_word
            for i_char in combination:
                char_scores[i_char] += 1
            if any([x >= 2 for x in char_scores]):
                continue
            for candidate in product(*[x[y] for x, y in zip(guessed, char_scores)]):
                candidate = ''.join(candidate)
                if candidate.lower() in all_words:
                    if addFix is None:
                        return candidate
                    else:
                        addFix(candidate)
    if addFix is None:
        return NOT_A_WORD

def fix(word, only_first = True, addFix = None):
    if word.lower() in all_words:
        return CORRECT
    if len(word) > LONGEST_TO_FIX:
        return TOO_LONG
    try:
        guess_no_swap = fixNoSwap(word, addFix)
        if only_first and guess_no_swap != NOT_A_WORD:
            return guess_no_swap
        for i in range(len(word) - 1):
            chars = [*word]
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
            swapped = ''.join(chars)
            if swapped.lower() in all_words:
                if only_first:
                    return swapped
                else:
                    addFix(swapped)
            guess_no_swap = fixNoSwap(swapped, addFix, -1)
            if only_first and guess_no_swap != NOT_A_WORD:
                return guess_no_swap
        if only_first:
            return NOT_A_WORD
    except ImprobableChar:
        return NOT_A_WORD

def fixIO(inFile, outFile, interactive = False):
    word = ''
    buffer = [''] * PEEK_LEN
    if interactive:
        def write(s):
            outFile.write(s)
            for char in s:
                buffer.append(char)
                buffer.pop(0)
    else:
        write = outFile.write
    try:
        while True:
            read = inFile.read(1)
            if read in ALL_CHARS:
                word += read
            elif read == '=':
                if word == '' or word.lower() in all_words:
                    write(word)
                    write('=')
                else:
                    word = word[:-1]
            else:
                if word:
                    write(fixMultiTail(word, interactive, buffer, inFile, read))
                    word = ''
                write(read)
                if read == '':
                    break
    except CloseOutputNow:
        return

class CloseOutputNow(Exception):
    pass

def fixMultiTail(word, interactive, buffer, inFile, following):
    fixes = []
    def addFix(fixed):
        fixed += right
        if fixed in fixes:
            return
        fixes.append(fixed)
        clearLine()
        print(Fore.LIGHTCYAN_EX, end = '')
        print(len(fixes) - 1, ':', fixed)
        print(Fore.RESET, end = 'calculating...\r', flush = True)
    if word.lower() in all_words:
        return word
    else:
        if interactive:
            saved_pos = inFile.tell()
            print()
            print(''.join(buffer), Back.RED, word, Back.RESET, 
                following, inFile.read(PEEK_LEN), sep = '')
            inFile.seek(saved_pos)
            print()
    cursor = 0
    left = word
    right = ''
    for cursor in range(-1, -len(word) - 1, -1):
        if interactive:
            fixed = fix(left, False, addFix)
        else:
            fixed = fix(left)
        if fixed == CORRECT:
            return left + right
        if not interactive and fixed not in (TOO_LONG, NOT_A_WORD):
            return fixed + right
        if word[cursor] not in RIGHT_BORDER:
            break
        left = word[:cursor]
        right = ''.join([RIGHT_BORDER_MAP[x] for x in word[cursor:]])
    if not interactive:
        return word
    else:
        clearLine()
        print('A : Add to my personal dictionary that is public on Github')
        print('I : Ignore')
        print('M : Manually fix it')
        print('C : Close and save the file now')
        op = None
        while True:
            op = input('> ').upper()
            try:
                return fixes[int(op)]
            except (ValueError, IndexError):
                if op == 'A':
                    addToDict(word)
                    return word
                elif op == 'I':
                    return word
                    print('Ignored. ')
                elif op == 'M':
                    manual = inputChin(f'Let {word} be ' + Fore.CYAN, word, cursor = 0)
                    print(Fore.RESET, end = '')
                    manual_letters = manual.rstrip(SYMBOLS).lower()
                    if manual_letters not in all_words:
                        print('Add', Fore.CYAN, manual_letters, Fore.RESET, 'to my personal dictionary that is public on Github? y/n')
                        if listen('yn') == b'y':
                            addToDict(manual_letters)
                    else:
                        print(manual_letters, 'is already in the dictionary. ')
                    return manual
                elif op == 'C':
                    raise CloseOutputNow
                    print('Closing. ')
                else:
                    print('Choose one from above ', end = '')
                    continue
                break

def addToDict(word):
    with open(packagePath('my_personal_dict_that_is_public_on_github.txt'), 'a') as f:
        print(word, file = f)
    print('Added. ')

if __name__ == '__main__':
    print('(i)nteractive, or (a)utomatic, or (c)onsole?')
    op = listen('iac')
    if op in b'ia':
        with open('example.txt', 'r') as inp:
            with open('example.fix.txt', 'w') as outp:
                if op == b'i':
                    fixIO(inp, outp, interactive = True)
                else:
                    fixIO(inp, outp)
        print('Done! ')
    else:
        from console import console
        console(globals())
