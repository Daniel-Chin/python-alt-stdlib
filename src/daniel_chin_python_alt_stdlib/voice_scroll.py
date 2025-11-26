'''
Scroll whatever you are reading with voice.  
low hum to scroll down. high hum to scroll up.  
'''
import pyaudio
from scipy import signal
import numpy as np
from time import sleep
import keyboard
from yin import yin

FRAME_LEN = 4096
SR = 44100

DECAY = 10
CAP = 2.3
THRESHOLD = 2
SCROLL_COOLDOWN = .15

SAMPLE_FORMAT = pyaudio.paFloat32
NP_DTYPE = np.float32
CHANNELS = 1

SECOND_PER_FRAME = FRAME_LEN / SR
DECAY_PER_FRAME = DECAY * SECOND_PER_FRAME

def getPower(frame):
  _, power = signal.periodogram(frame, SR)
  return np.log(np.sum(power))

class Stream:
  def __init__(self, p):
    self.p = p
  
  def __enter__(self):
    self.s = self.p.open(format=SAMPLE_FORMAT,
      channels=CHANNELS,
      rate=SR,
      frames_per_buffer=FRAME_LEN,
      input=True,
    )
    print('Recording...')
    return self.s
  
  def __exit__(self, a, b, c):
    self.s.stop_stream()
    self.s.close()
    print('Finished recording')

def main():
  room_power = getRoomPower()
  print('Room noise level =', room_power)
  input('Press Enter to start scrolling with voice...')
  WAIT = 1
  print(f'Wait {WAIT} seonds...')
  sleep(WAIT)
  print('You can now scroll with your voice!')
  acc = 0
  cooldown = 0
  with Stream(p) as stream:
    while True:
      cooldown -= SECOND_PER_FRAME
      frame = np.frombuffer(stream.read(FRAME_LEN), NP_DTYPE)
      power = max(0, getPower(frame) - room_power)
      direction = 0
      f0 = yin(frame, SR, FRAME_LEN)
      if f0 < 220:
        direction = 1
      else:
        direction = -1
      # if abs(f0 - 130.81) < 5:
      #   # C3
      #   direction = 1
      # if abs(f0 - 161.82) < 5:
      #   # E3
      #   direction = -1
      print(acc)
      acc += power * direction
      if acc > 0:
        acc -= DECAY_PER_FRAME
        acc = max(0, acc)
      else:
        acc += DECAY_PER_FRAME
        acc = min(0, acc)
      acc = min( CAP, acc)
      acc = max(-CAP, acc)
      if cooldown <= 0:
        if abs(acc) > THRESHOLD:
          scroll(acc > 0)
          cooldown = SCROLL_COOLDOWN

def getRoomPower():
  TIME = 3
  print(f'Record the room sound for {TIME} seconds.')
  print('Make regular noide during the process.')
  input('Press Enter...')
  WAIT = .5
  print(f'Wait {WAIT} seconds...')
  sleep(WAIT)
  n_frames = int(TIME * SR / FRAME_LEN)
  acc = 0
  with Stream(p) as stream:
    for i in range(n_frames):
      acc += getPower(np.frombuffer(
        stream.read(FRAME_LEN), NP_DTYPE, 
      ))
      print(f'{i} / {n_frames}', end = '\r', flush = True)
  return acc / n_frames

def scroll(down_or_up):
  text = 'DOWN' if down_or_up else 'UP'
  print('scroll', text)
  keyboard.send(text)

p = pyaudio.PyAudio()
try:
  main()
finally:
  p.terminate()
