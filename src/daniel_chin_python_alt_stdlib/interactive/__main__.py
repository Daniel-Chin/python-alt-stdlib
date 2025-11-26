from interactive import *
import interactive

print('Demoing `inputChin`:')
print('(double press ESC to clear)')
a = inputChin('set X = ', 26)
print(a)
from console import console
print(interactive.__all__)
console(globals())
