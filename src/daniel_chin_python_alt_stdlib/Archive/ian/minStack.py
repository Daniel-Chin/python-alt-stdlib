# This assumes python lists to be arrays. 

class MinStack:
    def __init__(self, size):
        self.size = size
        self.array = [None] * size
        self.cursor = 0
        self.min_history = [None] * size
    
    def push(self, newThing):
        if self.cursor == self.size:
            raise OverflowError('Stack overflow')
        self.array[self.cursor] = newThing
        if self.cursor == 0:
            self.min_history[0] = newThing
        elif newThing < self.min_history[self.cursor - 1]:
            self.min_history[self.cursor] = newThing
        self.cursor += 1
    
    def pop(self):
        if self.cursor == 0:
            assert EOFError('Stack underflow')
        self.cursor -= 1
        return self.array[self.cursor]
    
    def getMin(self):
        return self.min_history[self.cursor - 1]
    
    def peek(self):
        return self.array[self.cursor - 1]
