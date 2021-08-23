from __future__ import annotations

import collections.abc
import warnings
from collections import OrderedDict, namedtuple
from typing import TYPE_CHECKING, Any, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnchoredText
from matplotlib.transforms import Bbox
from mpl_toolkits.axes_grid1 import axes_size, make_axes_locatable

from .utils import (
    get_histogram_axes_title,
    get_plottable_protocol_bins,
    hist_object_handler,
    isLight,
    process_histogram_parts,
)

if TYPE_CHECKING:
    from numpy.typing import ArrayLike

StairsArtists = namedtuple("StairsArtists", "stairs errorbar legend_artist")
ErrorBarArtists = namedtuple("ErrorBarArtists", "errorbar")
ColormeshArtists = namedtuple("ColormeshArtists", "pcolormesh cbar text")


Hist1DArtists = Union[StairsArtists, ErrorBarArtists]
Hist2DArtists = ColormeshArtists


def get_density(h, density: bool = True, binwnorm: float | None = None, *, bins, hists):
    if density and binwnorm is not None:
        raise ValueError("Can only calculate density or binwnorm")
    per_hist_norm = np.sum(h, axis=(1 if h.ndim > 1 else 0))
    if binwnorm is not None:
        overallnorm = binwnorm * per_hist_norm
    else:
        overallnorm = np.ones(len(hists))
    binnorms = np.outer(overallnorm, np.ones_like(bins[:-1]))
    binnorms /= np.outer(np.diff(bins), per_hist_norm).T
    if binnorms.ndim == 2 and len(binnorms) == 1:  # Unwrap if [[1,2,3]]
        binnorms = binnorms[0]
    return binnorms


def get_stack(_h, hists):
    if len(hists) > 1:
        return np.cumsum(_h, axis=0)
    else:
        return _h


def soft_update_kwargs(kwargs, mods, rc=True):
    not_default = [k for k, v in mpl.rcParamsDefault.items() if v != mpl.rcParams[k]]
    respect = [
        "hatch.linewidth",
        "lines.linewidth",
        "patch.linewidth",
        "lines.linestyle",
    ]
    aliases = {"ls": "linestyle", "lw": "linewidth"}
    kwargs = {aliases[k] if k in aliases else k: v for k, v in kwargs.items()}
    for key, val in mods.items():
        rc_modded = (key in not_default) or (
            key in [k.split(".")[-1] for k in not_default if k in respect]
        )
        if key not in kwargs and (rc and not rc_modded):
            kwargs[key] = val
    return kwargs


