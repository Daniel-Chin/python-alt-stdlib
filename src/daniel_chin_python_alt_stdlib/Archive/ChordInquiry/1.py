def main():
    chords = set()
    for x in range(12):
        for y in range(12):
            z = 12 - x - y
            if x >= 3 and y >= 3 and z >= 3:
                candidate = '%d%d%d' % tuple(sorted([x, y, z]))
                chords.add(candidate)
    print(chords)

if __name__ == '__main__':
    main()

'''
{'336', '345', '444'}
336,    345,   543,   444
minor6 ,minor, major, augmented

"C Major family"
135: 435 (C major)
146: 543 (F major -1 inversion)
725: 354 (G major +1 inversion)

"A Minor family"
613 : 345 (A minor)
624 : 534 (D minor -1 inversion)
#573: 354 (E major +1 inversion)
'''
