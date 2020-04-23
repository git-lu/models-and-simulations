
from random import random
from math import exp
##estimación de la integral de g con Nsim simulaciones


def monteCarlo0Infinite(g, nSim):
    ''' 
    Given integration limits 0 infinite
    '''
    h = lambda y: g((1/y)-1) * (1/(y**2)) 
    integralValue = monteCarlo01(h,nSim) 
    return integralValue

def monteCarloInfinite0(g, nSim):
    ''' 
    Given integration limits 0 infinite
    '''
    h = (lambda y: g((1/(-y))-1)* (1/(-y)**2)) 
    integralValue = monteCarlo01(h,nSim) 
    return integralValue

def monteCarloMulti(g,nSim):
    integral = 0
    for _ in range(nSim):
        integral += g(random(),random())
    return integral/nSim

def monteCarloInfInf(g,nSim,isEven=False):
    '''
    Estimates the integral of f between
    inf and -inf. 
    '''
    if isEven:
        integralValue = 2*monteCarlo0Infinite(g, nSim)
    else:
        integralValue = monteCarloInfinite0(g,nSim) + monteCarlo0Infinite(g,nSim)
    return integralValue
    

def monteCarloab(f, a, b, nSim):
    '''
    Given integrations limits a and b we have to map
    those limits to (0,1)
    '''
    # Mapping the domain:
    g = (lambda y: f(a + (b-a) * y))
    integralValue = monteCarlo01(g,nSim)*(b-a) 
    return integralValue


def monteCarlo01(f, nSim):
    '''
    Given ONE function that takes one parameter, calculates
    the integral by generating a random number between 0 and 1 'U' 
    and adding over the results of applying the function to U
    '''
    integralValue = 0
    for _ in range(nSim):
        integralValue += f(random())
    return integralValue/nSim


class MonteCarlo():
    '''
    Calculates a given integral using monteCarlo's method. This is
    a numerical method to numerically calculate difficult
    mathematical expressions.
    '''
    def __init__(self,f,integrationLimits,nParams,nIters):
        self.funs = f
        self.nParams = 0
        self.integrationLimits = integrationLimits
        self.result = 0

    def calculate(self,nIters):
        pass




