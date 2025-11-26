from dchin_log import DChinLog

dcl = DChinLog(__file__)
param = dcl.param

CGD = 'Cordinated Gradient Descend'
GD = 'Gradient Descend'
BIG = 'BIG'
SMALL = 'SMALL'

param.MODE = CGD
param.LR = BIG

def main():
    with dcl as print:
        if param.MODE is CGD:
            print('did this, did that')
        if param.LR is BIG:
            print('omg, failed. ')

main()
