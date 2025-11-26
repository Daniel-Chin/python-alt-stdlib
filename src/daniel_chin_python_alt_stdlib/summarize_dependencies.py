'''
Examines a directory of .py files and find all imports.  
'''
import os
from os import path
from indentprinter import indentPrinter, print
from pprint import pprint

def main():
    summary = set()
    warnings = []
    examineDir(summary, warnings)
    pprint(summary)
    pprint(warnings)

def examineDir(summary, warnings):
    for i in os.listdir():
        if i in '.git __pycache__':
            continue
        if path.isdir(i):
            print(i)
            with indentPrinter:
                os.chdir(i)
                examineDir(summary, warnings)
                os.chdir('..')
        else:
            if i[-3:].lower() in '.py .pyw':
                examineFile(i, summary, warnings)
            else:
                print('ignore', i)

def examineFile(filename, summary, warnings):
    with open(filename, 'r') as f:
        try:
            for line in f:
                if 'import' in line:
                    try:
                        if 'from' in line:
                            parts = line.split('from ')
                            assert parts[0].strip() == ''
                            assert len(parts) == 2
                            parts = parts[1].split(' import ')
                            assert len(parts) == 2
                            name = parts[0]
                        else:
                            parts = line.split('import ')
                            assert len(parts) == 2
                            name = parts[1].split(' as ')[0]
                        name = name.strip()
                        if name[0] == '.':
                            pass
                        else:
                            summary.add(name)
                    except AssertionError:
                        warnings.append((filename, line))
        except UnicodeDecodeError: 
            warnings.append((filename, 'UNICODE Error'))

main()
