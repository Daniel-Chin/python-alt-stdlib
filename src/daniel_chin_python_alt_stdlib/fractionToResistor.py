'''
Given a fraction, find the resistor connection to achieve it.  
'''
SHOW_DIAGRAM = True
PARALLEL_PADDING = 1    # better be an odd number
IN_TUNE_THRESHOLD = .11

PARALLEL = 'PARALLEL'
SERIAL = 'SERIAL'

from indentprinter import indentPrinter
from fractions import Fraction
from math import log

class Node:
    def __init__(self):
        self.connection = None
        self.children = []
    
    def eval(self):
        if self.connection is None:
            return 1
        if self.connection is SERIAL:
            return sum([x.eval() for x in self.children])
        if self.connection is PARALLEL:
            return 1 / sum([1 / x.eval() for x in self.children])
    
    def append(self, connection, other):
        node = Node()
        node.connection = connection
        if connection is self.connection:
            node.children = [*self.children, other]
        else:
            node.children = [self, other]
        return node
    
    def repr(self):
        if not self.children:
            return Matrix([[*'-<R>-']])
        else:
            reprs = [x.repr() for x in self.children]
            if self.connection is SERIAL:
                height = max([x.height for x in reprs])
                width = sum([x.width for x in reprs]) - len(reprs) + 1
                m = Matrix(width, height)
                x = 0
                for r in reprs:
                    m.copy(x, (height - r.height) // 2, r)
                    x += r.width - 1
                return m
            if self.connection is PARALLEL:
                width = max([x.width for x in reprs]) + 2 + 2
                height = sum([x.height for x in reprs]) + PARALLEL_PADDING * (len(reprs) - 1)
                m = Matrix(width, height)
                y = 0
                for r in reprs:
                    for x in range(width):
                        m.set(x, y, '-')
                    m.copy((width - r.width) // 2, y, r)
                    y += r.height + PARALLEL_PADDING
                for y in range(height):
                    m.set(0,         y, ' ')
                    m.set(width - 1, y, ' ')
                    # if y == height // 2:
                    #     if m.get(1, y) == '-':
                    #         m.set(1,         y, '+')
                    #         m.set(width - 2, y, '+')
                    #         continue
                    m.set(1,         y, '|')
                    m.set(width - 2, y, '|')
                m.set(0,         height // 2, '-')
                m.set(width - 1, height // 2, '-')
                return m
    
    def __repr__(self):
        return repr(self.repr())
    
    def __add__(self, other):
        return self.append(SERIAL, other)
    
    def __mul__(self, other):
        return self.append(PARALLEL, other)

class Matrix:
    def __init__(self, *args):
        if len(args) == 1:
            self.main = args[0]
            self.width = len(self.main[0])
            self.height = len(self.main)
        elif len(args) == 2:
            self.width = args[0]
            self.height = args[1]
            self.main = [
                [' '] * self.width 
                for _ in range(self.height)
            ]
        else:
            raise Exception('Incorrect number of parameters')
    
    def get(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return ' '
        return self.main[y][x]
    
    def set(self, x, y, value):
        self.main[y][x] = value
    
    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.main])
    
    def copy(self, left, top, other):
        for y, row in enumerate(other.main):
            for x, char in enumerate(row):
                self.set(left + x, top + y, char)

def main():
    op = input('Fraction (x/y) = ')
    x, y = op.split('/')
    target = Fraction(int(x), int(y))
    R = Node()
    n_resistors = 1
    frontier = [[R, 1, ['C', 4, 0], True]]
    available = {'C'}
    while True:
        n_resistors += 1
        backier = frontier
        frontier = []
        for node, fraction, _, __ in backier:
            a = node + R
            a_fraction = Fraction(
                fraction.numerator + fraction.denominator, 
                fraction.denominator, 
            )
            assert abs(a_fraction - a.eval()) < .0001
            a_note = classify(a_fraction)
            a_same_octave = a_note[1] == 4
            frontier.append([a, a_fraction, a_note, a_same_octave])

            b = node * R
            b_fraction = Fraction(
                fraction.numerator, 
                fraction.numerator + fraction.denominator, 
            )
            assert abs(b_fraction - b.eval()) < .0001
            b_note = classify(b_fraction)
            b_same_octave = b_note[1] == 4
            for r, frac in ((a, a_fraction), (b, b_fraction)):
                print(frac)
                if frac == target:
                    print(r)
                    main()
            frontier.append([b, b_fraction, b_note, b_same_octave])

def displayFrontier(n_resistors, frontier, available):
    print('Using', n_resistors, 'resistors:')
    print()
    is_first = True
    with indentPrinter as p:
        for node, fraction, note, same_octave in frontier:
            if abs(note[2]) > IN_TUNE_THRESHOLD:
                continue
            available.add(note[0])
            if SHOW_DIAGRAM:
                if is_first:
                    is_first = False
                else:
                    p('=' * 60)
                    p()
            with indentPrinter as p:
                if SHOW_DIAGRAM:
                    [p(x) for x in repr(node).split('\n')]
                    p()
                p('fraction:', fraction)
                p('note: ', note[0], note[1], ' ', format(note[2], '.0%'), sep = '')
                if same_octave:
                    p('SAME OCTAVE')
                p()
    print('Available:', available)

def classify(fraction):
    pitch = log(1 / fraction) / log(2) * 12
    rounded = round(pitch)
    residual = pitch - rounded
    pitch_class = [
        'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
    ][rounded % 12]
    octave = (rounded // 12) + 4
    return pitch_class, octave, residual

if __name__ == '__main__':
    # R = Node()
    # from console import console
    # console({**locals(), **globals()})
    main()
