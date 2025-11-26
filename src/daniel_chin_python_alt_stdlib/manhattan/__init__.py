import numpy as np
import pylab as plt

class Point:
    __slot__ = ['x', 'y', 'name']

    def __init__(self, x=None, y=None, name=None) -> None:
        self.x = x
        self.y = y
        self.name = name

    def __abs__(self):
        return np.abs(self.x) + np.abs(self.y)
    
    def __repr__(self):
        return (self.name or '') + f'({self.x}, {self.y})'
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Point(- self.x, - self.y)

    def __sub__(self, other):
        return self + (- other)
    
    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
    def __rmul__(self, other):
        return self * other
    
    def orientation(self):
        r = abs(self)
        if self.x >= 0: 
            if self.y >= 0:
                return abs(Point( r,  0) - self) / r
            else:
                return abs(Point( 0, -r) - self) / r + 6
        else:
            if self.y >= 0:
                return abs(Point( 0,  r) - self) / r + 2
            else:
                return abs(Point(-r,  0) - self) / r + 4

PI = 4

def cos(x):
    return np.abs(x % 8 - 4) / 2 - 1

def sin(x):
    return cos(x - 2)

def tan(x):
    return sin(x) / cos(x)

class PolarPoint(Point):
    __slot__ = ['r', 'theta', 'name']

    def __init__(self, r=None, theta=None, name=None) -> None:
        self.r = r
        self.theta = theta
        self.name = name
    
    @property
    def x(self):
        return self.r * cos(self.theta)
    @property
    def y(self):
        return self.r * sin(self.theta)

    def eularize(self):
        return self.r * Point(cos(self.theta), sin(self.theta))

    def fromEular(point):
        return PolarPoint(abs(point), point.orientation())
    
    def __repr__(self):
        return (self.name or '') + f'(r={self.r}, θ={self.theta})'

def circle(r, linspace):
    theta = np.linspace(0, 2*PI, linspace)
    return [PolarPoint(r, t) for t in theta]

def square(r, linspace):
    s = np.linspace(-r, r, linspace // 4)
    points = []
    points.extend([Point(x,  r) for x in s])
    points.extend([Point(x, -r) for x in s])
    points.extend([Point( r, y) for y in s])
    points.extend([Point(-r, y) for y in s])
    return points

def scatter(points, **kw):
    plt.scatter(
        [p.x for p in points], 
        [p.y for p in points], 
        **kw, 
    )
