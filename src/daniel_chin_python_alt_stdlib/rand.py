'''
I just wanna generate a random number very conveniently,  
e.g. Win+R py -m rand
'''

import random

while True:
    b = int(input('maximum='))
    print(random.randint(0, b))
