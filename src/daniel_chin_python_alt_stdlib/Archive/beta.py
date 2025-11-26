'''
experiment regarding covariance, coefficient, regression

F: future price / market portfolio price
S: spot price / stock price
h: hedge ratio / beta

Both F and S refers to per period return.
'''

import numpy as np
normal = np.random.normal
from stats import mean, regression, coefficient, std
# from functools import lru_cache
# mean = lru_cache()(mean)

def sample(size = 3000, beta = .6, idio = .7):
  F = []
  S = []
  for _ in range(size):
    m = normal()
    # F.append(m)
    F.append(m + normal() * 0.2)
    S.append(m * beta + normal() * idio * 0)
  return F, S

def cov(A, B):
  return mean(
    [(a - mean(A)) * (b - mean(B)) for a, b in zip(A, B)]
  )

def var(A):
  return cov(A, A)

def covvar(F, S):
  return cov(F, S) / var(F)

def reg(F, S):
  return regression(F, S)[1]

def hedgeRatio(F, S):
  rho = coefficient(F, S)
  return rho * std(S, fix=False) / std(F, fix=False)

def areTheThreeTheSame():
  beta = .6
  F, S = sample(beta=beta)
  print(beta)
  print(covvar(F, S))
  print(reg(F, S))
  print(hedgeRatio(F, S))

areTheThreeTheSame()
