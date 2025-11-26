'''
Sort files and pass them to imv.  
'''

import os
import argparse
import random

def main(is_random=False):
    files = os.popen(
        'ls -1t', 
    ).read().strip().split('\n')
    if is_random:
        random.shuffle(files)
    command = f'imv {" ".join(files)}'
    print(command)
    os.system(command)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r', '--random', 
        action='store_true', 
        help='Randomize the order of the files',
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parseArgs()
    main(is_random=args.random)
