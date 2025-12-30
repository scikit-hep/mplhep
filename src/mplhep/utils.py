from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import ArrayLike
else:
    ArrayLike = Any

import logging
from collections import OrderedDict

import matplotlib as mpl
from matplotlib.transforms import Bbox
from mpl_toolkits.axes_grid1 import axes_size, make_axes_locatable

logger = logging.getLogger(__name__)

from ._utils import (
    _calculate_optimal_scaling,
    _draw_leg_bbox,
    _draw_text_bbox,
    _overlap,
)


def merge_legend_handles_labels(handles, labels):
    """
    Merge handles for identical labels.
    This is useful when combining multiple plot functions into a single label.

    handles : List of handles
    labels : List of labels
    """

    seen_labels = []
    seen_label_handles = []
    for handle, label in zip(handles, labels):
        if label not in seen_labels:
            seen_labels.append(label)
            seen_label_handles.append([handle])
        else:
            idx = seen_labels.index(label)
            seen_label_handles[idx].append(handle)

    for i in range(len(seen_labels)):
        seen_label_handles[i] = tuple(seen_label_handles[i])

    return seen_label_handles, seen_labels


def set_fitting_ylabel_fontsize(ax: plt.Axes) -> float:
    """
    Get the suitable font size for a ylabel text that fits within the plot's y-axis limits.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib subplot to adjust the ylabel font size for.

    Returns
    -------
    float
        The adjusted font size for the ylabel text.
    """
    ylabel_fontsize = float(ax.yaxis.get_label().get_fontsize())

    # Force renderer to be initialized
    ax.figure.canvas.draw()

    current_extent = (
        ax.yaxis.get_label()
        .get_window_extent(renderer=ax.figure.canvas.get_renderer())  # type: ignore[attr-defined]
        .transformed(ax.transData.inverted())
    )

    y_alignment = plt.rcParams["yaxis.labellocation"]

    while (
        y_alignment in ["center", "bottom"] and current_extent.y1 > ax.get_ylim()[1]
    ) or (y_alignment == "top" and current_extent.y0 < ax.get_ylim()[0]):
        ylabel_fontsize -= 0.1

        if ylabel_fontsize <= 0:
            msg = "Only a y-label with a negative font size would fit on the y-axis."
            raise ValueError(msg)

        ax.get_yaxis().get_label().set_size(ylabel_fontsize)  # type: ignore[attr-defined]

        current_extent = (
            ax.yaxis.get_label()
            .get_window_extent(renderer=ax.figure.canvas.get_renderer())  # type: ignore[attr-defined]
            .transformed(ax.transData.inverted())
        )

    return ylabel_fontsize


def yscale_legend(
    ax: mpl.axes.Axes | None = None,
    otol: float = 0,
    soft_fail: bool = False,
    N: int = 10,
) -> mpl.axes.Axes:
    """
    Automatically scale y-axis up to fit in legend().

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched or one is created)
    otol : float, optional
        Tolerance for overlap, default 0. Set ``otol > 0`` for less strict scaling.
    soft_fail : bool, optional
        Set ``soft_fail=True`` to return even if it could not fit the legend.
    N : int, optional
        Maximum number of scaling iterations, default 10.

    Returns
    -------
    ax : matplotlib.axes.Axes
    """
    if ax is None:
        ax = plt.gca()

    # Get legend bbox
    leg_bbox = _draw_leg_bbox(ax)
    if not leg_bbox:
        # No legend found, return axes unchanged
        return ax

    initial_overlap = _overlap(ax, leg_bbox)
    if initial_overlap <= otol:
        return ax

    iterations = 0
    final_overlap = initial_overlap
    while iterations < N:
        # Calculate optimal scaling
        scale_factor = _calculate_optimal_scaling(ax, leg_bbox)

        if scale_factor <= 1.0:
            break

        # Apply scaling
        y_min, y_max = ax.get_ylim()
        new_y_max = y_max * scale_factor
        ax.set_ylim(y_min, new_y_max)

        # Redraw to update legend position
        if (fig := ax.figure) is None:
            msg = "Could not fetch figure, maybe no plot is drawn yet?"
            raise RuntimeError(msg)
        fig.canvas.draw()

        # Check if scaling resolved overlap
        final_overlap = _overlap(ax, _draw_leg_bbox(ax))
        if final_overlap <= otol:
            return ax

        iterations += 1

    if final_overlap > otol and not soft_fail:
        msg = f"Could not fit legend after {N} scaling iterations (overlap: {final_overlap}). Try increasing otol, N, or using soft_fail=True."
        raise RuntimeError(msg)
    if final_overlap > otol:
        logger.warning(
            f"Legend still overlaps after {N} scaling iterations (overlap: {final_overlap})"
        )

    return ax


