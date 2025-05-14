from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib import rcParams

from . import label as label_base


def _get_transform(transform=None, ax=None):
    """Get proper transform for placement of DUNE labels."""
    if transform is not None:
        return transform
    if ax is not None and hasattr(ax, "transAxes"):
        return ax.transAxes
    return plt.gca().transAxes


def _dune_watermark():
    """
    Produces the "DUNE" part of the string used in watermarks so it can be styled independently.
    
    Returns
    -------
    str
        The appropriately styled "DUNE" string
    """
    return r"$\mathdefault{\bf{DUNE}}$"


def _text_label(text, x, y, transform=None, ax=None, **kwargs):
    """
    Add a text label at an arbitrary place on the plot.
    Internal utility function for more specific label functions.
    
    Parameters
    ----------
    text : str
        Text to write
    x : float
        Intended x-coordinate
    y : float
        Intended y-coordinate
    transform : matplotlib.transforms.Transform, optional
        If you want to use a transformation other than the default transAxes
    ax : matplotlib.axes.Axes, optional
        If you prefer to pass an Axes directly
    **kwargs
        Any other arguments will be passed to pyplot.text()
        
    Returns
    -------
    None
    """
    plotter = plt if ax is None else ax
    kwargs.setdefault("fontdict", {})
    kwargs["fontdict"]["fontsize"] = 18
    if "color" in kwargs:
        kwargs["fontdict"]["color"] = kwargs.pop("color")
    if "fontsize" in kwargs:
        kwargs["fontdict"]["fontsize"] = kwargs.pop("fontsize")
    if "align" in kwargs:
        kwargs["horizontalalignment"] = kwargs.pop("align")
    
    plotter.text(x, y, text,
                 transform=_get_transform(transform, plotter),
                 **kwargs)


def text(label="", loc=0, ax=None, **kwargs):
    """Text label with DUNE style.
    
    Parameters
    ----------
    label : str, optional
        Text to add after DUNE label, by default ""
    loc : int, optional
        Label position:
        - 0 : Above axes, left aligned (default)
        - 1 : Top left corner
        - 2 : Top left corner, multiline
        - 3 : Split DUNE above axes, rest of label in top left corner
    ax : matplotlib.axes.Axes, optional
        Axes to add label to, by default None
    **kwargs
        Additional keyword arguments passed to _text_label
        
    Returns
    -------
    matplotlib.axes.Axes
        The axes with the label added
    """
    if ax is None:
        ax = plt.gca()
    
    # Add the main DUNE label
    _text_label(_dune_watermark() + (" " + label if label else ""), 
               x=0.05 if loc in [1, 2, 3] else 0.001,
               y=0.95 if loc in [1, 2, 3] else 1.005,
               ax=ax, 
               transform=None,
               align='left', 
               color="black",
               **kwargs)
    
    return ax


def label(exp="DUNE", loc=0, *, data=False, label="", year=None, 
          lumi=None, rlabel=None, energy=13, ax=None, **kwargs):
    """Add DUNE label to a plot.
    
    Parameters
    ----------
    exp : str, optional
        Experiment name, by default "DUNE"
    loc : int, optional
        Label position:
        - 0 : Above axes, left aligned (default)
        - 1 : Top left corner
        - 2 : Top left corner, multiline
        - 3 : Split DUNE above axes, rest of label in top left corner
    data : bool, optional
        Whether this is real data (True) or simulation (False), by default False
    label : str, optional
        Additional label text, e.g., "Preliminary", "Work in Progress", etc.
    year : int, optional
        Data-taking year, by default None
    lumi : float, optional
        Integrated luminosity, by default None
    rlabel : str, optional
        Override right label, by default None
    energy : int, optional
        Center-of-mass energy in TeV, by default 13
    ax : matplotlib.axes.Axes, optional
        Axes to place label on, by default None
    **kwargs
        Additional arguments passed to label_base.exp_text
        
    Returns
    -------
    tuple
        (exptext, expsuffix) text objects 
    """
    
    # Forward to the main label utility with DUNE-specific defaults
    return label_base.exp_label(
        exp=exp,
        loc=loc,
        data=data, 
        label=label,
        year=year,
        lumi=lumi,
        rlabel=rlabel,
        ax=ax,
        **kwargs
    )


def preliminary(x=0.05, y=0.90, align='left', transform=None, ax=None, **kwargs):
    """Apply a "DUNE Preliminary" label.
    
    Parameters
    ----------
    x : float, optional
        x-location for the label, by default 0.05
    y : float, optional
        y-location for the label, by default 0.90
    align : str, optional
        Text alignment for the label, by default 'left'
    transform : matplotlib.transforms.Transform, optional
        Transform to use, by default None
    ax : matplotlib.axes.Axes, optional
        Axes to add label to, by default None
    **kwargs
        Additional keyword arguments passed to _text_label
        
    Returns
    -------
    None
    """
    _text_label(_dune_watermark() + " Preliminary", x, y, ax=ax, transform=transform, 
               align=align, color="black", **kwargs)


