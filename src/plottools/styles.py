"""Plotting styles.


Usually you specify the line style for a plot command like this:

```py
ax.plot(x, y, color='#aa0000', lw=2, ls='--')
```

This way to define the appearance of the plotted line, however, has a
number of disadvantages:

1. Specifying the keyword arguments is quite lengthy, it is a lot to
   type and distracts the reader of your code from what you actually
   want to plot.
2. When you want to change the design of all your plots, you need to
   change this everywhere. For this reason I bet you really do not
   want to change any colors and line widths in your plots any more,
   which is sad.

To address the first issue, you may put all the keyword arguments
specifying the line style into a dictionary, like this:

```py
lsRed = dict(color='#aa0000', lw=2, ls='--')  # red line style (ls)
ax.plot(x, y, **lsRed)
```

The keyword expansion operator is such a powerful feature of python!

We here call such dictionaries with keyword arguments defining how
something is plotted *"plotting styles"*.  With plotting styles plot
commands are much more expressive and better readable.

Even better is to give the plotting styles functional names, like, for
example, `lsStimulus` or `lsResponse`. This way you make sure, that in
all your plots, the same things really appear in the same styles.

To address the second issue, you simply collect all plotting styles in
a module that you then import in all plotting scripts. Alternatively a
central function could add all plotting styles to some
namespace. Doing so makes your plot scripts sweet and short.

So, this is how your central module, named "plotstyles.py" might look
like:
```py
def plot_styles():
    class s: pass    # namespace `s`
    s.lsRed = dict(color='#aa0000', lw=2, ls='--')
    s.lsStimulus = dict(color='#00bb00', lw=1, ls='-')
    s.lsResponse = dict(color='#aa0000', lw=1, ls='-')
    return s
```
Then, a script producing a figure looks like this:
```py
import matplotlib.pyplot as plt
from plotstyles import plot_styles

s = plot_styles()
fig, ax = plt.subplots()
ax.plot(x, y, **s.lsResponse)
fig.savefig('example.pdf')
```

This way you can change the appearance of *all* your figures by
modifying the plotting styles in a single central file/function. You
can first code your figures and concentrate on the technicalities of
the data. And later on, when you are done, you then can easily improve
the design of your plots.

Plotting styles used in this way are a central element for separating
content from design. Python's keyword arguments and namespaces
provide nice mechanisms to achieve this.

The `styles` module provides a few functions that help you with
generating and organizing plotting styles.

In your central "plotstyle.py" module you can, of course, also import
all the cool plottool modules you need, or just the
`plottools.plottools` module to get and install them all. You also
should set matplotlib's `rcParams` variables to define the appearance
of your plots in this central place. Alternatively you can use the
respective `_params()` functions of the plottools modules.


## Duplicate and modify plotting styles

- `style()`: copy and update a style.
- `lighter_styles()`: duplicate style with a range of lighter colors.
- `darker_styles()`: duplicate style with a range of darker colors.
- `lighter_darker_styles()`: duplicate style with a range of lighter and darker colors.


## Generate plotting styles

- `make_line_styles()`: generate line styles.
- `make_point_styles()`: generate point styles.
- `make_linepoint_styles()`: generate line styles, point styles, and line point styles.
- `make_fill_styles()`: generate fill styles.
- `make_linepointfill_styles()`: generate line styles, point styles, line point styles, and fill styles from names, dashes, colors, and markers.
- `generic_styles()`: generates some generic line, points, linepoints and fill styles.


## Display plotting styles

- `plot_line_styles()`: plot names and lines of all available line styles.
- `plot_point_styles()`: plot names and markers of all available point styles.
- `plot_linepoint_styles()`: plot names, lines, and markers of all available linepoint styles.
- `plot_fill_styles()`: plot names and patches of all available fill styles.
"""

import __main__
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from .colors import palettes, lighter, darker


def style(orig_style, **kwargs):
    """Copy and update a style.

    Parameters
    ----------
    orig_style: dict
        Plotting-style dictionary holding keyword arguments like
        `linewidth` and `color` or `facecolor` for plotting.
    kwargs: dict
        Keyword arguments used to update keys in `orig_style`.

    Returns
    -------
    new_style: dict
        Plotting style dictionary as a copy of `orig_style`, updated
        by the keyword arguments provided by `kwargs`.

    See Also
    --------
    lighter_styles(), darker_styles(), lighter_darker_styles()

    Examples
    --------
    ```py
    lsRed = dict(color='red', linewidth=1, linestyle='-')
    lsBlue = style(lsRed, color='blue')
    ax.plot(x, y, **lsRed)
    ax.plot(x, z, **lsBlue)
    ```
    """
    new_style = dict(orig_style)
    new_style.update(**kwargs)
    return new_style

    
