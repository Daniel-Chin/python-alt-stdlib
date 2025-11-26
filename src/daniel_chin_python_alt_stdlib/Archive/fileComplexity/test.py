from time import perf_counter_ns
from math import log
from matplotlib import pyplot as plt
from shared import N

def main():
    x = []
    y = []
    for j in range(6):
        for i in range(N):
            size = 2 ** i
            start = perf_counter_ns()
            with open(f'{i}.data', 'rb+') as f:
                f.seek(size - 1)
                f.write(b'o')
                f.seek(size - 1)
                f.write(b'k')
            end = perf_counter_ns()
            dt = end - start
            x.append(i)
            y.append(log(dt))
            print(x[-1], dt)
    plt.plot(x, y, 'o')
    plt.show()

main()