def yscale_anchored_text(
    ax: mpl.axes.Axes | None = None,
    otol: float = 0,
    soft_fail: bool = False,
    N: int = 3,
) -> mpl.axes.Axes:
    """
    Automatically scale y-axis up to fit AnchoredText

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched or one is created)
    otol : float, optional
        Tolerance for overlap, default 0. Set ``otol > 0`` for less strict scaling.
    soft_fail : bool, optional
        Set ``soft_fail=True`` to return even if it could not fit the legend.
    N : int, optional
        Maximum number of scaling iterations, default 10.

    Returns
    -------
    ax : matplotlib.axes.Axes
    """
    if ax is None:
        ax = plt.gca()

    # Get text bbox and text objects
    text_bbox, text_objects = _draw_text_bbox(ax)
    logger.debug(f"yscale_anchored_text: Received {len(text_bbox)} text bboxes")
    if not text_bbox:
        return ax

    initial_overlap = _overlap(ax, text_bbox, exclude_texts=text_objects)
    if initial_overlap <= otol:
        return ax

    iterations = 0
    final_overlap = initial_overlap
    while iterations < N:
        # Calculate optimal scaling (excluding the text objects we're positioning)
        scale_factor = _calculate_optimal_scaling(
            ax, text_bbox, exclude_texts=text_objects
        )
        if scale_factor <= 1.0:
            break

        # Apply scaling
        y_min, y_max = ax.get_ylim()
        new_y_max = y_max * scale_factor
        ax.set_ylim(y_min, new_y_max)

        # Redraw to update text position
        if (fig := ax.figure) is None:
            msg = "Could not fetch figure, maybe no plot is drawn yet?"
            raise RuntimeError(msg)
        fig.canvas.draw()

        # Check if scaling resolved overlap (excluding the annotation texts themselves)
        updated_text_bbox, updated_text_objects = _draw_text_bbox(ax)
        final_overlap = _overlap(
            ax, updated_text_bbox, exclude_texts=updated_text_objects
        )
        if final_overlap <= otol:
            return ax

        iterations += 1

    if final_overlap > otol and not soft_fail:
        msg = f"Could not fit AnchoredText after {N} scaling iterations (overlap: {final_overlap}). Try increasing otol, N, or using soft_fail=True."
        raise RuntimeError(msg)
    if final_overlap > otol:
        logger.warning(
            f"AnchoredText still overlaps after {N} scaling iterations (overlap: {final_overlap})"
        )

    return ax


def set_ylow(
    ax: mpl.axes.Axes | None = None, ylow: float | None = None
) -> mpl.axes.Axes:
    """
    Set lower y limit to 0 or a specific value if not data/errors go lower.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched or one is created)
    ylow : float, optional
        Set lower y limit to a specific value.

    Returns
    -------
    ax : matplotlib.axes.Axes
    """
    if ax is None:
        ax = plt.gca()

    if ax.get_yaxis().get_scale() == "log":
        return ax

    if ylow is None:
        if (fig := ax.figure) is None:
            msg = "No figure found"
            raise ValueError(msg)
        fig.canvas.draw()
        current_ylim = ax.get_ylim()
        if current_ylim[0] >= 0:
            ax.set_ylim(0, current_ylim[1])

    else:
        ax.set_ylim(0, ax.get_ylim()[-1])

    return ax


def mpl_magic(
    ax=None,
    ylow: float | None = None,
    otol=1,
    soft_fail=False,
    N=2,
):
    """
    Consolidate all ex-post style adjustments:
        ylow
        yscale_legend
        yscale_anchored_text

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched or one is created)
    ylow : float, optional
        Set lower y limit to a specific value for ylow function
    otol : float, optional
        Tolerance for overlap for yscale_legend, default 0
    soft_fail : bool, optional
        Set to True to return even if legend could not fit in 10 iterations
    N : int, optional
        Maximum number of scaling iterations for yscale functions, default 10
    Returns
    -------
    ax : matplotlib.axes.Axes
    """
    if ax is None:
        ax = plt.gca()

    ax = set_ylow(ax, ylow=ylow)
    ax = yscale_legend(ax, otol=otol, soft_fail=soft_fail, N=N)
    return yscale_anchored_text(ax, otol=otol, soft_fail=soft_fail, N=N)


