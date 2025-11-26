def bs(sea, target):
    start = 0
    end = len(sea)
    while end > start:
        # print(start, end)
        cursor = start + round((end - start) * 0.382)
        if target == sea[cursor]:
            return cursor
        if target < sea[cursor]:
            end = cursor
        else:
            start = cursor + 1
    raise ValueError('binary search failed.')

TOP = 20
for i in range(TOP):
    print(bs(range(TOP), i))
