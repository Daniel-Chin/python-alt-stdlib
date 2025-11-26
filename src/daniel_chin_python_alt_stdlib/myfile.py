'''
Unreliable file utils
'''
import os
from os import path, listdir, rmdir, chdir, getcwd
from os.path import isfile, isdir
import argparse
import sys
from io import BytesIO
import hashlib

from .interactive import listen

def copy(src_name = None, dest_name = None):
    '''
    Copies only binary content, leaving meta data. 
    '''
    src_name = src_name or input('from: ')
    dest_name = dest_name or input('to: ')
    if isfile(dest_name):
        print('Destination file alreay exists. Overwrite? Y/N')
        if listen([b'y', b'n']) != b'y':
            print('Aborted. ')
            return
    with open(src_name, 'rb') as src:
        with open(dest_name, 'wb+') as dest:
            dest.write(src.read())
    print('Copied. ')

def eraseFile(filename, verbose = True):
    '''
    Fill file with zeros and erase. 
    '''
    filename = filename or input('file: ')
    assert isfile(filename), "Doesn't exist. "
    size = os.stat(filename).st_size
    with open(filename, 'wb') as f:
        f.write(bytearray(size))
    os.remove(filename)
    if verbose:
        print('Erased file. ')

def eraseDir(path, recursion_root = True):
    assert ' ' not in path, 'Dont use space in path!'
    if recursion_root:
        saved_cd = getcwd()
    chdir(path)
    ls = listdir()
    for i in ls:
        if isfile(i):
            eraseFile(i, verbose = False)
        elif isdir(i):
            eraseDir(i, recursion_root = False)
        else:
            input('ERROR: A thing is neither file nor dir!!! Enter to exit...')
            sys.exit(1)
    chdir('..')
    rmdir(path)
    if recursion_root:
        chdir(saved_cd)
        print('Erased dir. ')

def erase(thing):
    if isfile(thing):
        eraseFile(thing)
    elif isdir(thing):
        eraseDir(thing)
    else:
        assert False, thing + ' not file nor dir. '

def openAsciize(filename, verbose = False):
    '''Only supports 'rb'. '''
    if verbose:
        print('Asciizing file...')
    outIO = BytesIO()
    with open(filename, 'rb') as f:
        while True:
            byte = f.read(1)
            if byte == b'':
                break
            if byte[0] >= 128:
                outIO.write(b'?')
            else:
                outIO.write(byte)
    outIO.seek(0)
    if verbose:
        print('done')
    return outIO

def sysArgvOrInput(prompt = '(Drag file here)\npath/file.ext='):
    # deprecated! 
    if len(sys.argv) >= 2:
        return sys.argv[1]
    else:
        return input(prompt).strip('"')
del sysArgvOrInput

def parseArgsOrInput(
    prompt = '(Drag file here)\npath/file.ext=', 
    parser_description = '', 
):
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument(
        'filename', type=str, 
        nargs='?', default=None, 
    )
    args = parser.parse_args()
    if args.filename is None:
        return input(prompt).strip('"')
    else:
        return args.filename
sysArgvOrInput = parseArgsOrInput

def hashFile(filename, chunk = 65536):
    '''
    Uses MD5. Not secure! 
    '''
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            buffer = f.read(chunk)
            if len(buffer) == 0:
                break
            hasher.update(buffer)
    return hasher.hexdigest()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'erase':
            target = sys.argv[2]
        else:
            target = sys.argv[1]
        print('Erase %s? y/n ' % target)
        if listen(['y', 'n']) == b'y':
            erase(target)
            sys.exit(0)
        print('Opening console. You can access sys.argv')
    from console import console
    console(globals())