########################################
# Figure/axes helpers
def rescale_to_axessize(ax, w, h):
    """
    Adjust figure size to axes size in inches
    Parameters: w, h: width, height in inches
    """
    if not ax:
        ax = plt.gca()
    left = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w) / (r - left)
    figh = float(h) / (t - b)
    ax.figure.set_size_inches(figw, figh)


def box_aspect(ax, aspect=1):
    """
    Adjust figure size to axes size in inches
    Parameters: aspect: float, optional aspect ratio

    """
    position = ax.get_position()

    fig_width, fig_height = ax.get_figure().get_size_inches()
    fig_aspect = fig_height / fig_width

    pb = position.frozen()
    pb1 = pb.shrunk_to_aspect(aspect, pb, fig_aspect)
    ax.set_position(pb1)


class RemainderFixed(axes_size.Scaled):
    def __init__(self, xsizes, ysizes, divider):
        self.xsizes = xsizes
        self.ysizes = ysizes
        self.div = divider

    def get_size(self, renderer):
        _xrel, xabs = sum(self.xsizes, start=axes_size.Fixed(0)).get_size(renderer)
        _yrel, yabs = sum(self.ysizes, start=axes_size.Fixed(0)).get_size(renderer)
        bb = Bbox.from_bounds(*self.div.get_position()).transformed(
            self.div._fig.transFigure
        )
        w = bb.width / self.div._fig.dpi - xabs
        h = bb.height / self.div._fig.dpi - yabs
        return 0, min([w, h])


def make_square_add_cbar(ax, size=0.4, pad=0.1):
    """
    Make input axes square and return an appended axes to the right for
    a colorbar. Both axes resize together to fit figure automatically.
    Works with tight_layout().
    """
    divider = make_axes_locatable(ax)

    margin_size = axes_size.Fixed(size)
    pad_size = axes_size.Fixed(pad)
    xsizes = [pad_size, margin_size]
    ysizes = xsizes

    cax = divider.append_axes("right", size=margin_size, pad=pad_size)

    divider.set_horizontal([RemainderFixed(xsizes, ysizes, divider), *xsizes])
    divider.set_vertical([RemainderFixed(xsizes, ysizes, divider), *ysizes])
    return cax


def append_axes(ax, size=0.1, pad=0.1, position="right", extend=False):
    """
    Append a side ax to the current figure and return it.
    Figure is automatically extended along the direction of the added axes to
    accommodate it. Unfortunately can not be reliably chained.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to append to
    size : float or str, optional
        Size of the appended axes. If str ending with '%', interpreted as percentage of parent axes size.
    pad : float or str, optional
        Padding between axes. If str ending with '%', interpreted as percentage of parent axes size.
    position : str, optional
        Position of appended axes ('right', 'left', 'top', 'bottom')
    extend : bool, optional
        Whether to extend the figure size to accommodate the new axes

    Returns
    -------
    matplotlib.axes.Axes
        The appended axes object
    """
    fig = ax.figure
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height

    def convert(fraction, position=position):
        if isinstance(fraction, str) and fraction.endswith("%"):
            if position in ["right", "left"]:
                fraction = width * float(fraction.strip("%")) / 100
            elif position in ["top", "bottom"]:
                fraction = height * float(fraction.strip("%")) / 100
        return fraction

    size = convert(size)
    pad = convert(pad)

    divider = make_axes_locatable(ax)
    margin_size = axes_size.Fixed(size)
    pad_size = axes_size.Fixed(pad)
    xsizes = [pad_size, margin_size]
    if position in ["top", "bottom"]:
        xsizes.reverse()
    yhax = divider.append_axes(position, size=margin_size, pad=pad_size)

    if extend:

        def extend_ratio(ax, yhax):
            ax.figure.canvas.draw()
            orig_size = ax.get_position().size
            new_size = sum(itax.get_position().size for itax in [ax, yhax])
            return new_size / orig_size

        if position in ["right"]:
            divider.set_horizontal([axes_size.Fixed(width), *xsizes])
            fig.set_size_inches(
                fig.get_size_inches()[0] * extend_ratio(ax, yhax)[0],
                fig.get_size_inches()[1],
            )
        elif position in ["left"]:
            divider.set_horizontal([*xsizes[::-1], axes_size.Fixed(width)])
            fig.set_size_inches(
                fig.get_size_inches()[0] * extend_ratio(ax, yhax)[0],
                fig.get_size_inches()[1],
            )
        elif position in ["top"]:
            divider.set_vertical([axes_size.Fixed(height), *xsizes[::-1]])
            fig.set_size_inches(
                fig.get_size_inches()[0],
                fig.get_size_inches()[1] * extend_ratio(ax, yhax)[1],
            )
            yhax.sharex(ax)
        elif position in ["bottom"]:
            divider.set_vertical([*xsizes, axes_size.Fixed(height)])
            fig.set_size_inches(
                fig.get_size_inches()[0],
                fig.get_size_inches()[1] * extend_ratio(ax, yhax)[1],
            )
            yhax.sharex(ax)

    return yhax


