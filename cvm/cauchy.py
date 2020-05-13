from cvm.cvmgen import Generator
from random import random
import math
import numpy as np

class Cauchy(Generator):
    '''
    Generate a cauchy variable
    with different methods
    '''
    def __init__(self,lamda=1,method='q',**kw):
        CAUCHYCONST = lamda*math.pi 
        self.lamda = lamda
        self.method = method
        self.pdf = [lambda x: 1/(CAUCHYCONST*(1+(x/lamda)**2))]
        super().__init__(pdf=self.pdf,piecewise=False,**kw)

    def gen(self):
        return self.genQ()

    def genIT(self):
        return 0

    def genQ(self):
        '''
        Generate a point (u,v) uniformely
        distributed in a rectangle that contains 
        C = {(x,y)| 0<x<sqrt(f(u/v)}.
        We have proven that C is a right semicircle centered
        in (0,0) with radius 1/sqrt(pi).
        So we will generate points in the square 
        (0,1/sqrt(pi))x(-1/sqrt(pi),1/sqrt(pi)) 
        and check if they belong to the semicircle.
        If they do, we return u/v
        '''
        u = 1 - random()
        v = random()*(-2)+1
        while (u**2+v**2) > 1:
            u = 1 - random()
            v = random()*(-2) + 1
        return v/u


