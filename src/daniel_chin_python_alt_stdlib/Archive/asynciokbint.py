from asyncio import *
from threading import Lock

async def f(name):
    l = Lock()
    l.acquire()
    print('go')
    try:
        # l.acquire(timeout=1)
        await sleep(1)
    except KeyboardInterrupt:
        print(name, 'interrupt')
    else:
        return name
    finally:
        print(name, 'finally')

async def main():
    a = Task(f('a'))
    b = Task(f('b'))
    await a, b
    return a.result(), b.result()

print(run(main()))