def wip(x=0.05, y=0.90, align='left', transform=None, ax=None, **kwargs):
    """Apply a "DUNE Work In Progress" label.
    
    Parameters
    ----------
    x : float, optional
        x-location for the label, by default 0.05
    y : float, optional
        y-location for the label, by default 0.90
    align : str, optional
        Text alignment for the label, by default 'left'
    transform : matplotlib.transforms.Transform, optional
        Transform to use, by default None
    ax : matplotlib.axes.Axes, optional
        Axes to add label to, by default None
    **kwargs
        Additional keyword arguments passed to _text_label
        
    Returns
    -------
    None
    """
    _text_label(_dune_watermark() + " Work In Progress", x, y, ax=ax, 
               transform=transform, align=align, color="black", **kwargs)


def simulation(x=0.05, y=0.90, align='left', ax=None, transform=None, **kwargs):
    """Apply a "DUNE Simulation" label.
    
    Parameters
    ----------
    x : float, optional
        x-location for the label, by default 0.05
    y : float, optional
        y-location for the label, by default 0.90
    align : str, optional
        Text alignment for the label, by default 'left'
    transform : matplotlib.transforms.Transform, optional
        Transform to use, by default None
    ax : matplotlib.axes.Axes, optional
        Axes to add label to, by default None
    **kwargs
        Additional keyword arguments passed to _text_label
        
    Returns
    -------
    None
    """
    _text_label(_dune_watermark() + " Simulation", x, y, ax=ax, 
               transform=transform, align=align, color="black", **kwargs)


def simulation_side(x=1.05, y=0.5, align='right', ax=None, transform=None, **kwargs):
    """Apply a "DUNE Simulation" label on the right outside of the frame.
    
    Parameters
    ----------
    x : float, optional
        x-location for the label, by default 1.05
    y : float, optional
        y-location for the label, by default 0.5
    align : str, optional
        Text alignment for the label, by default 'right'
    transform : matplotlib.transforms.Transform, optional
        Transform to use, by default None
    ax : matplotlib.axes.Axes, optional
        Axes to add label to, by default None
    **kwargs
        Additional keyword arguments passed to _text_label
        
    Returns
    -------
    None
    """
    _text_label(_dune_watermark() + " Simulation", x, y, ax=ax, 
               transform=transform, align=align, rotation=270, color="black", **kwargs)


def official(x=0.05, y=0.90, align='left', ax=None, transform=None, **kwargs):
    """Apply a "DUNE" label (for officially approved results only).
    
    Parameters
    ----------
    x : float, optional
        x-location for the label, by default 0.05
    y : float, optional
        y-location for the label, by default 0.90
    align : str, optional
        Text alignment for the label, by default 'left'
    transform : matplotlib.transforms.Transform, optional
        Transform to use, by default None
    ax : matplotlib.axes.Axes, optional
        Axes to add label to, by default None
    **kwargs
        Additional keyword arguments passed to _text_label
        
    Returns
    -------
    None
    """
    _text_label(_dune_watermark(), x, y, ax=ax, 
               transform=transform, align=align, color="black", **kwargs)


def corner_label(label, ax=None, transform=None, **kwargs):
    """Apply a gray label with user-specified text on the upper-left corner (outside the plot frame).
    
    Parameters
    ----------
    label : str
        Text to display
    ax : matplotlib.axes.Axes, optional
        Axes to add label to, by default None
    transform : matplotlib.transforms.Transform, optional
        Transform to use, by default None
    **kwargs
        Additional keyword arguments passed to _text_label
        
    Returns
    -------
    None
    """
    _text_label(label, 0, 1.05, ax=ax, transform=transform, color="gray", **kwargs)


def set_dune_logo_colors():
    """Set the color cycler to use the subset of Okabe-Ito colors that overlap with the DUNE logo colors."""
    from cycler import cycler
    cyc = cycler(color=['#D55E00', '#56B4E9', '#E69F00'])
    plt.rc("axes", prop_cycle=cyc)


def set_okabe_ito_colors():
    """Set the color cycler to use Okabe-Ito colors."""
    from cycler import cycler
    cyc = cycler(color=['#000000', '#D55E00', '#56B4E9', '#E69F00', '#009E73', '#CC79A7', '#0072B2', '#F0E442'])
    plt.rc("axes", prop_cycle=cyc)