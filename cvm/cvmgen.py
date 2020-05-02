from random import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class InverseTransform():
    '''
    Inverse transform method to generate
    random continue variables with distribution
    f given the cummulative probability function.
    '''
    def __init__(
        self,
        inverse_cdf,
        cdf,
        limits,
        pdf = [],
        conds = []
        ):
        # This is the one we actually use to generate the 
        # variable
        self.inverse_cdf = inverse_cdf
        # The cummulative distribution function
        self.cdf = cdf
        # The density probability function
        self.pdf = pdf
        self.limits = self._calculateLimits(limits)
        self.conds = conds
    
    def _calculateLimits(self,limits):
        lims = []
        for i in range(len(limits)):
            lims.append(self.cdf[i](limits[i]))
        return lims

        
    def gen(self):
        funcs = self.inverse_cdf
        lims = self.limits
        i = 0
        u = random()
        fun = funcs[0]
        lim = lims[0]
        while u > lim:
            i+=1
            fun = funcs[i]
            lim = lims[i]
        return fun(u)    

    def plot(
        self,
        nValues,
        x_lim,
        y_lim=(0,2),
        figsize=(12,6),
        bins = 20):
        '''
        To plot, the probability density function must 
        be defined. Also a list of 
        conditions should be given
        '''
        # pylint: disable=no-member,unused-variable
        x = np.linspace(x_lim[0],x_lim[1])
        conds = self.conds
        ffunc = self.pdf
        values = [self.gen() for _ in range(nValues)]
        f = np.piecewise(x, conds, ffunc)

        # Create new Figure and an Axes which fills it.
        fig,ax = plt.subplots(figsize=figsize)
        ax.plot(x,f,'k',linewidth=3,label='f(x)')
        N,bins,patches = ax.hist(values,bins=bins,density=True,color='k')
        fracs = N / N.max()

        norm = colors.Normalize(fracs.min(), fracs.max())
        norm = colors.Normalize(fracs.min(), fracs.max())

        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.Spectral_r(norm(thisfrac))
            thispatch.set_facecolor(color)


        ax.legend(loc='upper left')
        plt.title("Distribution of generated values")
        plt.show()        
