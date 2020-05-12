from cvm.cvmgen import Generator
from cvm.cvmgen import Exponential
from random import random
import numpy as np
import math
class Normal(Generator):
    '''
    Generate a normal random variable with mean=mean and std = stdev.
    You can choose several generation methods being:
    'r': rejection method implemented with exponentials
    'c': composition method
    'q': uniform quotient
    '''
    def __init__(self,mean=0,stdev=1,method='r',**kw):
        NORMAL_CONST = 1/np.sqrt(2*math.pi)
        self.mean = mean
        self.stdev = stdev
        self.pdf = [lambda x: (NORMAL_CONST/stdev)*np.exp(-((x-mean)**2)/2*(stdev**2))]
        self.method = method
        self.generate = self._setMethod(method)
        self._setMethod(method)

        super().__init__(
            pdf=self.pdf,
            piecewise=False,
            x_lim=(-stdev*4,stdev*4),
            **kw)

    def _setMethod(self,method):
        if method == 'r':
            generator = self.genR
        elif method == 'p':
            generator = None
        elif method == 'q':
            generator = self.genQ
        else:
            raise ValueError("Valid methods are: r: rejection method, q: uniform quotient method.")
        return generator


    def gen(self):
        return self.generate()

    def genR(self):
        '''
        Generate a normal standard variable
        using rejection method as explained
        in S.M.Ross Simulation section 5f
        '''
        expgen = Exponential(1)
        y1 = expgen.gen()        
        y2 = expgen.gen()

        while y2 -((y1-1)**2)/2 <= 0:
            y1 = expgen.gen()        
            y2 = expgen.gen()
        if random() < 1/2:
            norm = y1
        else:
            norm = -y1
        return norm*self.stdev + self.mean

    def genQ(self):
        '''
        Generate a normal standar variable
        using the uniform quotient method
        '''
        CONST = 4*np.exp(-0.5)/np.sqrt(2.0)
        u1 = random()
        u2 = 1 -  random()
        z = CONST*(u1-0.5)/u2
        zz = z*z/4.0
        while zz > -np.log(u2):
            u1 = random()
            u2 = 1 -  random()
            z = CONST*(u1-0.5)/u2
            zz = z*z/4.0
        return self.mean + self.stdev * z


class NormalPolar(Normal):
    '''
    Generate 2 normal independent variables
    using the Polar Method
    '''
    def __init__(self,mean=0,stdev=1,**kw):
        super().__init__(mean,stdev,method='p',**kw)

    def gen(self):
        SquareR = -2 * np.log(1-random())
        Thetha = 2 * math.pi * random()
        x = np.sqrt(SquareR) * np.cos(Thetha)
        y = np.sqrt(SquareR) * np.sin(Thetha)
        res = (x*self.stdev + self.mean,y*self.stdev + self.mean)
        # I'm gonna return only one value, temporarily, to be able to
        # plot and see things. BUT i need to come up with a different
        # idea to visualize the generation process
        return res[0]

    