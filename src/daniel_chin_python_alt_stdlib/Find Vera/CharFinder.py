width=24
height=22
i=0
while i<40000:
    for h in range(height):
        print(i,end=' ')
        for w in range(width):
            print(chr(i),end='')
            i+=1
        print()
    input()
input('END')
