import matplotlib.pyplot as plt
import numpy as np

def plot(funcs,cumfuncs,conds,x_lim,y_lim,labels):
    '''
    Plot a distribution function and
    cumulative function piecewise
    '''
    if (len(funcs) != len(cumfuncs)):
        raise ValueError("Give all the goddamned functions.")
    # pylint: disable=no-member,unused-variable
    # Make equally separated numbers and plot
    x = np.linspace(x_lim[0],x_lim[1])
    # Setting the figure

    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(1, 1, 1)
    # Draw all xticks
    plt.xticks( range(x_lim[1]) )      
    # Set y limits
    plt.xlim(x_lim[0],x_lim[1])
    plt.ylim(y_lim[0],y_lim[1])
    # Plot horizontal line at 1
    plt.axhline(y=1, color='k', linestyle='--')

    nfuncs = len(funcs)

    # set a BEAUTIFUL COLOR MAP
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.gist_rainbow(np.linspace(0, 1, nfuncs*2))))
    # plot every line unless its an int because matplotlib DOES NOT LIKE THAT
    i = 0
    for f in funcs + cumfuncs:
        if type(f) is not int:
            plt.plot(x,f(x),ls='--',alpha=0.8,label = labels[i])
            i +=1

    # distribution function
    x = np.linspace(x_lim[0],x_lim[1])
    f = np.piecewise(x, conds, funcs)
    ax.fill_between(x, 0, f,alpha=0.1,color='k',label='f(x)')
    plt.plot(x,f,'k')

    # Cummulative
    x = np.linspace(x_lim[0],x_lim[1])
    cF = np.piecewise(x ,conds, cumfuncs)
    plt.plot(x,cF,'k',linewidth=3,label='F(x)')

    ax.legend(loc='upper left')

    # show the plot
    plt.show()
