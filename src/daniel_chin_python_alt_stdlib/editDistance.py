'''
Uses dynamic programming (DP) to calculate the minimum editing distance.  
'''

import numpy as np

def editDistance(
    a, b, 
    insert_cost = 1, del_cost = 1, replace_cost = 1, 
):
    X = len(a) + 1
    Y = len(b) + 1
    mat = np.zeros((X, Y))
    mat[:, 0] = np.arange(X) * insert_cost
    mat[0, :] = np.arange(Y) * del_cost
    for x in range(len(a)):
        for y in range(len(b)):
            mat[x + 1][y + 1] = min(
                mat[x, y + 1] + insert_cost, 
                mat[x + 1, y] + del_cost, 
                mat[x, y] + (
                    0 if a[x] == b[y] else replace_cost
                ), 
            )
    return mat[-1][-1]

def test(a, b, do_swap = True):
    print(f'"{a}", "{b}" ->', editDistance(a, b))
    if do_swap:
        test(b, a, False)

if __name__ == '__main__':
    test('asd', 'rsd')
    test('asdf', 'asdf')
    test('asdf', 'assf')
    test('asdf', 'asf')
    test('banana', 'palace')
    test('banana palace', 'palace')
    test('cat', 'cut')
    test('saturday', 'sunday')
    test('1234567890', '23e45ty780')
    test('a', 'a')
    test('a', 's')
