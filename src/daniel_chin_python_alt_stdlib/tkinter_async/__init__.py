'DONT COMILE README'

'''
I realize that this module is useless after fixing all its bugs.  

Original doc:
Worried that your async callbacks may fire in the middle of and `update()` and cause race condition?  
This module schedules async callbacks for tkinter.  
'''

__all__ = [ 'sched', 'tkAsync' ]

default_root = None

def sched(*args, **kw):  # only use this when your app has only 1 window
  default_root.sched(*args, **kw)

class TkAsync:    
  def __init__(self, root):
    self.root = root
    self.scheded = []
    self.saved_mainloop = root.mainloop
    root.mainloop = self.mainloop
    root.sched = self.sched
  
  def mainloop(self, n = 0):
    self.root.after(1, self.handle)
    self.saved_mainloop(n)
  
  def handle(self):
    self.root.after(1, self.handle)
    for func, args, kw in self.scheded:
      func(*args, **kw)
  
  def sched(self, func, *args, **kw):
    self.scheded.append((func, args, kw))

def tkAsync(root):
  global default_root
  TkAsync(root)
  default_root = root
