from random import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import itertools
import functools

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
        linspace = [],
        generator = None
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
        # You can define a custom generator
        self.generator = generator

    def gen(self):
        return self.generator()

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
        ax.set_ylim(y_lim[0],y_lim[1])
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
    f given the inverse of the 
    cummulative probability function.
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
        cdf = [0,lambda x: 1 - np.exp(-lamda*x)]
        # We will use our own generation method so...
        inverse_cdf = []
        x = np.linspace(x_lim[0],x_lim[1])
        conds = [x<0,x>=0]
        super().__init__(inverse_cdf,pdf=pdf,cdf=cdf,conds=conds,x_lim=x_lim,)

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


class Erlang(Generator):
    def __init__(self,k,mu,x_lim=(0,8),y_lim=(0,1)):
        self.k = k
        self.mu = mu
        x = np.linspace(x_lim[0],x_lim[1])
        conds = [x <= 0, x > 0]
        pdf = [0,lambda x: (x**(k-1) * np.exp(-x/mu))/(np.math.factorial(k-1)*(mu**k))]
        super().__init__(pdf,conds=conds,x_lim=x_lim,y_lim=y_lim)

    def gen(self):
        u = 1
        k = self.k
        lamda = self.mu
        for _ in range(k):
            u *= 1 - random()
        return -np.log(u)*lamda

class CompositionMethod(Generator):
    '''
    This method generates a random variable
    that its distribution can be expressed as a
    weighted sum of other distributions:
    F(x) = sum from 1 to n of pi*Fi(x)
    where sum(pi) = 1, 1 <= i <= n
    AND we know how to generate n Fi random variables
    IT IS asumed that the generators are from class generator
    AND the weights are sorted and corresponding to each generator.
    OK?
    '''
    def __init__(self,generators,weights):
        if sorted(weights) != weights:
            raise ValueError("Sort the weights and the generators")
        if not all(issubclass((type(gen)).__bases__[0],Generator) for gen in generators):
            raise ValueError("Please please give a list of instances of Generator")
        if len(weights) != len(generators):
            raise ValueError("weights and generators must be the same lenght")
        if sum(weights) != 1:
            raise ValueError("The weights sum is not 1")

        n = len(weights)
        self.generators = generators
        self.weights = weights
        pdf = self.__pdfFromGens()
        super().__init__(pdf,piecewise=False)


    def __pdfFromGens(self):
        '''
        We generate the pdf from the
        generators and the weights.
        What we want is:
        pdf = sum(gen.pdf*weigths)
        '''
        def pdfmult(pdf,a):
            def multWrapper(x):
                newPdf = pdf(x) * a
                return newPdf
            return multWrapper

        def pdfsum(pdfs):
            def sumWrap(x):
                fsum = 0
                for f in pdfs:
                    fsum += f(x)
                return fsum
            return sumWrap
        gens = self.generators
        weights = self.weights
        # For now, we will pick only the second one asuming
        # The first one is zero. Can and SHOULD be refined. 
        # As it is is disgusting but well

        # Get the principal probability function
        pdfs = [gen.pdf[1] for gen in gens]
        # Multiply those by its corresponding weight
        pdfsMult = [pdfmult(pdfs[i],weights[i]) for i in range(len(pdfs))]
        # Sum all of them
        pdf = pdfsum(pdfsMult)
        # Return in a list because pdfs are lists YOU KNOW very clever of me
        return [pdf]

    def gen(self):
        u = random()
        gens = self.generators
        weights = self.weights
        i = 0
        weight = weights[i]
        gen = gens[i].gen
        while u > weight:
            i += 1
            weight += weights[i]
            gen = gens[i].gen
        return gen()

        

class RejectionMethod(Generator):
    '''
    Generate a random variable with distribution
    pdf_x, given another random variable y,
    which we know how to generate.
    '''

    def __init__(self,pdf_x,pdf_y,gen_y,c=None,**kw):
        self.pdf_x = pdf_x
        self.pdf_y = pdf_y
        self.gen_y = gen_y
        if c is None:
            self.c = self.__calculateC()
        else:
            self.c = c
        super().__init__(pdf=pdf_x,**kw)

    def __calculateC(self):
        '''
        C is the minimum value
        such that f(x)/g(x) < c
        
        '''
        
        return 0

    def gen(self):
        y = self.gen_y()
        while random() >= self.pdf_x[0](y) / (self.c * self.pdf_y(y)):
            y = self.gen_y()
        return y 
