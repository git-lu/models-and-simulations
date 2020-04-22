from random import random

def meanEstimator(f,k,nSim):
    '''We estimate the mean of the sum of the function given
    using some Monte Carlo theoretical results.
    We calculate the result of the sum calculating the mean of the 
    terms applied to a uniform variable
    f is the function we want to estimate
    k is the number of terms of the sum
    nSim is the number of iterations we will use to estimate'''
    estimation = 0
    for _ in range(nSim):
        u = int(random()*k) + 1
        estimation += f(u)
    return (estimation/nSim)*k 

    
    

    