print('demo')

import tkinter as tk
from tkinter_async import *
from time import sleep

class App:
  def __init__(self, root):
    self.x = 0
    b = tk.Button(root, text='acc', command=self.subscribe)
    self.l = tk.Label(root, text='0')
    b.pack()
    self.l.pack()
    root.mainloop()
  
  def callback(self, result):
    self.x = result
    self.l['text'] = str(result)

print('baseline. It blocks the UI thread.')
print('(close the UI window when you are done testing...)')
print()

class App1(App):
  def subscribe(self):
    sleep(1)
    self.callback(self.x + 1)

root = tk.Tk()
App1(root)

print('Making it async. ')
print('This looks good, but it has race condition hazard.')
print('If the callback is fired during an update, your frontend code may break in rare occasions.')
print('(close the UI window when you are done testing...)')
print()
from threading import Thread
class AsyncTask(Thread):
  def __init__(self, app):
    self.app = app
    super().__init__()
  def run(self):
    sleep(1)
    self.app.callback(self.app.x + 1)

class App2(App):
  def subscribe(self):
    AsyncTask(self).start()
    self.l['text']='wait...'
    
root = tk.Tk()
App2(root)

print('Using this module. Removes the race condition hazard.')
print('(close the UI window when you are done testing...)')
class AsyncTask3(Thread):
  def __init__(self, app):
    self.app = app
    super().__init__()
  def run(self):
    sleep(1)
    sched(self.app.callback, self.app.x + 1)

class App3(App):
  def subscribe(self):
    AsyncTask3(self).start()
    self.l['text']='wait...'

root = tk.Tk()
tkAsync(root)
App3(root)
