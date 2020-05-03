import matplotlib.pyplot as plt
import numpy as np

def plot(funcs,
         x_lim,
         y_lim,
         labels,
         cumfuncs=[],
         conds=[],
         dist = True,
         ax = None,
         ls = '--',
         npoints = 50
        ):
    '''
    Plot a distribution function and
    cumulative function piecewise
    '''
    if (dist and len(funcs) != len(cumfuncs)):
        raise ValueError("Give all the goddamned functions.")
    # pylint: disable=no-member,unused-variable
    # Make equally separated numbers and plot
    x = np.linspace(x_lim[0],x_lim[1],npoints)
    # Setting the figure
    if ax is None:
        fig,ax = plt.subplots(figsize=(12,6))
    # Draw all xticks
    nfuncs = len(funcs)

    # set a BEAUTIFUL COLOR MAP
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.gist_rainbow(np.linspace(0, 1, nfuncs*2))))
    # plot every line unless its an int because matplotlib DOES NOT LIKE THAT
    i = 0
    for f in funcs + cumfuncs:
        if type(f) is not int:
            ax.plot(x,f(x),ls=ls,alpha=0.8,label = labels[i])
            i +=1
    if dist:
        # distribution function
        x = np.linspace(x_lim[0],x_lim[1])
        f = np.piecewise(x, conds, funcs)
        ax.fill_between(x, 0, f,alpha=0.1,color='k',label='f(x)')
        ax.plot(x,f,'k')

        # Cummulative
        x = np.linspace(x_lim[0],x_lim[1])
        cF = np.piecewise(x ,conds, cumfuncs)
        ax.plot(x,cF,'k',linewidth=3,label='F(x)')

    
    ax.set_xticks( range(x_lim[0],x_lim[1]) )      
    # Set y limits
    ax.set_xlim(x_lim[0],x_lim[1])
    ax.set_ylim(y_lim[0],y_lim[1])
    # Plot horizontal line at 1
    ax.axhline(y=1, color='k',alpha=0.3,linestyle='--')
    # Plot cartesian ax
    ax.axvline(x=0,color='k')
    ax.axhline(y=0,color='k')
    # Acommodate the x and y axis to be set on zero
    #ax.spines['left'].set_position('zero')
    #ax.spines['bottom'].set_position('zero')
    ax.legend(loc='best')

    # show the plot
    plt.show()
    return(ax)