########################################
# Histogram plotter
def histplot(
    H,  # Histogram object, tuple or array
    bins=None,  # Bins to be supplied when h is a value array or iterable of arrays
    *,
    yerr: ArrayLike | bool | None = None,
    w2=None,
    w2method=None,
    stack=False,
    density=False,
    binwnorm=None,
    histtype="step",
    xerr=False,
    label=None,
    edges=True,
    binticks=False,
    ax=None,
    **kwargs,
):
    """
    Create a 1D histogram plot from `np.histogram`-like inputs. Parameters
    ----------
        H : object
            Histogram object with containing values and optionally bins. Can be:

            - `np.histogram` tuple
            - PlottableProtocol histogram object
            - `boost_histogram` classic (<0.13) histogram object
            - raw histogram values, provided `bins` is specified.

        bins : iterable, optional
            Histogram bins, if not part of ``h``.
        yerr : iterable or bool, optional
            Histogram uncertainties. Following modes are supported:
            - True, sqrt(N) errors or poissonian interval when ``w2`` is specified
            - shape(N) array of for one sided errors or list thereof
            - shape(Nx2) array of for two sided errors or list thereof
        w2 : iterable, optional
            Sum of the histogram weights squared for poissonian interval error
            calculation
        w2method: callable, optional
            Function calculating CLs with signature ``low, high = fcn(w, w2)``. Here
            ``low`` and ``high`` are given in absolute terms, not relative to w.
            Default is ``None``. If w2 has integer values (likely to be data) poisson
            interval is calculated, otherwise the resulting error is symmetric
            ``sqrt(w2)``.
        stack : bool, optional
            Whether to stack or overlay non-axis dimension (if it exists). N.B. in
            contrast to ROOT, stacking is performed in a single call aka
            ``histplot([h1, h2, ...], stack=True)`` as opposed to multiple calls.
        density : bool, optional
            If true, convert sum weights to probability density (i.e. integrates to 1
            over domain of axis) (Note: this option conflicts with ``binwnorm``)
        binwnorm : float, optional
            If true, convert sum weights to bin-width-normalized, with unit equal to
                supplied value (usually you want to specify 1.)
        histtype: {'step', 'fill', 'errorbar'}, optional, default: "step"
            Type of histogram to plot:

            - "step": skyline/step/outline of a histogram using `plt.step <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.step.html#matplotlib.axes.Axes.step>`_
            - "fill": filled histogram using `plt.fill_between <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.step.html#matplotlib.axes.Axes.step>`_
            - "errorbar": single marker histogram using `plt.errorbar <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.step.html#matplotlib.axes.Axes.step>`_
        xerr:  bool or float, optional
            Size of xerr if ``histtype == 'errorbar'``. If ``True``, bin-width will be used.
        label : str or list, optional
            Label for legend entry.
        edges : bool, default: True, optional
            Specifies whether to draw first and last edges of the histogram
        binticks : bool, default: False, optional
            Attempts to draw x-axis ticks coinciding with bin boundaries if feasible.
        ax : matplotlib.axes.Axes, optional
            Axes object (if None, last one is fetched or one is created)
        **kwargs :
            Keyword arguments passed to underlying matplotlib functions -
            {'step', 'fill_between', 'errorbar'}.
    Returns
    -------
        List[Hist1DArtists]

    """
    # ax check
    if ax is None:
        ax = plt.gca()
    else:
        if not isinstance(ax, plt.Axes):
            raise ValueError("ax must be a matplotlib Axes object")

    # arg check
    _allowed_histtype = ["fill", "step", "errorbar"]
    _err_message = f"Select 'histtype' from: {_allowed_histtype}"
    assert histtype in _allowed_histtype, _err_message

    hists = list(process_histogram_parts(H, bins))
    final_bins, xtick_labels = get_plottable_protocol_bins(hists[0].axes[0])
    _x_axes_label = ax.get_xlabel()
    x_axes_label = (
        _x_axes_label
        if _x_axes_label != ""
        else get_histogram_axes_title(hists[0].axes[0])
    )

    # TODO: use hists everywhere
    h = np.stack([h.values().astype(float) for h in hists])
    if yerr is None and all(h.variances() is not None for h in hists):
        yerr = np.stack([np.sqrt(h.variances()) for h in hists])
    elif yerr is False:
        yerr = None

    # Convert 1/0 etc to real bools
    stack = bool(stack)
    density = bool(density)
    edges = bool(edges)
    binticks = bool(binticks)

    assert final_bins.ndim == 1, "bins need to be 1 dimensional"
    # TODO: can check validity of bin length elsewhere

    if w2 is not None and yerr is not None:
        raise ValueError("Can only supply errors or w2")

    _labels: list[str | None]
    if label is None:
        _labels = [None] * len(hists)
    elif isinstance(label, str):
        _labels = [label] * len(hists)
    elif not np.iterable(label):
        _labels = [str(label)] * len(hists)
    else:
        _labels = [str(lab) for lab in label]

    def iterable_not_string(arg):
        return isinstance(arg, collections.abc.Iterable) and not isinstance(arg, str)

    _chunked_kwargs: list[dict[str, Any]] = []
    for _i in range(len(hists)):
        _chunked_kwargs.append({})
    for kwarg in kwargs:
        # Check if iterable
        if iterable_not_string(kwargs[kwarg]):
            # Check if tuple (can be used for colors)
            if type(kwargs[kwarg]) == tuple:
                for i in range(len(_chunked_kwargs)):
                    _chunked_kwargs[i][kwarg] = kwargs[kwarg]
            else:
                for i, kw in enumerate(kwargs[kwarg]):
                    _chunked_kwargs[i][kwarg] = kw
        else:
            for i in range(len(_chunked_kwargs)):
                _chunked_kwargs[i][kwarg] = kwargs[kwarg]

    _bin_widths = np.diff(final_bins)
    _bin_centers = final_bins[1:] - _bin_widths / float(2)

    ############################
    # yerr calculation
    _yerr: np.ndarray | None
    if yerr is not None:
        # yerr is array
        if hasattr(yerr, "__len__"):
            _yerr = np.asarray(yerr)
        # yerr is a number
        elif isinstance(yerr, (int, float)) and not isinstance(yerr, bool):
            _yerr = np.ones_like(h) * yerr
        # yerr is automatic
        else:
            if yerr is True:
                if stack:
                    raise RuntimeError(
                        "Automatic errorbars not defined for " "stacked plot"
                    )
                _yerr = np.sqrt(h)
            else:
                raise RuntimeError("Empty code path")

    elif w2 is not None:
        if w2method is None:
            int_w2 = np.around(w2).astype(int)
            if np.all(np.isclose(w2, int_w2, 0.000001)):
                # If w2 are integers (true data hist), calculate Garwood interval
                try:
                    from .error_estimation import poisson_interval

                    _yerr = np.abs(poisson_interval(h[0], w2) - h[0])
                except ImportError:
                    warnings.warn(
                        "Integer weights indicate poissonian data. Will calculate "
                        "Garwood interval if ``scipy`` is installed. Otherwise errors "
                        "will be set to ``sqrt(w2)``."
                    )
                    _yerr = np.sqrt(w2)
            else:
                # w2 to errors directly if specified previously
                _yerr = np.sqrt(w2)
        else:
            _yerr = np.abs(w2method(h, w2) - h)

    else:
        _yerr = None

    if _yerr is not None:
        assert isinstance(_yerr, np.ndarray)
        if _yerr.ndim == 3:
            # Already correct format
            pass
        elif _yerr.ndim == 2 and len(hists) == 1:
            # Broadcast ndim 2 to ndim 3
            if _yerr.shape[-2] == 2:  # [[1,1], [1,1]]
                _yerr = _yerr.reshape(len(hists), 2, _yerr.shape[-1])
            elif _yerr.shape[-2] == 1:  # [[1,1]]
                _yerr = np.tile(_yerr, 2).reshape(len(hists), 2, _yerr.shape[-1])
            else:
                raise ValueError("yerr format is not understood")
        elif _yerr.ndim == 2:
            # Broadcast yerr (nh, N) to (nh, 2, N)
            _yerr = np.tile(_yerr, 2).reshape(len(hists), 2, _yerr.shape[-1])
        elif _yerr.ndim == 1:
            # Broadcast yerr (1, N) to (nh, 2, N)
            _yerr = np.tile(_yerr, 2 * len(hists)).reshape(
                len(hists), 2, _yerr.shape[-1]
            )
        else:
            raise ValueError("yerr format is not understood")

        assert _yerr is not None
        # Split
        _yerr_lo = _yerr[:, 0]
        _yerr_hi = _yerr[:, 1]

    ############################
    # Stacking, norming, density
    if density or binwnorm is not None:
        density_arr = get_density(h, density, binwnorm, bins=final_bins, hists=hists)
        if stack:
            h = get_stack(h, hists)
            h *= get_density(h, density, binwnorm, bins=final_bins, hists=hists)[-1]
        else:
            h *= density_arr
        if _yerr is not None:
            for i in range(len(hists)):
                _yerr_lo[i] = _yerr_lo[i] * density_arr[i]
                _yerr_hi[i] = _yerr_hi[i] * density_arr[i]

    if stack and not density and binwnorm is None:
        h = get_stack(h, hists)

    # Stack
    if stack and len(hists) > 1:
        h = h[::-1]
        if yerr is not None:
            _yerr_lo = _yerr_lo[::-1]
            _yerr_hi = _yerr_hi[::-1]
        _labels = _labels[::-1]
        _chunked_kwargs = _chunked_kwargs[::-1]

    #################################
    # Split and reshape for iteration
    h = h.reshape(len(hists), -1)

    ##########
    # Plotting
    return_artists: list[StairsArtists | ErrorBarArtists] = []
    if histtype == "step":
        for i in range(len(hists)):
            _kwargs = _chunked_kwargs[i]
            _label = _labels[i]
            _step_label = _label if (yerr is None and w2 is None) else None
            _kwargs = soft_update_kwargs(_kwargs, {"linewidth": 1.5})

            _s = ax.stairs(
                h[i],
                final_bins,
                baseline=None if not edges else 0,
                label=_step_label,
                **_kwargs,
            )

            if yerr is not None or w2 is not None:
                _kwargs = soft_update_kwargs(
                    _kwargs, {"color": _s.get_edgecolor(), "linestyle": "none"}
                )
                _e = ax.errorbar(
                    _bin_centers,
                    h[i],
                    yerr=[_yerr_lo[i], _yerr_hi[i]],
                    **_kwargs,
                )
                _e_leg = ax.errorbar(
                    [], [], yerr=1, xerr=1, color=_s.get_edgecolor(), label=_label
                )
            return_artists.append(
                StairsArtists(
                    _s,
                    _e if yerr is not None or w2 is not None else None,
                    _e_leg if yerr is not None or w2 is not None else None,
                )
            )
        _artist = _s

    elif histtype == "fill":
        for i in range(len(hists)):
            _kwargs = _chunked_kwargs[i]
            _f = ax.stairs(h[i], final_bins, label=_labels[i], fill=True, **_kwargs)
            return_artists.append(StairsArtists(_f, None, None))
        _artist = _f

    elif histtype == "errorbar":
        err_defaults = {
            "linestyle": "none",
            "marker": ".",
            "markersize": 10.0,
            "elinewidth": 1,
        }
        _yerri: list[float] | None
        if xerr is True:
            _xerr = _bin_widths / 2
        elif isinstance(xerr, (int, float)):
            _xerr = xerr

        for i in range(len(hists)):
            if yerr is not None or w2 is not None:
                _yerri = [_yerr_lo[i], _yerr_hi[i]]
            else:
                _yerri = None
            _e = ax.errorbar(
                _bin_centers,
                h[i],
                yerr=_yerri,
                xerr=_xerr if xerr else None,
                label=_labels[i],
                **soft_update_kwargs(_chunked_kwargs[i], err_defaults),
            )
            return_artists.append(ErrorBarArtists(_e))

        _artist = ax.plot(_bin_centers, h[0], lw=0, ms=0, alpha=0)[0]

    # Add sticky edges for autoscale
    _artist.sticky_edges.y.append(0)

    if xtick_labels is None:
        if binticks:
            _slice = int(round(float(len(final_bins)) / len(ax.get_xticks()))) + 1
            ax.set_xticks(final_bins[::_slice])
    else:
        ax.set_xticks(_bin_centers)
        ax.set_xticklabels(xtick_labels)

    if x_axes_label:
        ax.set_xlabel(x_axes_label)

    return return_artists


