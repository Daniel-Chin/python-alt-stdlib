from time import sleep
from Sound import *
from English import *
from Song import song
def main(song=song,pace=.3):
    input('Please turn audio on and then hit Enter. ')
    print('\n'*20)
    for beer in range(99,0,-1):
        for word in song:
            lyric=word[0]
            pitch=word[1]
            if pitch is None:
                sleep(pace)
            else:
                if type(lyric) is int:
                    lyric=english((beer,lyric))
                print(lyric,end='',flush=True)
                sound(pitch,100)
                sleep(pace)
main()
