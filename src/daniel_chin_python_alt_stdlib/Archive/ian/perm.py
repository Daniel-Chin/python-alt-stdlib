def perm(remain, already = [], root = []):
    if remain:
        for x in remain.copy():
            remain.remove(x)
            perm(remain, already + [x], root)
            remain.add(x)
    else:
        root.append(already)
    return root

if __name__ == '__main__':
    print(perm({1, 2, 3}))
    input('Enter...')
