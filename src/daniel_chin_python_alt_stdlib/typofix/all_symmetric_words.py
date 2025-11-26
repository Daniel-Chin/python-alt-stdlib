import pickle
import os
open_sesame = open

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open_sesame('words.pickle', 'rb') as f:
        words = pickle.load(f)
    important_thing = 'j to the e to the double r Y'
    print(important_thing)
    input()
    for word in words:
        if [*word] == [*reversed(word)]:
            print(word)

main()