def lighter_styles(style, n):
    """Duplicate style with a range of lighter colors.

    Parameters
    ----------
    style: dict
        Plotting-style dictionary holding keyword arguments like
        `linewidth` and `color` or `facecolor` for plotting.
    n: int
        Number of lighter colors to be generated (`n>1`).

    Returns
    -------
    styles: list of dict
        `n` copies of `style` with increasingly lighter `color` or
        `facecolor`.  The first style in the list is a copy of the
        original one.

    See Also
    --------
    style(), darker_styles(), lighter_darker_styles()

    Examples
    --------
    Suppose you have a style for blue lines like
    ```py
    lsBlue = dict(color='blue', lw=2)
    ```
    Now you need five variants of this plot style with increasingly
    lighter colors. Just call
    ```py
    lsBlues = lighter_styles(lsBlue, 5)
    ```
    and you can do something like
    ```py
    for k, ls in enumerate(lsBlues):
        ax.plot(x, y+0.5*k, **ls)
    ```
    """
    for ck in ['color', 'facecolor']:
        if ck in style:
            c = style[ck]
            styles = []
            for k in range(n):
                sd = dict(**style)
                sd[ck] = lighter(c, 1.0-k/n)
                styles.append(sd)
            return styles
    return [style]*n


def darker_styles(style, n):
    """Duplicate style with a range of darker colors.

    Parameters
    ----------
    style: dict
        Plotting-style dictionary holding keyword arguments like
        `linewidth` and `color` or `facecolor` for plotting.
    n: int
        Number of darker colors to be generated (`n>1`).

    Returns
    -------
    styles: list of dict
        `n` copies of `style` with increasingly darker `color` or
        `facecolor`.  The first style in the list is a copy of the
        original one.

    See Also
    --------
    style(), lighter_styles(), lighter_darker_styles()

    Examples
    --------
    Suppose you have a style for green lines in a plot like
    ```py
    lsGreen = dict(color='green', lw=2)
    ```
    Now you need 4 variants of this plot style with increasingly
    darker colors.  Just call
    ```py
    lsGreens = darker_styles(lsGreen, 4)
    ```
    and you can do something like
    ```py
    for k, ls in enumerate(lsGreens):
        ax.plot(x, y+0.5*k, **ls)
    ```
    """
    for ck in ['color', 'facecolor']:
        if ck in style:
            c = style[ck]
            styles = []
            for k in range(n):
                sd = dict(**style)
                sd[ck] = darker(c, 1.0-k/n)
                styles.append(sd)
            return styles
    return [style]*n


