import re
import pickle
from collections import Counter
import operator
from string import ascii_lowercase

TAKE = 20000

with open('big.txt', 'r') as f:
    big = f.read().lower()
counter = Counter(re.findall(r'\w+', big))
print('total:', len(counter))
print('take:', TAKE)
items = list(reversed(sorted(counter.items(), key=operator.itemgetter(1))))[:TAKE]
words = {w for w, n in items if all([c in ascii_lowercase for c in w])} - ({*ascii_lowercase} - {*'ai'})
with open('words.pickle', 'wb+') as f:
    pickle.dump(words, f)
