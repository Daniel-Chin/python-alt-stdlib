'''
Too bad. It does not work. Mindustry 6.0 is anti-python?  
'''
from keyboard import add_hotkey, send, clear_all_hotkeys, release, press

def main():
  try:
    for o, i in enumerate('zxcasdqwe'):
      add_hotkey(f'alt+{i}', _send, args=(o + 1, ))
      print('Alt +', i, 'is', o)
    while input('Enter "y" to quit >').lower() != 'y':
      pass
  finally:
    clear_all_hotkeys()

def _send(x):
  release('alt')
  send(str(x))
  press('alt')

main()
