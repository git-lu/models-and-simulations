from random import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import itertools

class Generator():
    '''
    Generator class.
    Generates a random variable with
    probability distribution pdf
    '''
    def __init__(
        self,
        pdf = [],
        cdf = [],
        conds = [],
        piecewise = True,
        x_lim = (0,8),
        y_lim = (0,1),
        linspace = []
        ):
        # The density probability function, used to plot
        self.pdf = pdf
        # The cummulative distribution function
        self.cdf = cdf
        # Are the functions defined piecewise? Almost all of them are.
        self.piecewise = piecewise
        # These are for the conditions of the piecewise
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.conds = conds
        self.values = []
        self.mean = 0
        # Linear space in which we generate the variable and plot
        self.linspace = linspace

    def plot(
        self,
        nValues,
        figsize=(12,6),
        bins = 20,
        plotMean = True):
        '''
        To plot, the probability density function must 
        be defined. Also a list of 
        conditions should be given
        '''
        # pylint: disable=no-member,unused-variable
        x_lim = self.x_lim
        y_lim = self.y_lim
        ffunc = self.pdf

        if self.linspace == []:
            x = np.linspace(x_lim[0],x_lim[1])
        else:
            x = self.linspace
        # Create new Figure and an Axes which fills it.
        fig , ax = plt.subplots(figsize=figsize)

        # Plot the distribution
        if self.piecewise:
            conds = self.conds
            f = np.piecewise(x, conds, ffunc)
            ax.plot(x,f,'k',linewidth=3,label='f(x)')
        else:
            # There is only one function in the list
            f = ffunc[0]
            ax.plot(x,f(x),'k',linewidth=3,label='f(x)')
        
        # Generate n_values to plot
        values = [self.gen() for _ in range(nValues)]
        
        self.values = values
        self.mean = np.mean(values)

        # Here we plot the histogram and color the bars
        # per height
        N,bins,patches = ax.hist(values,bins=bins,density=True,color='k')
        fracs = N / N.max()

        norm = colors.Normalize(fracs.min(), fracs.max())
        norm = colors.Normalize(fracs.min(), fracs.max())

        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.Spectral_r(norm(thisfrac))
            thispatch.set_facecolor(color)

        # Set x_axis limits 
        ax.set_xlim(x_lim[0],x_lim[1])
        # Set y_axis limits
        ax.set_xlim(x_lim[0],x_lim[1])
        # Set x_ticks 
        ax.set_xticks(range(x_lim[0],x_lim[1]))
        # We draw a cartesian ax
        ax.axvline(x=0,color='k')
        ax.axhline(y=0,color='k')
        # Draw a line in y=1 for reference
        ax.axhline(y=1, color='k',alpha=0.3,linestyle='--')
        # Plot a vertical line where the mean is
        if plotMean:
            ax.axvline(x=self.mean,color='k',alpha=0.7,
            linestyle='--',label= 'Mean = {:.3f}'.format(self.mean))

        # Set legend location
        ax.legend(loc='best')

        plt.title("Distribution of generated values")
        plt.show()        





class InverseTransform(Generator):
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
        x_lim = (0,8),
        y_lim = (0,2),
        linspace = []
        ):
        # This is the one we actually use to generate the 
        # variable
        super().__init__(pdf,cdf,conds,piecewise,x_lim,y_lim,linspace)
        self.inverse_cdf = inverse_cdf
        if piecewise:
            self.limits = self._calculateLimits(limits)
        else:
            self.limits = [1]


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




class Exponential(InverseTransform):
    def __init__(self,lamda,x_lim=(0,8)):
        self.lamda = lamda
        pdf = [0,lambda x: lamda*np.exp(-lamda*x)]
        # We will use our own generation method so...
        inverse_cdf = []
        x = np.linspace(x_lim[0],x_lim[1])
        conds = [x<0,x>=0]
        super().__init__(inverse_cdf,pdf=pdf,conds=conds,x_lim=x_lim,)

    def gen(self):
        lamda = self.lamda
        u = random()
        return -np.log(u)/lamda


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


