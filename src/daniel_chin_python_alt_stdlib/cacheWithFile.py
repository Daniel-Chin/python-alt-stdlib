'''
````python
@cacheWithFile('expanded_matrix')
def expandMatrix(m):
    # some heavy computation
    result = ...
    return result
````
'''
import pickle

class cacheWithFile:
    def __init__(self, name, force_recompute=False):
        self.name = name + '.pickle'
        self.force_recompute = force_recompute
    
    def __call__(self, func):
        try:
            if self.force_recompute:
                raise FileNotFoundError
            with open(self.name, 'rb') as f:
                result = pickle.load(f)
        except FileNotFoundError:
            def f(*a, **kw):
                result = func(*a, **kw)
                with open(self.name, 'wb') as f:
                    pickle.dump(result, f)
                return result
        else:
            def f(*_, **__):
                return result
        return f
