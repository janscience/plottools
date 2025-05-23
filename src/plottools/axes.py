"""
Setting axes appearance.


## Axes member functions

- `set_arrow_style()`: turn the axes into arrows through the origin.



## Figure member functions

Same functions as the ones for the Axes. Functions are called on all
figure axes.

- `set_arrow_style()`: turn the axes into arrows through the origin. 


## Settings

- `axes_params()`: set rc settings for axes.


## Install/uninstall axes functions

You usually do not need to call these functions. Upon loading the axes
module, `install_axes()` is called automatically.

- `install_axes()`: install functions of the axes module in matplotlib.
- `uninstall_axes()`: uninstall all code of the axes module from matplotlib.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def set_arrow_style(ax, spines='lb', xpos=0, ypos=0):
    """Turn the axes into arrows through the origin.

    Note: Call this function *after* you have set the xlabel and ylabel.

    Parameters
    ----------
    ax: matplotlib figure, matplotlib axis, or list of matplotlib axes
        Axes whose style is changed.
        If figure, then apply manipulations on all axes of the figure.
        If list of axes, apply manipulations on each of the given axes.
    spines: str
        String specifying which spines should be turned into arrows ('lrbt').
    xpos: float
        Position of the verical axis ('lr') on the x-axis.
    ypos: float
        Position of the horizontal axis ('bt') on the y-axis.
    """
    # collect axes:
    if isinstance(ax, (list, tuple, np.ndarray)):
        axs = ax
    elif hasattr(ax, 'get_axes'):
        # ax is figure:
        axs = ax.get_axes()
    else:
        axs = [ax]
    if not isinstance(axs, (list, tuple)):
        axs = [axs]
    for ax in axs:
        show_spines = ''
        if ax.spines['top'].get_visible():
            show_spines += 't'
        if ax.spines['bottom'].get_visible():
            show_spines += 'b'
        if ax.spines['left'].get_visible():
            show_spines += 'l'
        if ax.spines['right'].get_visible():
            show_spines += 'r'
        ax.set_spines_outward(spines, 0)
        xspines = ''
        yspines = ''
        for s in spines:
            if s in 'bt':
                xspines += s
                if s == 'b':
                    show_spines = show_spines.replace('t', '')
                elif s == 't':
                    show_spines = show_spines.replace('b', '')
                ax.arrow_spines(s, flush=0, extend=0)
            elif s in 'lr':
                yspines += s
                if s == 'l':
                    show_spines = show_spines.replace('r', '')
                elif s == 'r':
                    show_spines = show_spines.replace('l', '')
                ax.arrow_spines(s, flush=0, extend=1)
        ax.show_spines(show_spines)
        if xspines:
            ax.set_spines_zero(xspines, ypos)
            label = ax.xaxis.get_label()
            x, y = label.get_position()
            label.set_position([1, y])
            label.set_horizontalalignment('right')
            ax.xaxis.set_tick_params(direction='inout',
                                     length=2*plt.rcParams['xtick.major.size'])
        if yspines:
            ax.set_spines_zero(yspines, xpos)
            label = ax.yaxis.get_label()
            x, y = label.get_position()
            label.set_position([x, 1])
            label.set_rotation(0)
            label.set_horizontalalignment('right')
            ax.yaxis.set_tick_params(direction='inout', labelrotation=0,
                                     length=2*plt.rcParams['ytick.major.size'])
                 

def axes_params(xmargin=None, ymargin=None, zmargin=None, color=None,
                spinecolor=None, spinewidth=None):
    """ Set rc settings for axes.

    Only parameters that are not `None` are updated.

    Parameters
    ----------
    xmargin: float
        Padding added to x-axis limits in fractions of the data interval.
        Sets rcParam `axes.xmargin`.
    ymargin: float
        Padding added to y-axis limits in fractions of the data interval.
        Sets rcParam `axes.ymargin`.
    zmargin: float
        Padding added to z-axis limits in fractions of the data interval.
        Sets rcParam `axes.zmargin`.
    color: matplotlib color or 'none'
        Background color for each subplot.
        Sets rcParam `axes.facecolor`.
        For setting the backround color of a given axes, use
        ```
        ax.set_facecolor(color)
        ```
    spinecolor: matplotlib color or 'none'
        Color of the spines.
        Sets rcParam `axes.edgecolor`.
    spinewidth: float
        Line width of the spines.
        Sets rcParam `axes.linewidth`.
    """
    if xmargin is not None:
        mpl.rcParams['axes.xmargin'] = xmargin
    if ymargin is not None:
        mpl.rcParams['axes.ymargin'] = ymargin
    if 'axes.zmargin' in mpl.rcParams and zmargin is not None:
        mpl.rcParams['axes.zmargin'] = zmargin
    if color is not None:
        mpl.rcParams['axes.facecolor'] = color
    if spinecolor is not None:
        mpl.rcParams['axes.edgecolor'] = spinecolor
    if spinewidth is not None:
        mpl.rcParams['axes.linewidth'] = spinewidth


def install_axes():
    """ Install functions of the axes module in matplotlib.

    This function is called automatically upon importing the module.

    Adds the set_arrow_style() function to matplotlib.Axes.

    See also
    --------
    uninstall_axes()
    """
    # make functions available as members:
    if not hasattr(mpl.axes.Axes, 'set_arrow_style'):
        mpl.axes.Axes.set_arrow_style = set_arrow_style


def uninstall_axes():
    """ Uninstall all code of the axes module from matplotlib.

    See also
    --------
    install_axes()
    """
    # remove installed members:
    if hasattr(mpl.axes.Axes, 'set_arrow_style'):
        delattr(mpl.axes.Axes, 'set_arrow_style')

                
install_axes()


def demo():
    """ Run a demonstration of the axes module.
    """
    from .spines import spines_params
    axes_params(xmargin=0, ymargin=0, spinecolor='gray', spinewidth=2)
    fig, ax = plt.subplots()
    fig.suptitle('plottools.axes')
    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')
    ax.text(0.05, 0.7, 'axes_params(xmargin=0, ymargin=0, spinecolor="gray", spinewidth=2)', transform=ax.transAxes)
    ax.set_arrow_style()
    plt.show()
        

if __name__ == "__main__":
    demo()
