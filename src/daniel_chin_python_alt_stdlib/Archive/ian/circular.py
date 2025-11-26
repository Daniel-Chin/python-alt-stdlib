def doesContain(circle, target, start, end):
    end = end % len(circle)
    if circle[start] < circle[end]:
        return circle[start] <= target < circle[end]
    else:
        return target < circle[end] or circle[start] <= target

def circularBS(circle, target):
    if circle[0] == target:
        return 0
    return helper(circle, target, 0, len(circle))

def helper(circle, target, start, end):
    if end - start <= 1:
        raise ValueError('Fail')
    cursor = round(0.382 * start + 0.618 * end)
    if circle[cursor] == target:
        return cursor
    if doesContain(circle, target, start, cursor):
        return helper(circle, target, start, cursor)
    else:
        return helper(circle, target, cursor, end)

def test():
    TOP = 20
    for i in range(TOP):
        nice = [*range(i)]
        for j in range(i):
            mess = nice[j:] + nice[:j]
            print(mess)
            for k in range(i):
                found = circularBS(mess, k)
                truth = (k - j) % i
                if truth != found:
                    print('Mismatch!', truth, found)
                    input('Enter...')
                print(found, '==', truth)
    try:
        circularBS([3,4,5,6,0,1,2], 4.5)
    except ValueError:
        print('Fail, which is good.')
    else:
        print('did not fail. bad')
    try:
        circularBS([3,4,5,6,0,1,2], 99)
    except ValueError:
        print('Fail, which is good.')
    else:
        print('did not fail. bad')

if __name__ == '__main__':
    test()
    input('Enter...')
