'''
Preview a pickle file
'''
import sys, pickle
from pprint import pprint

def main():
    with open(sys.argv[1],'rb') as f:
        data=pickle.load(f)
    pprint(data)
    print()
    input('Enter...')

main()
sys.exit(0)
