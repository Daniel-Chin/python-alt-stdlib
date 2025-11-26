'''
morph a quad into another quad. It's like 3D projection.  
'''

import numpy as np
import cv2
from myfile import parseArgsOrInput
from jdt import jdtIter

def main():
    file_name = parseArgsOrInput()
    img = cv2.imread(file_name)
    img_h, img_w, _ = img.shape
    print("Enter the four coordinates of the quad's vertices.")
    A = getVertex('top left')
    B = getVertex('top right')
    C = getVertex('bottom left')
    D = getVertex('bottom right')
    AB = B - A
    CD = D - C
    CA = A - C
    DB = B - D
    width = max(np.abs(AB).sum(), np.abs(CD).sum())
    height = max(np.abs(CA).sum(), np.abs(DB).sum())
    canvas_size_w_h = np.max([A, B, C, D], axis=0) + np.array((1, 1))
    canvas = np.ones([canvas_size_w_h[1], canvas_size_w_h[0], 3], dtype=np.int8) * 255
    for i in jdtIter(np.linspace(0, 1, width)):
        for j in np.linspace(0, 1, height):
            S = AB * i + A
            T = CD * i + C
            ST = T - S
            O = ST * j + S
            canvas[
                round(O[1]), round(O[0]), :, 
            ] = img[
                round(j * (img_h - 1)), round(i * (img_w - 1)), :, 
            ]
    cv2.imwrite(file_name + '_2quad.png', canvas)

def getVertex(prompt):
    x = int(input(prompt + '.x = '))
    y = int(input(prompt + '.y = '))
    return np.array((x, y))

main()
