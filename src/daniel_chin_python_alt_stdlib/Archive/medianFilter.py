from time import sleep
from itertools import count
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

LECUN = "C:\\Users\\iGlop\\d\\archive\\__theUnsorted\\LecunSwitch\\Lecun.png"

def medianFilter(img: np.ndarray):
    w, h = img.shape
    canvas = img[:]
    for x in range(w):
        for y in range(h):
            neighbors = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    # if dx == 0 and dy == 0:
                    #     continue
                    try:
                        c = img[x + dx, y + dy]
                    except IndexError:
                        continue
                    neighbors.append(c)
            neighbors.sort()
            canvas[x, y] = neighbors[len(neighbors) // 2]
    return canvas

def main():
    # lecun = mpimg.imread(LECUN)
    # lecun = np.sum(lecun[:, :, :3], axis=2)
    # lecun = lecun[::3, ::3]
    # img = lecun
    SIZE = 256
    img = np.random.rand(SIZE, SIZE)
    for i in count():
        print(i)
        plt.imshow(img, vmin=0, vmax=1)
        plt.draw()
        plt.pause(.1)
        if i >= 1:
            img = medianFilter(img)

main()
