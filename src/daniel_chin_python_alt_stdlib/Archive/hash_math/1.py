from mymath import factorial

# f >> i >> 1
def phc(f, i, c):
    F = f * c
    I = i * c
    globa = factorial(F, F - I) / F ** I
    parti = (factorial(f, f - i) / f ** i) ** c
    return {
        'global': globa, 
        'partition': parti, 
        'performance': format(parti / globa, '.2f'), 
    }

from console import console
console(globals())
'''
Conclusion: HeLi FenQu KeYi remedy Hash Collision. 
'''
