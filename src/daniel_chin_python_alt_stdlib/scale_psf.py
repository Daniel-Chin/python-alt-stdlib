'''
Scale a PSF font file.  
'''

import argparse
from subprocess import Popen, PIPE
import typing as tp
from functools import partial
from itertools import chain, repeat

from tqdm import tqdm
import numpy as np

def main(in_filename: str, out_filename: str, ratio: int):
    assert ratio >= 2
    with open(out_filename, 'wb') as outF:
        with Popen(['txt2psf'], stdin=PIPE, stdout=outF) as outP:
            with Popen(['psf2txt', in_filename], stdout=PIPE) as inP:
                def safeInterface():
                    def readLine():
                        line = inP.stdout.readline()
                        if line == b'' and inP.poll() is not None:
                            raise EOFError
                        return line.decode('utf-8').rstrip('\n')
                    
                    def writeLine(x: str):
                        outP.stdin.write(f'{x}\n'.encode('utf-8'))
                    
                    def forward(transform: tp.Callable[[str], str]):
                        writeLine(transform(readLine()))
                    
                    def forwardUntilNextPercent():
                        while True:
                            x = readLine()
                            writeLine(x)
                            if x == '%':
                                return
                    
                    return forward, forwardUntilNextPercent
                
                forward, forwardUntilNextPercent = safeInterface()
                
                def expectCondition(condition: tp.Callable[[str], bool], x: str):
                    assert condition(x)
                    return x
                
                def expect(expected: str, x: str):
                    return expectCondition(lambda y: y == expected, x)

                def reportTheRest():
                    def verbose(x: str):
                        print(x)
                        return x
                    while True:
                        try:
                            forward(verbose)
                        except EOFError:
                            break

                forward(partial(expect, '%PSF2'))

                old_meta = {}
                is_in_header = True
                def parseMeta(x: str):
                    nonlocal is_in_header
                    if x == '%':
                        is_in_header = False
                        return x
                    k, v = x.split(': ', 1)
                    old_meta[k] = int(v)
                    if k in ('Width', 'Height'):
                        v_ = str(int(v) * ratio)
                    else:
                        v_ = v
                    return ': '.join((k, v_))
                while is_in_header:
                    forward(parseMeta)
                
                old_width = old_meta['Width']
                def find(keyword: str, src: str, not_found: int):
                    try:
                        return src.index(keyword)
                    except ValueError:
                        return not_found
                def scale(x: str):
                    head_len = min(
                        find('-', x, +np.inf), 
                        find('#', x, +np.inf), 
                    )
                    head, beheaded = x[:head_len], x[head_len:]
                    body, tail = beheaded[:old_width], beheaded[old_width:]
                    new_body = []
                    for c in body:
                        if c == '-':
                            scaled = c * ratio
                        elif c == '#':
                            scaled = c * ratio
                        else:
                            print(f'{x = }')
                            print(f'{old_width = }')
                            print(f'{body = }')
                            raise ValueError(f'Unexpected character: "{c}"')
                        new_body.append(scaled)
                    new_beheaded = ''.join(chain(new_body, (tail, )))
                    new_first_line = head            + new_beheaded
                    new_extra_line = ' ' * len(head) + new_beheaded
                    return '\n'.join(chain(
                        (new_first_line, ), 
                        repeat(new_extra_line, ratio - 1), 
                    ))
                
                is_first = True
                for _ in tqdm(range(old_meta['Length'])):
                    if is_first:
                        is_first = False
                    else:
                        forwardUntilNextPercent()
                    forward(partial(expectCondition, lambda x: x.startswith('//')))
                    for _ in range(old_meta['Height']):
                        forward(scale)
                
                print('The following output is the tail of the input file that I did not parse:')
                print('>>>>>>')
                reportTheRest()
                print('<<<<<<')

                inP.stdout.close()
                inP.wait()
            outP.stdin.close()
            outP.wait()
    print('ok')

def parseArgs():
    parser = argparse.ArgumentParser(description='Scale a PSF font file.')
    parser.add_argument('in_filename', type=str, help='Input PSF font file.')
    parser.add_argument('out_filename', type=str, help='Output PSF font file.')
    parser.add_argument('ratio', type=int, help='Scale ratio.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    main(args.in_filename, args.out_filename, args.ratio)