def lighter_darker_styles(style, n):
    """Duplicate style with a range of lighter and darker colors.

    Parameters
    ----------
    style: dict
        Plotting-style dictionary holding keyword arguments like
        `linewidth` and `color` or `facecolor` for plotting.
    n: int
        Number of modified colors to be generated (`n>1`).

    Returns
    -------
    styles: list of dict
        `n` copies of `style` with `color` or `facecolor` starting
        from a lighter color, traversing over the original color to
        darker colors.  The central style is a copy of the original
        color if `n` is odd.

    See Also
    --------
    style(), lighter_styles(), darker_styles()

    Example
    -------
    Suppose you have a style for blue lines in a plot like
    ```py
    lsBlue = dict(color='blue', lw=2)
    ```
    Now you need 5 variants of this plot style with lighter and darker colors.
    Just call
    ```py
    lsBlues = lighter_darker_styles(lsBlue, 5)
    ```
    and you can do something like
    ```py
    for k, ls in enumerate(lsBlues):
        ax.plot(x, y+0.5*k, **ls)
    ```
    """
    for ck in ['color', 'facecolor']:
        if ck in style:
            c = style[ck]
            styles = []
            for k in range(n):
                sd = dict(**style)
                sd[ck] = lighter(c, 1+(k-(n-1)/2)/((n+1)//2))
                styles.append(sd)
            return styles
    return [style]*n


def make_line_styles(namespace, prefix, names, suffix, colors,
                     dashes='-', lws=1, **kwargs):
    """Generate line styles.

    The generated dictionaries can be passed as keyword arguments to
    `ax.plot()` commands.  For each corresponding name, color, line
    style and line width a dictionary is generated holding these
    attributes. The generated dictionaries are named
    `prefix + name + suffix`, and are additionally added to the
    `prefix + suffix` dictionary in the given namespace. 
    `name` is also added to the `style_names` list in the namespace.

    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated line styles are added.
        If None add line styles to the `__main__` module.
    prefix: string
        Prefix prepended to all line style names.
    names: string or list of strings
        Names of the line styles.
        If string and a '%' is contained, then formats like '%d' are replaced
        by the index of the line style plus one.
    suffix: string or list of strings
        Sufffix appended to all line style names.
    colors: matplotlib color or list of matplotlib colors
        Colors of the line styles.
    dashes: matplotlib linestyle or list of matplotlib linestyles
        Dash styles of the connecting lines.
    lws: float or list of floats
        Widths of the connecting lines.
    kwargs: dict
        Keyword arguments with further line properties, e.g. alpha, zorder.

    See Also
    --------
    make_point_styles(), plot_line_styles()

    Examples
    --------
    ```py
    class s: pass
    make_line_styles(s, 'ls', 'Male', '', 'blue', '-', 2)
    ```
    generates a dictionary in the `s` namespace named `lsMale`
    defining a blue solid line, adds `Male` to the `style_names` list,
    and adds the `lsMale` dictionary to `ls` under the key `Male`.
    Simply throw the dictionary into a `plot()` command:
    ```py
    plt.plot(x, y, **s.lsMale)
    ```
    or
    ```py
    plt.plot(x, y, **s.ls['Male'])
    ```
    this is the same as:
    ```py
    plt.plot(x, y, '-', color='blue', lw=2)
    ```
    but is more expressive and can be changed at a single central place.

    This
    ```py
    class s: pass
    make_line_styles(s, 'ls', ['Red', 'Green'], '', ['r', 'g'],
                     ['-', '--'], 0.5)
    ```
    adds two line styles `lsRed` and `lsGreen` to the `s` namespace
    with the respective colors and a thin solid or dashed line,
    respectively.
    """
    # prepare dictionaries:
    if namespace is None:
        namespace = __main__
    if not hasattr(namespace, 'style_names'):
        namespace.style_names = []
    if not isinstance(suffix, (tuple, list)):
        suffix = [suffix]
    for sf in suffix:
        ln = prefix + sf 
        if not hasattr(namespace, ln):
            setattr(namespace, ln, {})
    # number of line styles to be generated:
    n = 1
    for x in (names, suffix, colors, dashes, lws):
        if isinstance(x, (tuple, list)) and len(x) > n:
            n = len(x)
    # generate styles:
    for k in range(n):
        if isinstance(names, (tuple, list)) :
            name = names[k]
        else:
            if '%' in names:
                name = names % (k+1)
            else:
                name = names
        if name not in namespace.style_names:
            namespace.style_names.append(name)
        sf = suffix[k%len(suffix)]
        c = colors[k] if isinstance(colors, (tuple, list)) else colors
        ds = dashes[k] if isinstance(dashes, (tuple, list)) else dashes
        lw = lws[k] if isinstance(lws, (tuple, list)) else lws
        ld = dict(color=c, linestyle=ds, linewidth=lw, **kwargs)
        setattr(namespace, prefix + name + sf, ld)
        getattr(namespace, prefix + sf)[name] = ld


def make_point_styles(namespace, prefix, names, suffix, colors,
                      dashes='none', lws=0, markers=('o', 1.0),
                      markersizes=5.0, markeredgecolors=0.0,
                      markeredgewidths=1.0, **kwargs):
    """Generate point styles.

    The generated dictionaries can be passed as keyword arguments to
    `ax.plot()` commands.  For each corresponding name, color, line
    style, line width, marker, marker size, marker edge color, and
    marker edge width a dictionary is generated holding these
    attributes.  The generated dictionaries are named
    `prefix + name + suffix`, and are additionally added to the
    `prefix + suffix` dictionary in the given namespace.
    `name` is also added to the `style_names` list in the namespace.

    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated point styles are added.
        If None add point styles to the `__main__` module.
    prefix: string
        Prefix prepended to all point style names.
    names: string or list of strings
        Names of the line styles.
        If string and a '%' is contained, then formats like '%d' are replaced
        by the index of the line style plus one.
    suffix: string or list of strings
        Sufffix appended to all point style names.
    colors: matplotlib color or list of matplotlib colors
        For each color in the list a point style is generated.
    dashes: matplotlib linestyle or list of matplotlib linestyles
        Dash styles of the connecting lines. If points are not to be
        connected, set to 'none'.
    lws: float or list of floats
        Widths of the connecting lines.
    markers: 2-tuple or list of 2-tuples
        For each point style a marker. The first element of the inner tuple is
        the marker symbol, the second one is a factor that is used to scale
        the marker's size.
    markersizes: float or list of floats
        For each point style a marker size. The marker size is
        multiplied with a factor of the corresponding marker.
    markeredgecolors: float or list of floats
        Defines the edge color for each point style.  It is passed as
        the lightness argument to `lighter()` using the face color
        form `colors`. That is, 0 results in a white edge color, 1 in
        an edge with the same color as the face color, and 2 in a
        black edge color.
    markersizes: float, list of floats
        For each point style a marker edge width.
    kwargs: dict
        Keyword arguments with further marker properties, e.g. alpha, zorder.

    See Also
    --------
    make_line_styles(), plot_point_styles()
    
    Examples
    --------
    ```py
    class s: pass
    make_point_styles(s, 'ps', 'Female', '', 'red', '-', 1, ('o', 1.0),
                      8, 0.5, 1, alpha=0.5)
    ```
    generates a dictionary in the `s` namespace named `psFemale`
    defining transparent red filled markers with a lighter edge, adds
    `Female` to `style_names`, and adds the dictionary to `ps` under
    the key `Female`.  Simply throw the dictionary into a `plot()`
    command:
    ```py
    plt.plot(x, y, **s.psFemale)
    ```
    this is the same as:
    ```py
    plt.plot(x, y, **s.ps['Female'])
    ```
    This
    ```py
    class s: pass
    make_point_styles(s, 'ps', 'Reds%d', 'c', ['red', 'orange', 'yellow'],
                      'none', 0, ('o', 1.0), 8, 1, 0)
    ```
    generates the three point styles 'psReds1', 'psReds2', and
    'psReds3' in the `s` namespace for plotting filled circles with
    colors red, orange, and yellow, respectively.
    """
    # prepare dictionaries:
    if namespace is None:
        namespace = __main__
    if not hasattr(namespace, 'style_names'):
        namespace.style_names = []
    if not isinstance(suffix, (tuple, list)):
        suffix = [suffix]
    for sf in suffix:
        ln = prefix + sf 
        if not hasattr(namespace, ln):
            setattr(namespace, ln, {})
    # number of markers:
    n_markers = 1
    if len(markers) >= 2 and isinstance(markers[1], (tuple, list)):
        n_markers = len(markers)
    # number of line styles to be generated:
    n = 1
    for x in (names, suffix, colors, dashes, lws, markersizes,
              markeredgecolors, markeredgewidths):
        if isinstance(x, (tuple, list)) and len(x) > n:
            n = len(x)
    if n < n_markers:
        n = n_markers
    # generate styles:
    for k in range(n):
        if isinstance(names, (tuple, list)) :
            name = names[k]
        else:
            if '%' in names:
                name = names % (k+1)
            else:
                name = names
        if name not in namespace.style_names:
            namespace.style_names.append(name)
        sf = suffix[k%len(suffix)]
        c = colors[k] if isinstance(colors, (tuple, list)) else colors
        ds = dashes[k] if isinstance(dashes, (tuple, list)) else dashes
        lw = lws[k] if isinstance(lws, (tuple, list)) else lws
        mk = markers[k] if n_markers > 1 else markers
        ms = markersizes[k] if isinstance(markersizes, (tuple, list)) else markersizes
        mc = markeredgecolors[k] if isinstance(markeredgecolors, (tuple, list)) else markeredgecolors
        mw = markeredgewidths[k] if isinstance(markeredgewidths, (tuple, list)) else markeredgewidths
        pd = dict(color=c, linestyle=ds, linewidth=lw, marker=mk[0],
                  markersize=mk[1]*ms, markeredgecolor=lighter(c, mc),
                  markeredgewidth=mw, **kwargs)
        setattr(namespace, prefix + name + sf, pd)
        getattr(namespace, prefix + sf)[name] = pd


def make_linepoint_styles(namespace, prefixes, names, suffix, colors,
                          dashes, lws, markers, markersizes,
                          markeredgecolors, markeredgewidths=1.0,
                          **kwargs):
    """Generate line styles, point styles, and line point styles.

    Passes the arguments on to `make_line_styles()` and twice to
    `make_point_styles()`, once with `dashes='none'` for non-connected
    markers, and once with dashes and line widths for connecting
    lines.  See those functions for a detailed description.

    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated styles are added.
        If None add line styles to the `__main__` module.
    prefixes: list of strings

        - If the first string in the list is not None, generate line
          styles with this prefix using `make_line_styles()`.
        - If the second string in the list is not None, generate point
          styles with this prefix using `make_point_styles()` with
          `dashes` set to 'none'.
        - If the third string in the list is not None, generate
          linepoint styles with this prefix using `make_point_styles()`
          and the supplied `dashes`.

    kwargs: dict
        All remaining arguments are explained in the
        `make_line_styles()` and `make_point_styles()` functions.

    See Also
    --------
    make_line_styles(), make_point_styles(), plot_linepoint_styles(),
    plot_line_styles(), plot_point_styles()
    """
    if namespace is None:
        namespace = __main__
    if prefixes[0]:
        make_line_styles(namespace, prefixes[0], names, suffix,
                         colors, dashes, lws, **kwargs)
    if prefixes[1]:
        make_point_styles(namespace, prefixes[1], names, suffix,
                          colors, 'none', 0, markers, markersizes,
                          markeredgecolors, markeredgewidths, **kwargs)
    if prefixes[2]:
        make_point_styles(namespace, prefixes[2], names, suffix,
                          colors, dashes, lws, markers, markersizes,
                          markeredgecolors, markeredgewidths, **kwargs)


def make_fill_styles(namespace, prefix, names, suffixes, colors,
                     edgecolors=1.0, edgewidths=0.0, fillalphas=1.0,
                     **kwargs):
    """Generate fill styles.

    The generated dictionaries can be passed as keyword arguments to
    `ax.fill_between()` commands.  For each corresponding name, color,
    edge color, edge width and alpha a dictionary is generated holding
    these attributes.  The generated dictionaries are named
    `prefix + name + suffix`, and are additionally added to the
    `prefix + suffix` dictionary in the given namespace.
    `name` is also added to the `style_names` list in the namespace.

    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated fill styles are added.
        If None add fill styles to the `__main__` module.
    prefix: string
        Prefix prepended to all fill style names.
    names: string or list of strings
        Names of the line styles.
        If string and a '%' is contained, then formats like '%d' are replaced
        by the index of the line style plus one.
    suffixes: string or list of strings or None
        A single or multiple sufffixes appended to all fill style
        names.  If a single suffix is specified (it can be empty)
        then a fill style according to all arguments is generated.
        In case of a list of suffixes, the following fill styles are generated:
        The first is for a fill style with edge color, the
        second for a solid fill style without edge, and the third for
        a transparent fill style without edge. If `None` the
        corresponding style is not generated.
    colors: matplotlib color or list of matplotlib colors
        Fill colors.
    edgecolors: float or list of floats
        Defines edge colors for the first fill style.  It is passed as
        the lightness argument to `lighter()` using the face color
        from `colors`. That is, 0 results in a white edge color, 1 in
        an edge with the same color as the face color, and 2 in a
        black edge color.
    edgewidth: float or list of floats
        Widths for the edge color of the first fill style.
    fillalphas: float or list of floats
        Alpha values for the transparent (third) fill style.
    kwargs: dict
        Keyword arguments with further fill properties, e.g. zorder.

    See Also
    --------
    plot_fill_styles(), make_line_styles(), make_point_styles(),
    make_linepoint_styles()
    
    Examples
    --------
    ```py
    class s: pass
    make_fill_styles(s, 'fs', 'PSD', ['', 's', 'a'],
                     ['green'], 2.0, 0.5, 0.4)
    ```
    generates dictionaries in the `s` namespace named `fsPSD`,
    `fsPSDs`, `fsPSDa` defining a green fill color.  The first,
    `fsPSD` gets a black edge color with edge width set to 0.5.  The
    second, `fsPSDs` is without edge.  The third, `fsPSDa` is without
    edge and has alpha set to 0.4.  Further, `PSD` is added to
    `style_names`, and the three dictionaries are added to the `fs`,
    `fss` and `fsa` dictionaries under the key `PSD`.  Simply throw
    the dictionaries into a `fill_between()` command:
    ```py
    plt.fill_between(x, y0, y1, **s.fsPSD)
    ```
    or like this (here for a transparent fill style):
    ```py
    plt.plot(x, y, **s.fsa['PSD'])
    ```

    """
    # prepare dictionaries:
    if namespace is None:
        namespace = __main__
    if not hasattr(namespace, 'style_names'):
        namespace.style_names = []
    single_suffix = not isinstance(suffixes, (tuple, list))
    if single_suffix:
        suffixes = [suffixes]
    for suffix in suffixes:
        if suffix is not None:
            ln = prefix + suffix 
            if not hasattr(namespace, ln):
                setattr(namespace, ln, {})
    # number of line styles to be generated:
    n = 1
    for x in (names, colors, edgecolors, edgewidths, fillalphas):
        if isinstance(x, (tuple, list)) and len(x) > n:
            n = len(x)
    # generate styles:
    for k in range(n):
        if isinstance(names, (tuple, list)) :
            name = names[k]
        else:
            if '%' in names:
                name = names % (k+1)
            else:
                name = names
        if name not in namespace.style_names:
            namespace.style_names.append(name)
        for j, suffix in enumerate(suffixes):
            if suffix is not None:
                sn = prefix + name + suffix
                c = colors[k] if isinstance(colors, (tuple, list)) else colors
                ec = edgecolors[k] if isinstance(edgecolors, (tuple, list)) else edgecolors
                ew = edgewidths[k] if isinstance(edgewidths, (tuple, list)) else edgewidths
                fa = fillalphas[k] if isinstance(fillalphas, (tuple, list)) else fillalphas
                filldict = dict(facecolor=c, **kwargs)
                if j == 0:   # fill with edge:
                    if single_suffix:
                        filldict.update(dict(edgecolor=lighter(c, ec), linewidth=ew, alpha=fa))
                    else:
                        filldict.update(dict(edgecolor=lighter(c, ec), linewidth=ew))
                elif j == 1: # fill without edge:
                    filldict.update(dict(edgecolor='none'))
                elif j == 2: # fill without edge, with alpha:
                    filldict.update(dict(edgecolor='none', alpha=fa))
                setattr(namespace, sn, filldict)
                getattr(namespace, prefix + suffix)[name] = filldict

    
def make_linepointfill_styles(namespace, names, colors, dashes,
                              markers, lwthick=2.0, lwthin=1.0,
                              markerlarge=7.5, markersmall=5.5,
                              mec=0.5, mew=1.0, fillalpha=0.4):
    """Generate line styles, point styles, line point styles, and fill styles from names, dashes, colors, and markers.

    For each color and name a variety of plot styles are generated
    (for the example, names is 'Female'):

    - Major line styles (prefix 'ls', no suffix, e.g. 'lsFemale')
      for normal lines without markers.
    - Minor line styles (prefix 'ls', suffix 'm', e.g. 'lsFemalem')
      for thinner lines without markers.
    - Major point styles (prefix 'ps', no suffix, e.g. 'psFemale')
      for large markers without connecting lines.
    - Major circular point styles (prefix 'ps', suffix 'c', e.g. 'psFemalec')
      for large circular markers without connecting lines.
    - Minor point styles (prefix 'ps', suffix 'm', e.g. 'psFemalem')
      for small circular markers without connecting lines.
    - Major linepoint styles (prefix 'lps', no suffix, e.g. 'lpsFemale')
      for large markers with connecting lines.
    - Major circular linepoint styles (prefix 'lps', suffix 'c',
      e.g. 'lpsFemalec') for large circular markers with connecting
      lines.
    - Minor linepoint styles (prefix 'lps', suffix 'm', e.g. 'lpsFemalem')
      for small circular markers with connecting lines.
    - Fill styles with edge color (prefix 'fs', no suffix, e.g. 'fsFemale')
    - Fill styles with solid fill color and no edge color (prefix
      'fs', suffix 's', e.g. 'fsFemales')
    - Fill styles with transparent fill color and no edge color
      (prefix 'fs', suffix 'a', e.g. 'fsFemalea')
                
    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated styles are added.
        If None add styles to the `__main__` module.
    names: list of strings
        For each color in `colors` a name.
    colors: list of matplotlib colors
        For each color in the list line, point, linepoint, and fill
        styles are generated.
    dashes: matplotlib linestyle or list of matplotlib linestyles
        For each color a descriptor of a matplotlib linestyle
        that is used for line and linepoint styles.
    markers: tuple or list of tuples
        For each color a marker that is used for point and linepoint
        styles.  The first element of the tuple is the marker symbol,
        the second one is a factor that is used to scale the
        marker sizes.
    lwthick: float
        Line width for major line styles.
    lwthin: float
        Line width for minor line styles.
    markerlarge: float
        Marker size for major point styles.
    markersmall: float
        Marker size for minor point styles.
    mec: float
        Edge color for markers and fill styles. A factor between 0 and
        2 passed together with the facecolor to `lighter()`. I.e. 0
        results in a white edge, 1 in an edge of the color of the face
        color, and 2 in a black edge.
    mew: float
        Line width for marker edges and fill styles.
    fillalpha: float
        Alpha value for transparent fill styles.

    See Also
    --------
    make_linepoint_styles(), make_fill_styles(), generic_styles(),
    plot_line_styles(), plot_point_styles(), plot_linepoint_styles(),
    plot_fill_styles()
    """    
    if namespace is None:
        namespace = __main__

    # line, point and linepoint styles:
    make_linepoint_styles(namespace, ['ls', 'ps', 'lps'], names, '',
                          colors, dashes, lwthick, markers,
                          markerlarge, mec, mew)
    # circular point and linepoint styles:
    make_linepoint_styles(namespace, ['', 'ps', 'lps'], names, 'c',
                          colors, dashes, lwthick, ('o', 1.0),
                          markerlarge, mec, mew)
    # minor line, point and linepoint styles:
    make_linepoint_styles(namespace, ['ls', 'ps', 'lps'], names, 'm',
                          colors, dashes, lwthin, ('o', 1.0),
                          markersmall, mec, mew)
    # fill styles:
    make_fill_styles(namespace, 'fs', names, ['', 's', 'a'], colors,
                     mec, mew, fillalpha)

    
def generic_styles(namespace, colors='muted', lwthick=1.7, lwthin=0.8,
                   markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                   fillalpha=0.4):
    """Generates some generic line, points, linepoints and fill styles.
    
    Generates a range of line (ls), point (ps), linepoint (lps) and
    fill (fs) styles defined in `namespace`,
    named A1-A3 (red, orange, yellow), B1-B4 (blues), C1-C4 (greens),
    that can be used as follows:
    ```py
    ax.plot(x, y, **lsA1)   # major line only
    ax.plot(x, y, **lsB2m)  # minor line only
    ax.plot(x, y, **psA2)   # markers (points) only
    ax.plot(x, y, **lpsC3)  # markers (points) with connecting lines
    ax.fill_between(x, y0, y1, **fsA3a) # transparent fill
    ```

    Each style is derived from a main color as indicated by the
    capital letter.  Substyles, indicated by the number following the
    capital letter, have the same style and similar hues.

    Line styles (ls):
    
    - plain style with a thick, solid line (e.g. `lsA1`), and
    - minor style with a thinner line (e.g. `lsA1m`).

    Point (marker) styles (ps):
    
    - plain style with large solid markers (e.g. `psB1`),
    - plain style with large circular markers (e.g. `psB1c`), and
    - minor style with smaller, circular markers (e.g. `psB1m`).
    
    Linepoint styles (lps, markers connected by lines):
    
    - plain style with large solid markers (e.g. `lpsA2`),
    - plain style with large circular markers (e.g. `lpsA2c`),
    - minor style with smaller (circular) markers (e.g. `lpsA2m`).
    
    Fill styles (fs):
    
    - plain (e.g. `fsA3`) for a solid fill color and an edge color,
    - solid (e.g. `fsA3s`) for a solid fill color without edge color, and
    - alpha (e.g. `fsA3a`) for a transparent fill color.

    `palette`, a dictionary with colors of the specified color palette,
    is added to `namespace` as well.

    Parameters
    ----------
    namespace: class or None
        Namespace to which the generated line, point, linepoint and
        fill styles are added.  If None add styles to the global
        namespace of the `__main__` module.
    colors: string
        Name of the color palette from `plottools.colors` to be used.
    lwthick: float
        Line width for major line styles.
    lwthin: float
        Line width for minor line styles.
    markerlarge: float
        Marker size for major point styles.
    markersmall: float
        Marker size for minor point styles.
    mec: float
        Edge color for markers and fill styles. A factor between 0 and
        2 passed together with the facecolor to `lighter()`. I.e. 0
        results in a white edge, 1 in an edge of the color of the face
        color, and 2 in a black edge.
    mew: float
        Line width for marker edges and fill styles.
    fillalpha: float
        Alpha value for transparent fill styles.

    See Also
    --------
    make_linepointfill_styles(), plot_line_styles(), plot_point_styles(),
    plot_linepoint_styles(), plot_fill_styles()
    """
    if namespace is None:
        namespace = __main__
    namespace.palette = palettes[colors]
    palette = namespace.palette
    names = ['A1', 'A2', 'A3',
             'B1', 'B2', 'B3', 'B4', 'B5',
             'C1', 'C2', 'C3', 'C4']
    colors = [palette['red'], palette['orange'], palette['yellow'],
              palette['blue'], palette['purple'], palette['magenta'], palette['lightblue'], palette['pink'], 
              palette['lightgreen'], palette['green'], palette['darkgreen'], palette['cyan']]
    markers = [('o', 1.0), ('p', 1.1), ('h', 1.1),
               ((3, 1, 60), 1.25), ((3, 1, 0), 1.25), ((3, 1, 90), 1.25), ((3, 1, 30), 1.25), ((3, 1, 0), 1.25),
               ('s', 0.9), ('D', 0.85), ('*', 1.6), ((4, 1, 45), 1.4)]
    make_linepointfill_styles(namespace, names, colors, '-', markers,
                              lwthick=lwthick, lwthin=lwthin,
                              markerlarge=markerlarge,
                              markersmall=markersmall, mec=mec,
                              mew=mew, fillalpha=fillalpha)

    
def plot_line_styles(ax, namespace=None):
    """Plot names and lines of all available line styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the line styles.
    namespace: class or None
        Namespace on which styles are defined.
        If None take styles from the `__main__` module.

    See Also
    --------
    make_line_styles(), plot_point_styles(), plot_linepoint_styles(),
    plot_fill_styles()
    """
    if namespace is None:
        namespace = __main__
    k = 0
    for j, name in enumerate(namespace.style_names):
        gotit = False
        if name in namespace.ls:
            ax.text(k, 0.9, 'ls'+name)
            ax.plot([k, k+3.5], [1.0, 1.8], **namespace.ls[name])
            gotit = True
        if name in namespace.lsm:
            ax.text(k, -0.1, 'ls'+name+'m')
            ax.plot([k, k+3.5], [0.0, 0.8], **namespace.lsm[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(-0.2, k+2.8)
    ax.set_ylim(-0.15, 1.9)
    ax.set_title('line styles')
        

def plot_point_styles(ax, namespace=None):
    """Plot names and markers of all available point styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the point styles.
    namespace: class or None
        Namespace on which styles are defined.
        If None take styles from the `__main__` module.

    See Also
    --------
    make_point_styles(), plot_line_styles(), plot_linepoint_styles(),
    plot_fill_styles()
    """
    if namespace is None:
        namespace = __main__
    dy = 0.2
    k = 0
    for j, name in enumerate(reversed(namespace.style_names)):
        gotit = False
        if name in namespace.ps:
            ax.text(0.1, k, 'ps'+name)
            ax.plot([0.6], [k+dy], **namespace.ps[name])
            gotit = True
        if name in namespace.psc:
            ax.text(1.1, k, 'ps'+name+'c')
            ax.plot([1.6], [k+dy], **namespace.psc[name])
            gotit = True
        if name in namespace.psm:
            ax.text(2.1, k, 'ps'+name+'m')
            ax.plot([2.6], [k+dy], **namespace.psm[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(0.0, 3.0)
    ax.set_ylim(-1.0, k)
    ax.set_title('point styles')
        

def plot_linepoint_styles(ax, namespace=None):
    """Plot names, lines, and markers of all available linepoint styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the linepoint styles.
    namespace: class or None
        Namespace on which styles are defined.
        If None take styles from the `__main__` module.

    See Also
    --------
    make_linepoint_styles(), plot_line_styles(), plot_point_styles(),
    plot_fill_styles()
    """
    if namespace is None:
        namespace = __main__
    dy = 0.2
    k = 0
    for j, name in enumerate(reversed(namespace.style_names)):
        gotit = False
        if name in namespace.lps:
            ax.text(0.1, k-dy, 'lps'+name)
            ax.plot([0.8, 1.1, 1.4], [k, k, k], **namespace.lps[name])
            gotit = True
        if name in namespace.lpsc:
            ax.text(2.1, k-dy, 'lps'+name+'c')
            ax.plot([2.8, 3.1, 3.4], [k, k, k], **namespace.lpsc[name])
            gotit = True
        if name in namespace.lpsm:
            ax.text(4.1, k-dy, 'lps'+name+'m')
            ax.plot([4.8, 5.1, 5.4], [k, k, k], **namespace.lpsm[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(0.0, 6.0)
    ax.set_ylim(-1.0, k)
    ax.set_title('linepoint styles')
        

def plot_fill_styles(ax, namespace=None):
    """Plot names and patches of all available fill styles.

    Parameters
    ----------
    ax: matplotlib axes
        Subplot to use for plotting the fill styles.
    namespace: class or None
        Namespace on which styles are defined.
        If None take styles from the `__main__` module.

    See Also
    --------
    make_fill_styles(), plot_line_styles(), plot_point_styles(),
    plot_linepoint_styles()
    """
    if namespace is None:
        namespace = __main__
    x = np.linspace(0.0, 0.8, 50)
    y0 = np.zeros(len(x))
    y1 = -x*(x-0.6)*0.6/0.3/0.3
    y1[y1<0.0] = 0.0
    y2 = np.zeros(len(x))
    y2[x>0.3] = 0.7
    ax.text(0.0, 2.75, 'plain')
    ax.text(0.0, 1.75, 'solid')
    ax.text(0.0, 0.75, 'alpha')
    k = 0
    for j, name in enumerate(namespace.style_names):
        gotit = False
        if name in namespace.fs:
            ax.text(k, 1.9, 'fs'+name)
            ax.fill_between(x+k, y0+2, y2+2, **namespace.fs[name])
            ax.fill_between(x+k, y0+2, y1+2, **namespace.fs[name])
            gotit = True
        if name in namespace.fss:
            ax.text(k, 0.9, 'fs'+name+'s')
            ax.fill_between(x+k, y0+1, y2+1, **namespace.fss[name])
            ax.fill_between(x+k, y0+1, y1+1, **namespace.fss[name])
            gotit = True
        if name in namespace.fsa:
            ax.text(k, -0.1, 'fs'+name+'a')
            ax.fill_between(x+k, y0+0, y2+0, **namespace.fsa[name])
            ax.fill_between(x+k, y0+0, y1+0, **namespace.fsa[name])
            gotit = True
        if gotit:
            k += 1
    ax.set_xlim(-0.2, k)
    ax.set_ylim(-0.15, 2.9)
    ax.set_title('fill styles')
        

def demo(mode='line'):
    """ Run a demonstration of the styles module.

    Parameters
    ----------
    mode: string
        'line': plot the names and lines of all available line styles
        'point': plot the names and points (markers) of all available point styles
        'linepoint': plot the names and lines of all available linepoint styles
        'fill': plot the names and patches of all available fill styles
        'arrow': plot the names and arrows of all available arrow styles
    """
    generic_styles(None, colors='muted', lwthick=1.7, lwthin=0.8,
                   markerlarge=6.5, markersmall=4.0, mec=0.0, mew=0.8,
                   fillalpha=0.4)
    fig, ax = plt.subplots()
    if mode == 'lps' or 'linep' in mode:
        plot_linepoint_styles(ax)
    elif mode == 'ls' or 'line' in mode:
        plot_line_styles(ax)
    elif mode == 'ps' or 'point' in mode:
        plot_point_styles(ax)
    elif mode == 'fs' or 'fill' in mode:
        plot_fill_styles(ax)
    elif mode == 'ars' or mode == 'as' or 'arrow' in mode:
        from .arrows import generic_arrow_styles, plot_arrowstyles
        generic_arrow_styles(None, palettes['muted'], 3)
        plot_arrow_styles(ax)
    else:
        print('unknown option %s!' % mode)
        print('possible options are: line, ls, point, ps, linep(oint), lps, fill, fs, arrow, as, ars')
        return
    plt.show()


if __name__ == "__main__":
    mode = 'line'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    demo(mode)
