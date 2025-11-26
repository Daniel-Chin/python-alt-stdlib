from math import *

FUN = 10000
d = 5

def myFunc(x, d):
  c = cos(x)
  k = d**2 + 1 - 2*d*c
  return (d-c) / (
    k * sqrt(k)
  )

thetas = [x / 1000 * pi for x in range(FUN)]
Z = 2 * sum([myFunc(x, d) for x in thetas]) / FUN * pi
T = 2 * pi / d**2
print(Z)
print(T)
