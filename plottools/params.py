"""
Default rc param settings for all modules.


You actually do not need to import this module. Rather use one of its
functions as a template. Copy it to your own module and adapt it to your
needs.


## Default parameters and plot styles

- `screen_style()`: layout and plot styles optimized for display on a screen.
- `paper_style()`: layout and plot styles optimized for inclusion into a paper.
- `sketch_style()`: layout and plot styles with xkcd style activated.


## Settings

- `plot_params()`: set some default plot parameter via matplotlib's rc settings.
"""

import __main__
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from .plottools import *


def plot_params(axes_color='none', namespace=None):
    """ Set some default plot parameter via matplotlib's rc settings.

    Call this function *before* you create any matplotlib figure.

    Parameters
    ----------
    axes_color: matplotlib color specification or 'none'
        Background color for each subplot.
    namespace: dict
        Namespace to which generated line, point, linepoint and fill styles were added.
        If None use the global namespace of the __main__ module.
        `lsSpine` and `lsGrid` of the namespace are used to set spine and grid properties.
    """
    if namespace is None:
        namespace = __main__
    # axes, label, ticks and text color:
    mpl.rcParams['axes.facecolor'] = axes_color
    if hasattr(namespace, 'lsSpine'):
        mpl.rcParams['axes.linewidth'] = getattr(namespace, 'lsSpine')['linewidth']
        mpl.rcParams['axes.edgecolor'] = getattr(namespace, 'lsSpine')['color']
        mpl.rcParams['axes.labelcolor'] = mpl.rcParams['axes.edgecolor']
        mpl.rcParams['xtick.color'] = mpl.rcParams['axes.edgecolor']
        mpl.rcParams['ytick.color'] = mpl.rcParams['axes.edgecolor']
        mpl.rcParams['text.color'] = mpl.rcParams['axes.edgecolor']
    # grid style:
    if hasattr(namespace, 'lsGrid'):
        mpl.rcParams['grid.color'] = getattr(namespace, 'lsGrid')['color']
        mpl.rcParams['grid.linestyle'] = getattr(namespace, 'lsGrid')['linestyle']
        mpl.rcParams['grid.linewidth'] = getattr(namespace, 'lsGrid')['linewidth']


def screen_style(namespace=None):
    """ Layout and plot styles optimized for display on a screen.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:
    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit, e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - a range of line, point, linepoint and fill styles defined in `namespace`, called
      A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:
      ```py
      ax.plot(x, y, **lsA1)   # major line only
      ax.plot(x, y, **lsB2m)  # minor line only
      ax.plot(x, y, **psA2)   # markers (points) only
      ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
      ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
      ```
      See `plot_styles()` for details. 
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.

    Parameters
    ----------
    namespace: dict
        Namespace to which the generated line, point, linepoint and fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    if namespace is None:
        namespace = __main__
    lwthick=2.5
    lwthin=1.5
    generic_styles(colors='vivid', lwthick=lwthick, lwthin=lwthin,
                   markerlarge=10.0, markersmall=6.5, mec=0.0, mew=1.5,
                   fillalpha=0.4, namespace=namespace)
    lwspines=1.0    
    make_linestyles('ls', 'Spine', '', palette['black'], '-', lwspines,
                    namespace, clip_on=False)
    make_linestyles('ls', 'Grid', '', palette['gray'], '--', lwthin, namespace)
    make_linestyles('ls', 'Marker', '', palette['black'], '-', lwthick,
                    namespace, clip_on=False)
    generic_arrow_styles(namespace.palette, 1.3)
    # rc settings:
    mpl.rcdefaults()
    align_params(xdist=5, ydist=10)
    axes_params(xmargin=0, ymargin=0)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    colors_params(palette, cycle_colors, cmap='RdYlBu')
    figure_params(color=palette['gray'], format='png',
                  compression=6, fonttype=3, stripfonts=False)
    labels_params(lformat='{label} [{unit}]', label_size='medium')
    legend_params(fontsize='small', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5,
                  numpoints=1, scatterpoints=1, labelspacing=0.5, columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f',
                    lw=2, color=palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lbrt', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'})
    tag_params(xoffs='auto', yoffs='auto', label='%A', minor_label='%A%mi',
               font=dict(fontsize='x-large', fontstyle='normal', fontweight='normal'))
    text_params(font_size=11.0, font_family='sans-serif')
    ticks_params(tick_dir='out', tick_size=4.0)
    plot_params(axes_color=palette['white'], namespace=namespace)

    
def paper_style(namespace=None):
    """ Layout and plot styles optimized for inclusion into a paper.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:
    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit, e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - a range of line, point, linepoint and fill styles defined in `namespace`, called
      A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:
      ```py
      ax.plot(x, y, **lsA1)   # major line only
      ax.plot(x, y, **lsB2m)  # minor line only
      ax.plot(x, y, **psA2)   # markers (points) only
      ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
      ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
      ```
      See `plot_styles()` for details. 
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.

    Parameters
    ----------
    namespace: dict
        Namespace to which the generated line, point, linepoint and fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    if namespace is None:
        namespace = __main__
    lwthick=1.7
    lwthin=0.8
    generic_styles(colors='muted', lwthick=lwthick, lwthin=lwthin,
                   markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                   fillalpha=0.4, namespace=namespace)
    lwspines=0.8    
    make_linestyles('ls', 'Spine', '', palette['black'], '-', lwspines, namespace, clipon=False)
    make_linestyles('ls', 'Grid', '', palette['gray'], '--', lwthin, namespace)
    make_linestyles('ls', 'Marker', '', palette['black'], '-', lwthick, namespace, clipon=False)
    generic_arrow_styles(namespace.palette, 1.0)
    # rc settings:
    mpl.rcdefaults()
    align_params(xdist=5, ydist=10)
    axes_params(xmargin=0, ymargin=0)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    colors_params(palette, cycle_colors, cmap='RdYlBu')
    figure_params(color='none', format='pdf',
                  compression=6, fonttype=3, stripfonts=False)
    labels_params(lformat='{label} [{unit}]', label_size='small')
    legend_params(fontsize='small', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5,
                  numpoints=1, scatterpoints=1, labelspacing=0.5, columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f',
                    lw=2, color=palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lbrt', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'})
    tag_params(xoffs='auto', yoffs='auto', label='%A', minor_label='%A%mi',
               font=dict(fontsize='x-large', fontstyle='normal', fontweight='normal'))
    text_params(font_size=10.0, font_family='sans-serif')
    ticks_params(tick_dir='out', tick_size=2.5)
    plot_params(axes_color='none', namespace=namespace)
    
   