def hist2dplot(
    H,
    xbins=None,
    ybins=None,
    labels=None,
    cbar=True,
    cbarsize="7%",
    cbarpad=0.2,
    cbarpos="right",
    cbarextend=False,
    cmin=None,
    cmax=None,
    ax=None,
    **kwargs,
):
    """
    Create a 2D histogram plot from `np.histogram`-like inputs.

    Parameters
    ----------
    H : object
        Histogram object with containing values and optionally bins. Can be:

        - `np.histogram` tuple
        - `boost_histogram` histogram object
        - raw histogram values as list of list or 2d-array

    xbins : 1D array-like, optional, default None
        Histogram bins along x axis, if not part of ``H``.
    ybins : 1D array-like, optional, default None
        Histogram bins along y axis, if not part of ``H``.
    labels : 2D array (H-like) or bool, default None, optional
        Array of per-bin labels to display. If ``True`` will
        display numerical values
    cbar : bool, optional, default True
        Draw a colorbar. In contrast to mpl behavious the cbar axes is
        appended in such a way that it doesn't modify the original axes
        width:height ratio.
    cbarsize : str or float, optional, default "7%"
        Colorbar width.
    cbarpad : float, optional, default 0.2
        Colorbar distance from main axis.
    cbarpos : {'right', 'left', 'bottom', 'top'}, optional,  default "right"
        Colorbar position w.r.t main axis.
    cbarextend : bool, optional, default False
        Extends figure size to keep original axes size same as without cbar.
        Only safe for 1 axes per fig.
    cmin : float, optional
        Colorbar minimum.
    cmax : float, optional
        Colorbar maximum.
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched or one is created)
    **kwargs :
        Keyword arguments passed to underlying matplotlib function - pcolormesh.

    Returns
    -------
        Hist2DArtist

    """

    # ax check
    if ax is None:
        ax = plt.gca()
    else:
        if not isinstance(ax, plt.Axes):
            raise ValueError("ax must be a matplotlib Axes object")

    hist = hist_object_handler(H, xbins, ybins)

    # TODO: use Histogram everywhere
    H = hist.values()
    xbins, xtick_labels = get_plottable_protocol_bins(hist.axes[0])
    ybins, ytick_labels = get_plottable_protocol_bins(hist.axes[1])
    xbin_centers = xbins[1:] - np.diff(xbins) / float(2)
    ybin_centers = ybins[1:] - np.diff(ybins) / float(2)

    _x_axes_label = ax.get_xlabel()
    x_axes_label = (
        _x_axes_label if _x_axes_label != "" else get_histogram_axes_title(hist.axes[0])
    )
    _y_axes_label = ax.get_ylabel()
    y_axes_label = (
        _y_axes_label if _y_axes_label != "" else get_histogram_axes_title(hist.axes[1])
    )

    H = H.T

    if cmin is not None:
        H[H < cmin] = None
    if cmax is not None:
        H[H > cmax] = None

    X, Y = np.meshgrid(xbins, ybins)

    kwargs.setdefault("shading", "flat")
    pc = ax.pcolormesh(X, Y, H, **kwargs)

    if x_axes_label:
        ax.set_xlabel(x_axes_label)
    if y_axes_label:
        ax.set_ylabel(y_axes_label)

    ax.set_xlim(xbins[0], xbins[-1])
    ax.set_ylim(ybins[0], ybins[-1])

    if xtick_labels is None:  # Ordered axis
        if len(ax.get_xticks()) > len(xbins) * 0.7:
            ax.set_xticks(xbins)
    else:  # Categorical axis
        ax.set_xticks(xbin_centers)
        ax.set_xticklabels(xtick_labels)
    if ytick_labels is None:
        if len(ax.get_yticks()) > len(ybins) * 0.7:
            ax.set_yticks(ybins)
    else:  # Categorical axis
        ax.set_yticks(ybin_centers)
        ax.set_yticklabels(ytick_labels)

    if cbar:
        cax = append_axes(
            ax, size=cbarsize, pad=cbarpad, position=cbarpos, extend=cbarextend
        )
        cb_obj = plt.colorbar(pc, cax=cax)
    else:
        cb_obj = None

    plt.sca(ax)

    _labels: np.ndarray | None = None
    if isinstance(labels, bool):
        _labels = H if labels else None
    elif np.iterable(labels):
        label_array = np.asarray(labels).T
        if H.shape == label_array.shape:
            _labels = label_array
        else:
            raise ValueError(
                f"Labels input has incorrect shape (expect: {H.shape}, got: {label_array.shape})"
            )
    elif labels is not None:
        raise ValueError(
            "Labels not understood, either specify a bool or a Hist-like array"
        )

    text_artists = []
    if _labels is not None:
        for ix, xc in enumerate(xbin_centers):
            for iy, yc in enumerate(ybin_centers):
                color = (
                    "black"
                    if isLight(pc.cmap(pc.norm(H[iy, ix]))[:-1])
                    else "lightgrey"
                )
                text_artists.append(
                    ax.text(
                        xc, yc, _labels[iy, ix], ha="center", va="center", color=color
                    )
                )

    return ColormeshArtists(pc, cb_obj, text_artists)


