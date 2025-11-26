'''
Find local minima of a 1D function without gradient.  
Minimizes the number of calls to the function.  
Run this script to test it.  
Implementation:  
* A 3-point recursion of shifting and zooming  
* Cacheing with input as Fractions  
'''
from functools import lru_cache
from fractions import Fraction

HALF = Fraction(1, 2)

def blindDescend(func, resolution, init_step, guess = None):
  if guess is None:
    guess = 0
  def trans(fraction):
    return float(guess + fraction * init_step)
  @lru_cache(128)
  def trans_func(fraction):
    return func(trans(fraction))
  target_trans_step = abs(resolution / init_step)
  trans_cursor = 0
  trans_step = 1
  while trans_step > target_trans_step:
    left = trans_cursor - trans_step
    right = trans_cursor + trans_step
    if trans_func(trans_cursor) < min(
      trans_func(left), trans_func(right)
    ):
      # Zoom in
      # print('zoom')
      trans_step *= HALF
    if trans_func(right) < trans_func(left):
      # print('right')
      trans_cursor += trans_step
    else:
      # print('left')
      trans_cursor -= trans_step
  if trans_func(right) < trans_func(left):
    trans_cursor = right
  else:
    trans_cursor = left
  return (trans(trans_cursor), trans_func(trans_cursor))

# test
if __name__ == '__main__':
  from math import pi
  print('This is a test')
  def f(x):
    print('`f` called')
    return (x + pi) ** 2
  print(blindDescend(f, .01, 1, 3))
  print(blindDescend(f, .01, -1, 3))
  print(blindDescend(f, -.01, -1, 3))
  print(blindDescend(f, -.01, 1, 3))
  print(blindDescend(f, -.01, 1, -3))