def sort_legend(ax, order=None):
    """
    ax : axes with legend labels in it
    order : Ordered dict with renames or array with order
    """

    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))

    if isinstance(order, OrderedDict):
        ordered_label_list = list(order.keys())
    elif isinstance(order, (list, tuple, np.ndarray)):
        ordered_label_list = list(order)
    elif order is None:
        ordered_label_list = labels
    else:
        msg = f"Unexpected values type of order: {type(order)}"
        raise TypeError(msg)

    ordered_label_list = [entry for entry in ordered_label_list if entry in labels]
    ordered_label_values = [by_label[k] for k in ordered_label_list]
    if isinstance(order, OrderedDict):
        ordered_label_list = [order[k] for k in ordered_label_list]
    return ordered_label_values, ordered_label_list


def _get_model_type(components):
    """
    Check that all components of a model are either all histograms or all functions
    and return the type of the model components.

    Parameters
    ----------
    components : list
        The list of model components.

    Returns
    -------
    str
        The type of the model components ("histograms" or "functions").

    Raises
    ------
    ValueError
        If the model components are not all histograms or all functions.
    """
    if all(callable(x) for x in components):
        return "functions"
    return "histograms"


def subplots(
    figsize: tuple[float, float] | None = None,
    nrows: int = 1,
    gridspec_kw: dict | None = None,
    hspace: float = 0.15,
    *args,
    **kwargs,
) -> tuple[plt.Figure, np.ndarray]:
    """
    Wrapper around plt.subplots to create a figure with multiple subplots. Conveniently
    adjusts the figure size and spacing between subplots if multiple rows are requested.

    Parameters
    ----------
    figsize : tuple[float, float], optional
        Figure size in inches. Default will adjust height based on number of rows.
    nrows : int, optional
        Number of rows in the subplot grid. Default is 1.
    gridspec_kw : dict | None, optional
        Additional keyword arguments for the GridSpec. Default is None.
        If None is provided and nrows > 1, height_ratios will be set to
        give more space to the top subplot.
    hspace : float, optional
        Height spacing between subplots. Default is 0.15.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    axes : np.ndarray
        Array of Axes objects representing the subplots.
    """
    if gridspec_kw is None and nrows > 1:
        gridspec_kw = {
            "height_ratios": [
                4 - (0.2 * (nrows - 2)),
                *(1 for _ in range(nrows - 1)),
            ]
        }

    if figsize is None:
        figsize = (
            plt.rcParams["figure.figsize"][0],
            plt.rcParams["figure.figsize"][1] * (1.25 ** (nrows - 1)),
        )

    kwargs.setdefault("figsize", figsize)
    kwargs.setdefault("gridspec_kw", gridspec_kw)
    kwargs.setdefault("nrows", nrows)

    fig, axes = plt.subplots(
        *args,
        **kwargs,
    )
    if nrows > 1:
        fig.subplots_adjust(hspace=hspace)

        for ax in axes[:-1]:
            _ = ax.xaxis.set_ticklabels([])
            ax.set_xlabel(" ")

    return fig, axes