#############################################
# Utils
def overlap(ax, bbox, get_vertices=False):
    """
    Find overlap of bbox for drawn elements an axes.
    """
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch, Rectangle

    # From
    # https://github.com/matplotlib/matplotlib/blob/08008d5cb4d1f27692e9aead9a76396adc8f0b19/lib/matplotlib/legend.py#L845
    lines = []
    bboxes = []
    for handle in ax.lines:
        assert isinstance(handle, Line2D)
        path = handle.get_path()
        lines.append(path)
    for handle in ax.collections:
        for path in handle.get_paths():
            lines.append(path.interpolated(20))

    for handle in ax.patches:
        assert isinstance(handle, Patch)

        if isinstance(handle, Rectangle):
            transform = handle.get_data_transform()
            bboxes.append(handle.get_bbox().transformed(transform))
        else:
            transform = handle.get_transform()
            bboxes.append(handle.get_path().get_extents(transform))

    # TODO Possibly other objects

    vertices = np.concatenate([line.vertices for line in lines])
    tvertices = [ax.transData.transform(v) for v in vertices]

    overlap = bbox.count_contains(tvertices) + bbox.count_overlaps(bboxes)

    if get_vertices:
        return overlap, vertices
    else:
        return overlap


def _draw_leg_bbox(ax):
    """
    Draw legend() and fetch it's bbox
    """
    fig = ax.figure
    leg = ax.get_legend()

    fig.canvas.draw()
    return leg.get_frame().get_bbox()


