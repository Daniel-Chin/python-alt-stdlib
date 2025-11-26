'''
Print the headings of a markdown file.  
'''

from myfile import parseArgsOrInput

def main():
    filename = parseArgsOrInput()
    print()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                line = line.lstrip(' \t')
                line = line.rstrip('\r\n')
                i = 0
                while line[1] == '#':
                    line = line[1:]
                    i += 1
                print(' ' * i, line, sep='')
                # line = line.lstrip('#')
    print()

main()
