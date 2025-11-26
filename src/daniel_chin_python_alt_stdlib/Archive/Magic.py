def isMagic(square_2d):
    square_1d = square_2d[0] + square_2d[1] + square_2d[2]
    RULE = [
        [0, 1],
        [3, 1],
        [6, 1],  0 1 2
        [0, 3],  3 4 5
        [1, 3],  6 7 8
        [2, 3],
        [0, 4], 
        [2, 2]
    ]
    tally = []
    for rule in RULE:
        sum = 0
        for i in range(3):
            sum += square_1d[rule[0] + rule[1] * i]
        tally.append(sum)
    return min(tally) == max(tally)

print(isMagic([[4,9,2], [3,5,7], [8,1,6]]))
input()
