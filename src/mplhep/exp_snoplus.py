from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

import matplotlib as mpl
from matplotlib import rcParams

import mplhep

from . import label as label_base
from ._compat import copy_doc
from .styles import snoplus as style

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.legend import Legend


__all__ = ("style", "text", "legend")


@copy_doc(label_base.add_text)
def text(text="", **kwargs):
    """Add SNO+ experiment text to a plot."""
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("fontsize", 16)
    kwargs.setdefault("fontname", "serif")
    return label_base.add_text(text=text, **kwargs)


def legend(ax: Axes | None = None, **kwargs) -> Legend:
    """Add a SNO+ Styled legend to a plot.

    Parameters
    ----------
        ax : Axes | None, optional:
            The axes object of the plot to add the legend to.
            If no axes is provided, the legend is added to the current global axis.

    Returns
    -------
        Legend:
            The Legend object that was added to the axis.
    """
    ax = ax or mpl.pyplot.gca()

    handles, labels = ax.get_legend_handles_labels()
    new_handles: list[mpl.artist.Artist] = []

    for handle in handles:
        color: Any = None
        if isinstance(handle, mpl.patches.Polygon):
            color = handle.get_edgecolor()
        elif isinstance(handle, mpl.collections.PolyCollection):
            color = handle.get_facecolor()
            if len(color) > 0:
                color = color[0]

        if color is not None:
            new_handle = mpl.lines.Line2D(
                [0], [0], color=color, lw=rcParams["lines.linewidth"]
            )
            new_handles.append(new_handle)
        else:
            new_handles.append(handle)

    return ax.legend(new_handles, labels, **kwargs)
