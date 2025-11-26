'''
The bar chart provided by matplotlib is surprisingly manual.  
Let's fix that.  
'''

import numpy as np
from matplotlib import pyplot as plt

class SmartBar:
    def __init__(
        self, padding: float =None, 
    ) -> None:
        '''
        0 <= `padding` < 1 is the whitespace between bars.  
        '''
        self.padding = padding
        self.groups = []
        self.group_kw = []
        self.labels = []
        self.x_ticks = None
    
    def setXTicks(self, ticks):
        self.x_ticks = ticks

    def addGroup(self, Y, label='default', **kw):
        self.groups.append(Y)
        self.labels.append(label)
        self.group_kw.append(kw)
    
    def validate(self):
        assert len(self.groups)
        lens = []
        for Y in self.groups:
            lens.append(len(Y))
        if len(set(lens)) != 1:
            raise IndexError(
                f'The groups are not of equal len: {lens}'
            )
        x_len = lens[0]
        if self.x_ticks is not None:
            assert len(self.x_ticks) == x_len
        return x_len
    
    def draw(self, ax: plt.Axes =None):
        ax = ax or plt.gca()
        x_len = self.validate()
        cell_width, roll = self.rollX()
        x = np.arange(x_len)
        for Y, x_offset, label, kw in zip(
            self.groups, roll, self.labels, self.group_kw,
        ):
            ax.bar(
                x + x_offset, Y, cell_width, label=label, 
                align='edge', **kw, 
            )
        if self.x_ticks is not None:
            ax.set_xticks(x)
            ax.set_xticklabels(self.x_ticks)
    
    def rollX(self):
        n_groups = len(self.groups)
        if self.padding is None:
            width = (n_groups) / (n_groups + 1.5)
        else:
            width = 1 - self.padding
        cell_width = width / n_groups
        x_start = - width * .5
        x_stop  = + width * .5
        return cell_width, np.linspace(
            x_start, x_stop, n_groups, False, 
        )

def demo():
    sBar = SmartBar()
    sBar.addGroup([1, 3, 3, 3, 7], 'hacker')
    sBar.addGroup([1, 2, 3, 4, 5], 'linear')
    sBar.addGroup([3, 1, 4, 1, 5], 'pi')
    sBar.setXTicks('abcde')
    sBar.draw()
    plt.legend()
    plt.show()

if __name__ == '__main__':
    demo()
