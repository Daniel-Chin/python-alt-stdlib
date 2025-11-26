'''
A double linked file list.  
A simple database solution, but highly scalable on systems that use hash map to store files.  
Each entry has a timestamp, and the list is sorted by time.  
Features:  
* Dynamic filename length, grows as the database grows.  
'''
# Time ascends from HEAD to TAIL. (old -> new)
from my import ChangeDir
import os
from os import path
import json
import random
from math import inf, log
from string import ascii_lowercase, digits

HEAD = '__head__'
TAIL = '__tail__'
ID_CHARS = (*ascii_lowercase, *digits)

class LinkedFileList:
  '''
  Warning: this class caches listdir result.  
  Please set self.list_dir = None everytime you change the dir.  
  '''
  def __init__(self, _path):  # UNIT TEST PASS
    self.path = _path.rstrip('/').rstrip('\\')
    self.cd = ChangeDir(_path)
    self.list_dir = None
    with self.cd:
      if not path.exists(HEAD):
        self.initDisk()
  
  def initDisk(self):  # UNIT TEST PASS
    name = path.split(self.path)[-1]
    with open(HEAD, 'w') as f:
      f.write('{"id": "%s", "next": "%s"}\n' % (HEAD, TAIL))
    with open(TAIL, 'w') as f:
      f.write('{"id": "%s", "prev": "%s"}\n' % (TAIL, HEAD))
    print(f'Initialized linked file list "{name}"')
  
  def getFile(self, id, mode):  # UNIT TEST PASS
    with self.cd:
      return open(id, mode)
  
  def getEntry(self, id):  # UNIT TEST PASS
    with self.getFile(id, 'r') as f:
      raw = json.load(f)
      if id in (HEAD, TAIL):
        if id == HEAD:
          time = -inf
        else:
          time = inf
        return {**raw, 'time': time}
      return raw
  
  def listDir(self):  # UNIT TEST PASS
    if self.list_dir is None:
      with self.cd:
        self.list_dir = os.listdir()
      assert '.' not in self.list_dir and '..' not in self.list_dir
      self.list_dir.remove(HEAD)
      self.list_dir.remove(TAIL)
    return self.list_dir
  
  def display(self):  # UNIT TEST PASS
    id = self.getEntry(HEAD)['next']
    print(*self.getEntry(id).keys(), sep = '\t')
    while id != TAIL:
      print(*self.getEntry(id).values(), sep = '\t')
      id = self.getEntry(id)['next']

  def seekTime(self, time, start_id):  # UNIT TEST PASS
    entry = self.getEntry(start_id)
    if time > entry['time']:
      direction = 'next'
      to_next = True
    else:
      direction = 'prev'
      to_next = False
    entry = self.getEntry(entry[direction])
    while (time > entry['time']) == to_next:
      entry = self.getEntry(entry[direction])
      if (time > entry['time']) != to_next:
        break
      randomEntry = self.getEntry(random.choice(self.listDir()))
      delta = time - randomEntry['time']
      if abs(delta) < abs(time - entry['time']):
        entry = randomEntry
        if delta > 0:
          direction = 'next'
          to_next = True
        else:
          direction = 'prev'
          to_next = False
    if to_next:
      return entry['prev'], entry['id']
    else:
      return entry['id'], entry['next']

  def newId(self):  # UNIT TEST PASS
    list_dir = self.listDir()
    id_len = int(log(len(list_dir) + 1, len(ID_CHARS))) + 3
    id = None
    while id is None or id in list_dir:
      id = ''.join([random.choice(ID_CHARS) for _ in range(id_len)])
    return id

  def add(self, entry):  # UNIT TEST PASS
    prev_id, next_id = self.seekTime(entry['time'], TAIL)
    id = self.newId()
    with self.getFile(id, 'w') as f:
      json.dump({
        **entry, 
        'id': id, 
        'prev': prev_id, 
        'next': next_id, 
      }, f)
    with self.getFile(prev_id, 'r') as f:
      original = json.load(f)
    with self.getFile(prev_id, 'w') as f:
      json.dump({**original, 'next': id}, f)
    with self.getFile(next_id, 'r') as f:
      original = json.load(f)
    with self.getFile(next_id, 'w') as f:
      json.dump({**original, 'prev': id}, f)
    self.list_dir.append(id)
  
  def delete(self, id):
    ...

if __name__ == '__main__':
  from console import console
  l = LinkedFileList('d:/temp/database')
  console({**globals(), **locals()})

'''
del list_dir when you add/remove
unit test
'''
