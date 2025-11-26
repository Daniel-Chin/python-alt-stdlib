'''
Softmax with temperature and probability weighting.  
'''

from math import log, exp

COLDNESS = 1

def softmax(X, coldness = COLDNESS):
    try: 
        X[0][0]
    except TypeError:
        X = [(x, 1) for x in X]
    return log(
        sum([
            exp(x * coldness) * prob
            for (x, prob) in X
        ]) / sum(
            [prob for (x, prob) in X]
        )
    ) / coldness

def softmin(X, coldness = COLDNESS):
    try: 
        X[0][0]
    except TypeError:
        X = [(x, 1) for x in X]
    return - log(
        sum([
            exp(-x * coldness) * prob
            for (x, prob) in X
        ]) / sum(
            [prob for (x, prob) in X]
        )
    ) / coldness
