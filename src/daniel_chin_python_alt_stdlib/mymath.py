'''
More math utils than just `import math`
'''
import math

def factorial(up, down = 0, optimize = True):
    '''
    When testing the runspeed, I found Python actually optimizes factorial(x) // factorial(y). 
    But when doing factorial(50000, 49000), my optimization is still faster, for unknown reasons. 
    '''
    if down == 0:
        return math.factorial(up)
    if not optimize:
        return math.factorial(up) // math.factorial(down)
    else:
        result = 1
        for i in range(down + 1, up + 1):
            result *= i
        return result

if __name__ == '__main__':
    from console import console
    console(globals())
