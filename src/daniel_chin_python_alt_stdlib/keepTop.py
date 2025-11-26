'''
Maintain a list of high scores.  
'''

import numpy as np

class KeepTop:
    def __init__(self, size, evaluate = None) -> None:
        self.size = size
        self.scoreboard = [(None, - np.inf)]
        if evaluate is None:
            self.evaluate = lambda x : x
        else:
            self.evaluate = evaluate
        
        self.low = - np.inf
    
    def eat(self, x):
        if len(self.scoreboard) < self.size:
            self.__add(x)
            return
        score = self.evaluate(x)
        if score > self.low:
            self.__add(x, score)
    
    def __add(self, x, score = None):
        if score is None:
            score = self.evaluate(x)
        for i, (_, item_score) in enumerate(self.scoreboard):
            # imagine binary search
            if score < item_score:
                break
        else:
            i = len(self.scoreboard)
        self.scoreboard = (
            self.scoreboard[:i] + [( x, score )] + self.scoreboard[i:]
        )   # imagine linked list
        if len(self.scoreboard) > self.size:
            self.scoreboard.pop(0)
        self.low = self.scoreboard[0][1]
    
    def getList(self):
        return [item for (item, _) in self.scoreboard]

if __name__ == '__main__':
    kt = KeepTop(5)
    from random import randint
    for _ in range(50):
        kt.eat(randint(0, 69))
    print(kt.getList())
