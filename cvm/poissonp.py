import numpy as numpy
from cvm.cvmgen import Exponential
import matplotlib.pyplot as plt


class PoissonProcess():
    def __init__(self,lamda,T,h=True,flambda=[],lims=[]):
        self.time = T
        self.lamda = lamda
        self.h = h
        self.flambda = flambda
        self.lims = lims
    
    def gen(self):
        T = self.time
        exp = Exponential(self.lamda)
        eventTimes = []
        t = exp.gen()
        while t < T:
            eventTimes.append(t)
            t += exp.gen()
        return eventTimes
    
    def plot(self,**kw):
        figsize = (16,2)
        fig , ax = plt.subplots(figsize=figsize)

        # Generate n_values to plot and not plot the "problematic" ones
        values = self.gen()
        n = len(values)
        ax.scatter(values,[0]*n,color='k')
        # Set x_axis limits 
        ax.set_xlim(0,self.time)
        # Set y_axis limits
        ax.set_ylim(-0.5,0.5)
        # Set x_ticks 
        ax.set_xticks(list(range(0,self.time)))
        ax.spines['bottom'].set_position('zero')
        #plt.xticks(rotation=90)
        plt.title("Distribution of generated values")
        plt.show()      