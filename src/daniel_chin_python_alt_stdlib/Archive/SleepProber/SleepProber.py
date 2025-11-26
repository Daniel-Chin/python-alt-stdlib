from time import sleep
from Sound import *
from Song import song
def main(song=song,pace=.5,sustain=.1):
    while True:
        buff=''
        for i in song:
            if i != '\n':
                if buff=='':
                    buff+=i
                else:
                    pitch=buff+i
                    buff=''
                    if pitch=='  ':
                        sleep(pace)
                    else:
                        sound(pitch,1000*sustain)
                        sleep(pace-sustain)
main()
