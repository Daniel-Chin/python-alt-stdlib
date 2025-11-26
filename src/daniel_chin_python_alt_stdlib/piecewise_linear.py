'''
Input: datapoints that define a piecewise linear function.  
Output: a rule-generated pytorch module implementing such a function.  
'''

import torch
from torch import Tensor
from matplotlib import pyplot as plt

class PiecewiseLinear(torch.nn.Module):
    def __init__(self, X: Tensor, Y: Tensor):
        super(PiecewiseLinear, self).__init__()

        n, = X.shape
        assert Y.shape == (n, )
        assert (X[1:] - X[:-1] > 0.0).all()
        self.y0 = Y[0]
        self.offset = torch.nn.Parameter(torch.zeros((
            1, n, 
        )), requires_grad=False)
        self.slope = torch.nn.Parameter(torch.zeros((
            1, n, 
        )), requires_grad=False)
        slope = 0.0
        for i in range(n):
            self.offset[0, i] = -X[i]
            if i == n - 1:
                target_slope = 0.0
            else:
                target_slope = (Y[i + 1] - Y[i]) / (X[i + 1] - X[i])
            self.slope[0, i] = target_slope - slope
            slope = target_slope

    def forward(self, x: Tensor, /):
        '''
        `x`: (batch_size, ).  
        '''
        x = x.unsqueeze(1) + self.offset
        x = torch.nn.functional.relu(x)
        x = x * self.slope
        x = x.sum(dim=1)
        x = x + self.y0
        return x

def test():
    X = torch.tensor([-2.0, 1.0, 3.0])
    Y = torch.tensor([6.0, -1.0, 1.0])
    print(X)
    print(Y)
    model = PiecewiseLinear(X, Y)
    x = torch.linspace(-4.0, 4.0, 100)
    y = model(x)
    plt.plot(x, y)
    plt.show()

if __name__ == '__main__':
    test()
