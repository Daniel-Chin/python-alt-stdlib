'''
Inefficiently cache and lookup function returns. 
'''
class cache:
    def __init__(self, func):
        self.func = func
        self.i = []
        self.o = []
    
    def __call__(self, *args, **kw):
        for i, trying in enumerate(self.i):
            if trying == (args, kw):
                return self.o[i]
        self.i.append((args, kw))
        result = self.func(*args, **kw)
        self.o.append(result)
        return result
