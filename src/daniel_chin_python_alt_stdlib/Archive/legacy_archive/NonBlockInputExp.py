import msvcrt
a=b''
done=False
while not done:
    if msvcrt.kbhit():
        b=msvcrt.getch()
        if b==b'\r':
            done=True
        else:
            a+=b
input(a.decode())
