# A5 = 440 Hz
# C5 = 0
from winsound import Beep as beep
def sound(pitch,length):
    letter=pitch[0]
    height=int(pitch[1])
    note=(height-4)*12 + {'c':0,\
                          'd':2,\
                          'e':4,\
                          'f':5,\
                          'g':7,\
                          'a':9,\
                          'b':11}[letter]
    frequency=int(2**(note/12)* 261.6255653005986)
    beep(frequency,int(length))
