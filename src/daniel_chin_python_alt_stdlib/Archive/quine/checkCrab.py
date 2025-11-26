from os import system

system('crab.py > crab.txt')
with open('crab.py', 'r') as f:
    src = f.read()
with open('crab.txt', 'r') as f:
    out = f.read()
rout = ''.join([*reversed(out)])
if src != rout:
    print(repr(src))
    print(repr(rout))
input('Enter...')
