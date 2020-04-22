
from timeit import timeit
import matplotlib.pyplot as plt
import numpy as np

def runTimeCalc(func,nRuns):
    '''
    Given a function, and a number of times to run it,
    returns a 100 element array with the runtimes
    of running the function nRuns times
    '''
    execTimes = []
    print("Calculating exectime",end='')
    for i in range(100):
        if i % 10 == 0:
            print(".",end='')
        # Calculate the execTime for nRums executions
        execTime =timeit(
            func,
            number= nRuns,
            globals= globals()
            )
        execTimes.append(execTime)
    print('Done')
    return execTimes



def plotExTimes(execTimesDict):
    '''
    Given a dict funcname:executiontimesarray 
    plots all the functions in the same plot
    '''
    # Make a colormap to plot the lines in different colors
    # pylint: disable=no-member,unused-variable
    num_plots = len(execTimesDict)
    fig,ax = plt.subplots(figsize = (15,3))
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.gist_rainbow(np.linspace(0, 1, num_plots))))
    for fname,exTime in execTimesDict.items():
        ax.plot(exTime,label = fname)
    ax.set_xticklabels([str(i/5.) for i in range(6)])
    ax.set_xticks([i for i in range(0,101,20)])
    ax.set_xlabel('u')
    ax.set_ylabel('Execution time')

    ax.legend(loc = 'best')

    plt.suptitle('Runtime execution times')
