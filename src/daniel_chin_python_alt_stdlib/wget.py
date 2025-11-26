'''
Downloads a web resource. 
Provide no argument to enter interactive mode. 
'''

from urllib.request import urlopen
import sys
import os
from os import path
from pathlib import Path
import unicodedata, re
from interactive import listen
from urllib.parse import urlsplit
import platform
if platform.system() == 'Windows':
    DEFAULT = 'D:/downloads/'
else:
    DEFAULT = '/sdcard/download/'

def main():
    if path.samefile(os.getcwd(), str(Path.home())):
        os.chdir(DEFAULT)
    if len(sys.argv) >= 2:
        url = sys.argv[1]
        if len(sys.argv) == 3:
            filename = sys.argv[2]
        else:
            filename = None
        wget(url, filename)
    else:
        from console import console
        console(globals())

def wget(url, filename = None):
    if filename is None:
        filename = guessFilename(url)
    if path.isfile(filename):
        print(filename, 'already exists. Overwrite? ')
        if listen('yn') != b'y':
            print('canceled. ')
            return
    print('Downloading...')
    try:
        response = urlopen(url)
    except ValueError:
        response = urlopen('https://' + url)
    with open(filename, 'wb+') as f:
        f.write(response.read())
    print('Downloaded to', filename)

def guessFilename(url):
    scheme, _, remote_path, _, _ = urlsplit(url)
    if not scheme:
        url = 'https://' + url
    scheme, _, remote_path, _, _ = urlsplit(url)
    filename = path.basename(remote_path.strip('/')) or 'index.html'
    if '.' not in filename:
        filename += '.html'
    # Code copied from django:  https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    filename = unicodedata.normalize('NFKD', filename)
    filename = re.sub('[^\w\s.-]', '', filename).strip()
    filename = re.sub('[-\s]+', '-', filename)
    return filename

if __name__ == '__main__':
    main()
    sys.exit(0)
