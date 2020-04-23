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
        return self
        
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
        self.meanExecTime = 0

        return self

    def meanRunTime(self,nSim):
        '''
        Returns the mean execution time from 
        running the simulation nSim times
        '''            
        return runTimeCalc(self.simulation,nSim)

    def plotAllResults(self,n_bins = 10):
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

    def plot(self,n_bins = 10):
        '''
        Plot lastest simulation
        '''
        # pylint: disable=unused-variable
        results = self.results
        
        fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
        axs.hist(results[-1], bins=n_bins,normed=1)
        return self

    def calculateMeanExecTime(self,nRuns,plot=True):
        '''
        Calculates mean execution time 
        in nIters executions
        '''
        execTimes = runTimeCalc(self.simulation,nRuns)
        self.meanExecTime = np.mean(execTimes)
        print("The average execution time is {}".format(self.meanExecTime))
        if plot:
            self.plotEfficency(execTimes)
        return self

    def plotEfficency(self,execTimes):
        # pylint: disable=no-member,unused-variable
        fig,ax = plt.subplots(figsize = (15,3))
        ax.plot(execTimes)
        ax.set_xticklabels([str(i/5.) for i in range(6)])
        ax.set_xticks([i for i in range(0,101,20)])
        ax.set_xlabel('u')
        ax.set_ylabel('Execution time')
        ax.legend(loc = 'best')
        plt.suptitle('Runtime execution times')
        return self




