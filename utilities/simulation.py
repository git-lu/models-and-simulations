from utilities.efficency import runTimeCalc
import numpy as np
import matplotlib.pyplot as plt

class Simulation():
    def __init__(self,simFunction):
        self.simulation = simFunction
        self.results = []
        self.estimatedMean = 0
        self.std = 0

    def resetResults(self):
        self.results = []
        self.estimatedMean = 0
        self.std = 0
        
    def simulate(self,nSim):
        '''
        Exec a simulation nSim times
        Returns an array with the results of the simulation
        Updates the mean and standard deviation
        '''
        simulationResults = []
        for _ in range(nSim):
            simulationResults.append(self.simulation())
        self.results.append(simulationResults)
        self.estimatedMean = np.mean(simulationResults)
        self.std = np.var(simulationResults)

        return self

    def meanRunTime(self,nSim):
        '''
        Returns the mean execution time from 
        running the simulation nSim times
        '''            
        return runTimeCalc(self.simulation,nSim)

    def plot(self,n_bins = 10):
        '''
        Makes a plot with all the simulation results stored
        '''
        # pylint: disable=unused-variable
        nplots = len(self.results)
        results = self.results
        
        fig, axs = plt.subplots(1, nplots, sharey=True, tight_layout=True)
        if nplots == 1:
            axs.hist(results[0], bins=n_bins,normed=1)
        else:
            for i in range(nplots):
            # We can set the number of bins with the `bins` kwarg
                axs[i].hist(results[i], bins=n_bins,normed=1)
        return self




