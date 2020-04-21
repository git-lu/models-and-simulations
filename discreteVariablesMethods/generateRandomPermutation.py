from random import random

def generateRandomPermutation(a):
    ''' Returns a random permutation of array a'''
    N = len(a)
    for j in range(N-1,0,-1):
        index = int((j+1)*random())
        a[j] , a[index] = a[index], a[j]
    return a