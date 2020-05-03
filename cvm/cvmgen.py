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
        cdf=[],
        limits=[],
        pdf = [],
        conds = [],
        piecewise = True,
        x_lim = (0,8)
        ):
        # This is the one we actually use to generate the 
        # variable
        self.inverse_cdf = inverse_cdf
        # The cummulative distribution function
        self.cdf = cdf
        # The density probability function, used to plot
        self.pdf = pdf
        self.piecewise = piecewise
        if piecewise:
            self.limits = self._calculateLimits(limits)
        else:
            self.limits = [1]
        self.conds = conds
        self.values = []
        self.mean = 0
        self.x_lim = x_lim
    
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
        y_lim=(0,2),
        figsize=(12,6),
        bins = 20):
        '''
        To plot, the probability density function must 
        be defined. Also a list of 
        conditions should be given
        '''
        # pylint: disable=no-member,unused-variable
        x_lim = self.x_lim
        ffunc = self.pdf
        x = np.linspace(x_lim[0],x_lim[1])
        # Create new Figure and an Axes which fills it.
        fig,ax = plt.subplots(figsize=figsize)
        if self.piecewise:
            conds = self.conds
            f = np.piecewise(x, conds, ffunc)
            ax.plot(x,f,'k',linewidth=3,label='f(x)')
        else:
            f = ffunc[0]
            ax.plot(x,f(x),'k',linewidth=3,label='f(x)')
        
    
        values = [self.gen() for _ in range(nValues)]
        
        self.values = values
        self.mean = np.mean(values)
    
        N,bins,patches = ax.hist(values,bins=bins,density=True,color='k')
        fracs = N / N.max()

        norm = colors.Normalize(fracs.min(), fracs.max())
        norm = colors.Normalize(fracs.min(), fracs.max())

        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.Spectral_r(norm(thisfrac))
            thispatch.set_facecolor(color)

        ax.set_xlim(x_lim[0],x_lim[1])
        ax.legend(loc='upper left')
        ax.set_xticks( range(x_lim[0],x_lim[1]) )
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        plt.title("Distribution of generated values")
        plt.show()        


class Pareto(InverseTransform):
    def __init__(self,a,x_lim=(0,8)):
        self.a = a
        inverse_cdf = [lambda x: (1 - x)**(-1/a)]
        pdf = [0,lambda x: a*(x**(-(a+1)))]
        cdf = [lambda x: 1-x**(-a)]
        x = np.linspace(x_lim[0],x_lim[1])
        conds = [x<1,x>1]
        lims = [np.infty]
        super().__init__(inverse_cdf,cdf=cdf,limits=lims,pdf=pdf,conds=conds)

class Weibull(InverseTransform):
    def __init__(self,lamda,beta,x_lim):
        self.beta = beta
        self.lamda = lamda
        # WELL this is incredibly HORRIBLE 
        pdf = [0,lambda x: (beta/lamda)*(x/lamda)**(beta-1)*np.exp(-(x/lamda)**(beta))]
        cdf = [lambda x: 1 - np.exp(-(x/lamda)**(beta))]
        inverse_cdf = [lambda x: lamda * (-np.log(1-x))**(1/beta)]
        lims = [np.infty]
        x = np.linspace(x_lim[0],x_lim[1])
        conds = [x<= 0, x>=0]
        super().__init__(inverse_cdf,cdf=cdf,limits=lims,pdf=pdf,conds=conds,x_lim=x_lim)