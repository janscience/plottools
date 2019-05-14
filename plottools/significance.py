"""
# Significance

Indicating statsitical significance.

- `significance_bar()`: horizontal bar with asterisks indicating significance level.

"""

import matplotlib as mpl


def significance_bar(ax, p, x0, x1, y, **kwargs):
    """
    A horizontal bar with asterisks indicating significance level.
    
    Plot a horizontal bar from x0 to x1 at height y
    for indicating significance. On top of the bar plot
    asterisks according to the significance value p are drawn.
    If p > 0.05 nothing is plotted.
    p<0.001: '***', p<0.01: '**', p<0.05: '*'.

    Note: call this function AFTER ylim has been set!

    Parameters
    ----------
    ax: matplotlib axes
        Axes to which the inset is added.
    p: float
        Significance level.
    x0: float
        x-coordinate of starting point of significance bar in data units.
    x1: float
        x-coordinate of ending point of significance bar in data units.
    y: float
        y-coordinate of significance bar in data units.
    kwargs: key-word arguments
        Passed on to ax.text() used to print the asterisks.
    """
    # set label:
    if p < 0.001:
        ps = '***'
    elif p < 0.01:
        ps = '**'
    elif p < 0.05:
        ps = '*'
    else:
        return
    # ax dimensions:
    pixely = np.abs(np.diff(ax.get_window_extent().get_points()[:,1]))[0]
    unity = np.abs(np.diff(ax.get_ylim()))[0]
    dyu = unity/pixely
    fs = mpl.rcParams['font.size']
    if 'fontsize' in kwargs and isinstance(kwargs['fontsize'], (float, int)):
        fs = kwargs['fontsize']
    dy = 0.3*fs*dyu
    lw = 1.0
    lh = ax.plot([x0, x0, x1, x1], [y-dy, y, y, y-dy], color='black', lw=lw,
                 solid_capstyle='butt', solid_joinstyle='miter', clip_on=False)
    # get y position of line in figure pixel coordinates:
    ly = np.array(lh[0].get_window_extent(ax.get_figure().canvas.get_renderer()))[1,1]
    th = ax.text(0.5*(x0+x1), y, ps, ha='center', va='bottom', **kwargs)
    ty = np.array(th.get_window_extent(ax.get_figure().canvas.get_renderer()))[0,1]
    dty = ly+0.5*lw -0.4*fs - ty
    th.set_position((0.5*(x0+x1), y+dty*dyu))
    

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    x1 = 1.0+0.3*np.random.randn(50)
    x2 = 4.0+0.5*np.random.randn(50)
    ax.boxplot([x1, x2])
    ax.set_xlim(0.5, 2.5)
    ax.set_ylim(0.0, 8)
    significance_bar(ax, 0.002, 1, 2, 6)
    plt.show()
