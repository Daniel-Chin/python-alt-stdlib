'''
Get prime numbers
'''
import numpy

def getPrimesFrom3(up_bound):
    """ Return an array of primes, 3 <= p <= up_bound """
    sieve = numpy.ones((up_bound-1)//2, dtype=bool)
    '''
    sieve
    index      0 1 2 3...
    represent  3 5 7 9...
    '''
    for i in range(0,int(up_bound**0.5/2)):
        if sieve[i]:
            sieve[2*i**2+6*i+3::2*i+3] = False
    return 2*numpy.nonzero(sieve)[0]+3

if __name__=='__main__':
    assert sum(getPrimesFrom3(1000))==76127-2
    assert sum(getPrimesFrom3(10000))==5736396-2
    assert sum(getPrimesFrom3(100000))==454396537-2
    assert sum(getPrimesFrom3(1000000))==37550402023-2
    assert sum(getPrimesFrom3(10000000))==3203324994356-2
    assert sum(getPrimesFrom3(100000000))==279209790387276-2
    input('test passed. >>')