def _draw_text_bbox(ax):
    """
    Draw legend() and fetch it's bbox
    """
    fig = ax.figure
    textboxes = [k for k in ax.get_children() if type(k) == AnchoredText]
    if len(textboxes) > 1:
        print("Warning: More than one textbox found")
        for box in textboxes:
            if box.loc in [1, 2]:
                bbox = box.get_tightbbox(fig.canvas.renderer)
    else:
        bbox = textboxes[0].get_tightbbox(fig.canvas.renderer)

    return bbox


def yscale_legend(ax=None):
    """
    Automatically scale y-axis up to fit in legend()
    """
    if ax is None:
        ax = plt.gca()

    scale_factor = 10 ** (1.05) if ax.get_yscale() == "log" else 1.05
    while overlap(ax, _draw_leg_bbox(ax)) > 0:
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[-1] * scale_factor)
        ax.figure.canvas.draw()
    return ax


def yscale_text(ax=None):
    """
    Automatically scale y-axis up to fit AnchoredText
    """
    if ax is None:
        ax = plt.gca()

    while overlap(ax, _draw_text_bbox(ax)) > 0:
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[-1] * 1.1)
        ax.figure.canvas.draw()
    return ax


def ylow(ax=None, ylow=None):
    """
    Set lower y limit to 0 if not data/errors go lower.
    Or set a specific value
    """
    if ax is None:
        ax = plt.gca()

    if ax.get_yaxis().get_scale() == "log":
        return ax

    if ylow is None:
        # Check full figsize below 0
        bbox = Bbox.from_bounds(
            0, 0, ax.get_window_extent().width, -ax.get_window_extent().height
        )
        if overlap(ax, bbox) == 0:
            ax.set_ylim(0, None)
        else:
            ydata = overlap(ax, bbox, get_vertices=True)[1][:, 1]
            ax.set_ylim(np.min([np.min(ydata), ax.get_ylim()[0]]), None)

    else:
        ax.set_ylim(0, ax.get_ylim()[-1])

    return ax


