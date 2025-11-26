class C:
 def __call__(self):
  print(1)

class D:
 def __call__(self):
  print(2)
 def __init__(self):
  self.__call__ = C()

d = D()
d()
