from cvm.cvmgen import Generator
from random import random
import math
import numpy as np

class Cauchy(Generator):
    '''
    Generate a cauchy variable
    with different methods.
    Possible methods:
    q: uniform quotient method
    it: inverse transform method
    '''
    def __init__(self,lamda=1,method='q',**kw):
        METHODS = ['q','it']
        if method not in METHODS:
            raise ValueError('Possible values for method are {}'.format(METHODS))
        CAUCHYCONST = lamda*math.pi 
        PDFCONST = 1/math.pi
        PI = math.pi
        self.lamda = lamda
        self.method = method
        self.cdf = [lambda x: 1/2 + np.arctan(x/self.lamda)*PDFCONST]
        self.pdf = [lambda x: 1/(CAUCHYCONST*(1+(x/lamda)**2))]
        self.inverse_cdf = lambda x: self.lamda*np.tan(PI*(x-1/2))
        super().__init__(pdf=self.pdf,cdf=self.cdf,piecewise=False,**kw)

    def gen(self):
        method = self.method
        if method == 'q':
            value = self.genQ()
        elif method == 'it':
            value = self.genIT()
        return value

    def genIT(self):
        inverse_cdf = self.inverse_cdf
        u = random()
        return inverse_cdf(u)*self.lamda    

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


