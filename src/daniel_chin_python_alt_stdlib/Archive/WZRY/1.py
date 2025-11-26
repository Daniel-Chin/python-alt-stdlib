from random import random

SIZE = 1000

def a(r = .55):
    acc = 35
    i = 0
    while acc != 0:
        i += 1
        if random() < r:
            acc -= 1
        else:
            acc += 1
    return i

for _ in range(10):
    print(sum([a(.55) for _ in range(SIZE)]) / SIZE)
