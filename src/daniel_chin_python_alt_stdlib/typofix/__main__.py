from typofix import *
from interactive import listen, multiLineInput
from myfile import sysArgvOrInput
from os.path import splitext
from io import StringIO
from console import console

def doIt(inFile, outFile):
    print('(i)nteractive, or (a)utomatic?')
    if listen('ia') == b'i':
        fixIO(inFile, outFile, interactive = True)
    else:
        fixIO(inFile, outFile)

print('open (f)ile, or paste (r)aw text? ')
if listen('fr') == b'f':
    filename = sysArgvOrInput()
    with open(filename, 'r') as inFile:
        base, ext = splitext(filename)
        base += '_fix'
        with open(base + ext, 'w') as outFile:
            doIt(inFile, outFile)
    print('done')
else:
    print('Please paste here and Ctrl + Z: ')
    inFile = StringIO()
    outFile = StringIO()
    raw = multiLineInput(inFile)
    inFile.seek(0)
    doIt(inFile, outFile)
    outFile.seek(0)
    print(outFile.read())
    console(globals())