def mpl_magic(ax=None, info=True):
    """
    Consolidate all ex-post style adjustments:
        ylow
        yscale_legend
    """
    if ax is None:
        ax = plt.gca()
    if not info:
        print("Running ROOT/CMS style adjustments (hide with info=False):")

    ax = ylow(ax)
    ax = yscale_legend(ax)
    ax = yscale_text(ax)

    return ax


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
        xrel, xabs = axes_size.AddList(self.xsizes).get_size(renderer)
        yrel, yabs = axes_size.AddList(self.ysizes).get_size(renderer)
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

    divider.set_horizontal([RemainderFixed(xsizes, ysizes, divider)] + xsizes)
    divider.set_vertical([RemainderFixed(xsizes, ysizes, divider)] + ysizes)
    return cax


def append_axes(ax, size=0.1, pad=0.1, position="right", extend=False):
    """
    Append a side ax to the current figure and return it.
    Figure is automatically extended along the direction of the added axes to
    accommodate it. Unfortunately can not be reliably chained.
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
        xsizes = xsizes[::-1]
    yhax = divider.append_axes(position, size=margin_size, pad=pad_size)

    if extend:

        def extend_ratio(ax, yhax):
            ax.figure.canvas.draw()
            orig_size = ax.get_position().size
            new_size = sum(itax.get_position().size for itax in [ax, yhax])
            return new_size / orig_size

        if position in ["right"]:
            divider.set_horizontal([axes_size.Fixed(width)] + xsizes)
            fig.set_size_inches(
                fig.get_size_inches()[0] * extend_ratio(ax, yhax)[0],
                fig.get_size_inches()[1],
            )
        elif position in ["left"]:
            divider.set_horizontal(xsizes[::-1] + [axes_size.Fixed(width)])
            fig.set_size_inches(
                fig.get_size_inches()[0] * extend_ratio(ax, yhax)[0],
                fig.get_size_inches()[1],
            )
        elif position in ["top"]:
            divider.set_vertical([axes_size.Fixed(height)] + xsizes[::-1])
            fig.set_size_inches(
                fig.get_size_inches()[0],
                fig.get_size_inches()[1] * extend_ratio(ax, yhax)[1],
            )
            ax.get_shared_x_axes().join(ax, yhax)
        elif position in ["bottom"]:
            divider.set_vertical(xsizes + [axes_size.Fixed(height)])
            fig.set_size_inches(
                fig.get_size_inches()[0],
                fig.get_size_inches()[1] * extend_ratio(ax, yhax)[1],
            )
            ax.get_shared_x_axes().join(ax, yhax)

    return yhax


####################
# Legend Helpers
def hist_legend(ax=None, **kwargs):
    from matplotlib.lines import Line2D

    if ax is None:
        ax = plt.gca()

    handles, labels = ax.get_legend_handles_labels()
    new_handles = [
        Line2D([], [], c=h.get_edgecolor()) if type(h) == mpl.patches.Polygon else h
        for h in handles
    ]
    ax.legend(handles=new_handles[::-1], labels=labels[::-1], **kwargs)

    return ax


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
        raise TypeError(f"Unexpected values type of order: {type(order)}")

    ordered_label_list = [entry for entry in ordered_label_list if entry in labels]
    ordered_label_values = [by_label[k] for k in ordered_label_list]
    if isinstance(order, OrderedDict):
        ordered_label_list = [order[k] for k in ordered_label_list]
    return ordered_label_values, ordered_label_list


#########################
# Other helpers
def save_variations(fig, name, text_list=None, exp=None):
    """[summary]

    Parameters
    ----------
    fig : figure
    name : str
        Savename to pass to `plt.savefig()`
    text_list : list, optional
        Variations of ExpSuffix text object to cycle
        through
    exp : str, optional
        Change experiment name label
    """
    if text_list is None:
        text_list = ["Preliminary", ""]

    from mplhep.label import ExpSuffix, ExpText

    for text in text_list:
        for ax in fig.get_axes():
            exp_labels = [t for t in ax.get_children() if isinstance(t, ExpText)]
            suffixes = [t for t in ax.get_children() if isinstance(t, ExpSuffix)]
            for exp_label, suffix_text in zip(exp_labels, suffixes):
                if exp is not None:
                    exp_label.set_text(exp)
                suffix_text.set_text(text)
        name_ext = "" if text == "" else "_" + text.lower()
        if exp is not None:
            name_ext = exp.lower() + name_ext
        save_name = name.split(".")[0] + name_ext + "." + name.split(".")[1]
        fig.savefig(save_name)
