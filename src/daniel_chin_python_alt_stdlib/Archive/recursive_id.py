from time import sleep

thing = eval(input('>>> '))

while True:
    sleep(.2)
    print(thing)
    thing = id(thing)
