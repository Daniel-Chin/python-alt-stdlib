from numpy import random
from stats import mean

EXP = 99999
N_X = 4

# sales = 0 + t * k + \sigma
k = [1, 2, -1, 1.9] # slope
d = [0, 2, 2, 2.5]  # noise 

def sample():
  data = []
  sums = []
  for t in range(N_X):
    data.append([x * t + random.normal() * y for x, y in zip(k, d)])
    sums.append(sum(data[-1]))
  return data, sums
  # china japan italy korea sum
  #1                           
  #2                           
  #3                           
  #4                           

def leastSquare(x, y):
  n = len(x)
  x_bar = sum(x) / n
  y_bar = sum(y) / n
  ssxy = sum([a * b - n * x_bar * y_bar for a, b in zip(x, y)])
  ssxx = sum([a ** 2 - n * x_bar ** 2 for a, b in zip(x, y)])
  return ssxy / ssxx

def myMethod():
  betas = []
  for _ in range(EXP):
    _, sums = sample()
    betas.append(leastSquare([*range(N_X)], sums))
  return betas

def fsaMethod():
  betas = []
  for _ in range(EXP):
    data, _ = sample()
    beta = [leastSquare([*range(N_X)], [data[x][j] for x in range(N_X)]) for j in range(4)]
    betas.append(sum(beta))
  return betas

def main():
  truth = sum(k)
  mine = [x - truth for x in myMethod()]
  fsa = [x - truth for x in fsaMethod()]
  with open('vs.csv', 'w+') as f:
    print('mine', 'fsa', sep = ',', file = f)
    for a, b in zip(mine, fsa):
      print(a, b, sep = ',', file = f)

main()
