'''
Converts ipynb to py. 
Works even when Jupyter is not installed. 
'''
import json
from io import StringIO as IO
import sys
from os import path
from myfile import openAsciize

def convert(inIO):
    print('Parsing json into dict...')
    root = json.load(inIO)
    print('done')
    outIO = IO()
    print('extracting source code...')
    for i, cell in enumerate(root['cells']):
        print('#' * 5, 'cell', i, '#' * 5, file = outIO)
        if cell['cell_type'] != 'code':
            print('', *cell['source'], file = outIO, sep = '#')
        else:
            print(*cell['source'], file=outIO, sep = '')
    outIO.seek(0)
    print('done')
    return outIO

def main():
    if len(sys.argv) < 2:
        from console import console
        console({'convert': convert})
    else:
        in_filename = sys.argv[1]
        with openAsciize(in_filename, verbose = True) as inF:
            print('File opened:', in_filename)
            out_filename = path.splitext(in_filename)[0] + '.py'
            print('Will overwrite:', out_filename)
            if input('Ok? y/n ') == 'y':
                with open(out_filename, 'w') as outF:
                    outF.write(convert(inF).read())
                print('ok')
            else:
                print('canceled')

if __name__ == '__main__':
    main()
    sys.exit(0)