def sketch_style(namespace=None):
    """ Layout and plot styles with xkcd style activated.

    You might want to copy this function and adjust it according to your needs.

    Call this function *before* you create any matplotlib figure
    to have the following features in effect:
    - modified rc settings.
    - figure sizes are to be specified in centimeter.
    - detailed control over spine appearance.
    - xlabel and ylabel with separately specified unit, e.g. `set_xlabel('Time', 'ms')`.
    - automatic alignment of x- and ylabels.
    - a range of line, point, linepoint and fill styles defined in `namespace`, called
      A1-A3, B1-B4, C1-C4, Male, Female, that can be used as follows:
      ```py
      ax.plot(x, y, **lsA1)   # major line only
      ax.plot(x, y, **lsB2m)  # minor line only
      ax.plot(x, y, **psA2)   # markers (points) only
      ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
      ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
      ```
      See `plot_styles()` for details. 
    - `lsSpine`, `lsGrid`, `lsMarker` line styles defined in `namespace`.

    Parameters
    ----------
    namespace: dict
        Namespace to which the generated line, point, linepoint and fill styles are added.
        If None add styles to the global namespace of the __main__ module.
    """
    #global bar_fac
    #bar_fac = 0.9
    if namespace is None:
        namespace = __main__
    lwthick=3.0
    lwthin=1.8
    generic_styles(colors='vivid', lwthick=lwthick, lwthin=lwthin,
                   markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                   fillalpha=0.4, namespace=namespace)
    lwspines=1.8    
    make_linestyles('ls', 'Spine', '', palette['black'], '-', lwspines, namespace, clipon=False)
    make_linestyles('ls', 'Grid', '', palette['gray'], '--', lwthin, namespace)
    make_linestyles('ls', 'Marker', '', palette['black'], '-', lwthick, namespace, clipon=False)
    generic_arrow_styles(namespace.palette, 1.3)
    # rc settings:
    mpl.rcdefaults()
    plt.xkcd()
    align_params(xdist=5, ydist=10)
    axes_params(xmargin=0, ymargin=0)
    cycle_colors = ['blue', 'red', 'orange', 'lightgreen', 'magenta', 'yellow', 'cyan', 'pink']
    colors_params(palette, cycle_colors, cmap='RdYlBu')
    figure_params(color='none', format='pdf',
                  compression=6, fonttype=3, stripfonts=False)
    labels_params(lformat='{label} ({unit})', label_size='medium')
    legend_params(fontsize='medium', frameon=False, borderpad=0,
                  handlelength=1.5, handletextpad=0.5,
                  numpoints=1, scatterpoints=1, labelspacing=0.5, columnspacing=0.5)
    scalebar_params(format_large='%.0f', format_small='%.1f',
                    lw=2, color=palette['black'], capsize=0, clw=0.5)
    spines_params(spines='lb', spines_offsets={'lrtb': 0}, spines_bounds={'lrtb': 'full'})
    tag_params(xoffs='auto', yoffs='auto', label='%A', minor_label='%A%mi',
               font=dict(fontsize='x-large', fontstyle='normal', fontweight='normal'))
    text_params(font_size=10.0, font_family='sans-serif')
    ticks_params(tick_dir='out', tick_size=6)
    plot_params(axes_color='none', namespace=namespace)
        

def demo(style='screen'):
    """ Run a demonstration of the params module.

    Parameters
    ----------
    style: string
        'screen', 'print', or 'sketch': style to use.
    """
    if style == 'sketch':
        sketch_style(sys.modules[__name__])
    elif style == 'paper':
        paper_style(sys.modules[__name__])
    else:
        style = 'screen'
        screen_style(sys.modules[__name__])
    fig, ax = plt.subplots()
    fig.suptitle('plottools.params')
    x = np.linspace(0, 20, 200)
    y = np.sin(x)
    ax.plot(x, y, **lsA1)
    ax.text(0.1, 0.9, '%s_style()' % style, transform=ax.transAxes)
    ax.text(0.1, 0.8, 'ax.plot(x, y, **lsA1)', transform=ax.transAxes)
    ax.set_ylim(-1.2, 2.0)
    plt.show()


if __name__ == "__main__":
    style = 'screen'
    if len(sys.argv) > 1:
        style = sys.argv[1]
    demo(style)