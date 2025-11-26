def a(i):
    def b():
        print(i)
    return b

def c():
    l = []
    for i in range(4):
        l.append(a(i))
    return l

print([x() for x in c()])
input('enter...')
