'''
Compare the shape of two dicts. 
i.e. is the structure the same? are the keys the same? 
'''
__all__ = ['shapeOfDict', 'dictShapeCompare', 'pprintDict']
import json

def shapeOfDict(x):
    y = {}
    for key, value in x.items():
        if type(value) is dict:
            y[key] = shapeOfDict(value)
        else:
            y[key] = None
    return y

def dictShapeCompare(a, b):
    return shapeOfDict(a) == shapeOfDict(b)

def pprintDict(x):
    print(json.dumps(x, indent = 2))
