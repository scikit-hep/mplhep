import warnings
import collections
from collections import namedtuple
import mplhep._deprecate as deprecate
from typing import Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Bbox
from matplotlib.offsetbox import AnchoredText
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

from .error_estimation import poisson_interval
from .utils import get_histogram_axes_title

# mpl updated to new methods
# from packaging import version
# _mpl_up_version = "3.3.3"
# _mpl_up = version.parse(mpl.__version__) >= version.parse(_mpl_up_version)

StepArtists = namedtuple("StepArtists", "step errorbar legend_artist")
FillArtists = namedtuple("FillArtists", "fill_between")
ErrorBarArtists = namedtuple("ErrorBarArtists", "errorbar")
ColormeshArtists = namedtuple("ColormeshArtists", "pcolormesh cbar")

Hist1DArtists = Union[StepArtists, FillArtists, ErrorBarArtists]
Hist2DArtists = ColormeshArtists


########################################
# Histogram plotter
def histplot(
    H,  # Histogram object, tuple or array
    bins=None,  # Bins to be supplied when h is a value array or iterable of arrays
    *,
    yerr=None,
    w2=None,
    stack=False,
    density=False,
    binwnorm=None,
    histtype="step",
    label=None,
    edges=True,
    binticks=False,
    ax=None,
    **kwargs
):
    """
    Create a 1D histogram plot from `np.histogram`-like inputs.
    Parameters
    ----------
        H : object
            Histogram object with containing values and optionally bins. Can be:

            - `np.histogram` tuple
            - `boost_histogram` histogram object
            - raw histogram values, provided `bins` is specified.

        bins : iterable, optional
            Histogram bins, if not part of ``h``.
        yerr : iterable or bool, optional
            Histogram uncertainties. Following modes are supported:
            - True, sqrt(N) errors or poissonian interval when ``w2`` is specified
            - shape(N) array of for one sided errors or list thereof
            - shape(Nx2) array of for two sided errors or list thereof
        w2 : iterable, optional
            Sum of the histogram weights squared for poissonian interval error caclulation
        stack : bool, optional
            Whether to stack or overlay non-axis dimension (if it exists
        density : bool, optional
            If true, convert sum weights to probability density (i.e. integrates to 1 over domain of axis)
            (Note: this option conflicts with ``binwnorm``)de
        binwnorm : float, optional
            If true, convert sum weights to bin-width-normalized, with unit equal to supplied value (usually you want to specify 1.)
        histtype: {'step', 'fill', 'errorbar'}, optional, default: "step"
            Type of histogram to plot:

            - "step": skyline/step/outline of a histogram using `plt.step <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.step.html#matplotlib.axes.Axes.step>`_
            - "fill": filled histogram using `plt.fill_between <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.step.html#matplotlib.axes.Axes.step>`_
            - "errorbar": single marker histogram using `plt.errorbar <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.step.html#matplotlib.axes.Axes.step>`_

        label : str or list, optional
            Label for legend entry.
        edges : bool, default: True, optional
            Specifies whether to draw first and last edges of the histogram
        binticks : bool, optional
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

    x_axes_label = ""  # Only added in if non-blank

    # arg check
    _allowed_histtype = ["fill", "step", "errorbar"]
    _err_message = "Select 'histtype' from: {}".format(_allowed_histtype)
    assert histtype in _allowed_histtype, _err_message

    def hist_object_handler(h, check_only=False):
        if hasattr(h, "axes") and hasattr(h, "to_numpy"):
            # Boost histogram / Hist compat
            # TODO: support different storages
            if len(h.axes) != 1:
                raise ValueError("Must have only 1 axis")
            # FIXME x_axes_label = get_histogram_axes_title(h.axes[0])
            h, bins = h.to_numpy()

        elif hasattr(h, "to_numpy"):
            # Generic (possibly Uproot 4)
            _tup = h.to_numpy(flow=False)
            if len(_tup) != 2:
                raise ValueError("to_numpy() method not understood")
            else:
                h, bins = _tup

        elif hasattr(h, "numpy"):
            # uproot/TH1
            _tup = h.numpy()
            if len(_tup) != 2:
                raise ValueError("numpy() method not understood")
            else:
                h, bins = _tup

        elif isinstance(h, tuple):
            # Numpy histogram tuple
            h, bins = h

        else:
            h = h
            bins = None

        if check_only:
            return True if bins is not None else False
        else:
            return np.asarray(h).astype(float), np.asarray(bins).astype(float)

    # Try to understand input
    if type(H) is list:
        # A list of objects
        type_check = [hist_object_handler(h, check_only=True) for h in H]

        if all(type_check):
            # All objects are understandable
            NH = len(type_check)
            _H, _bins = [], []
            for h in H:
                h, bins = hist_object_handler(h)
                _H.append(h)
                _bins.append(bins)
            if len(set(map(len, _H))) != 1:
                raise ValueError(
                    "Plotting multiple histograms with different binning is not supported"
                )
            h = np.asarray(_H).astype(float)
            bins = _bins[0]
        elif any(type_check):
            # Some objects are not understandable
            raise ValueError("Some hist objects were not recognized")
        else:
            # List of lists or arrays
            h = np.asarray(H).astype(float)
            bins = np.asarray(bins).astype(float) if bins is not None else None
            NH = len(h) if h.ndim > 1 else 1
    else:
        # Single object, numpy array, 2D array
        if hist_object_handler(H, check_only=True):
            NH = 1
            h, bins = hist_object_handler(H)
        else:
            # 2D array
            h = np.asarray(H).astype(float)
            bins = np.asarray(bins).astype(float) if bins is not None else None
            NH = len(h) if h.ndim > 1 else 1

    if bins is None and NH == 1:
        bins = np.arange(len(h) + 1)
    elif bins is None and NH > 1:
        bins = [np.arange(len(_h) + 1) for _h in h][0]

    # Convert 1/0 etc to real bools
    stack = bool(stack)
    density = bool(density)
    edges = bool(edges)
    binticks = bool(binticks)
    assert bins.ndim == 1, "bins need to be 1 dimensional"
    # assert bins.shape[0] == h.shape[-1] + 1, (
    #     "len along main axis of h has " "to be smaller by 1 than len " "of bins"
    # )
    assert w2 is None or yerr is None, "Can only supply errors or w2"

    if label is None:
        _labels = [None] * NH
    elif isinstance(label, str):
        _labels = [label] * NH
    elif not np.iterable(label):
        _labels = [str(label)] * NH
    else:
        _labels = [str(lab) for lab in label]

    def iterable_not_string(arg):
        return isinstance(arg, collections.abc.Iterable) and not isinstance(arg, str)

    _chunked_kwargs = []
    for _i in range(NH):
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

    _bin_widths = np.diff(bins)
    _bin_centers = bins[1:] - _bin_widths / float(2)

    ############################
    # yerr calculation
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
                assert stack is False, (
                    "Automatic errorbars not defined for " "stacked plot"
                )
                _yerr = np.sqrt(h)

    elif w2 is not None:
        int_w2 = np.around(w2).astype(int)
        if np.all(np.isclose(w2, int_w2, 0.000001)):
            # If w2 are integers (true data hist), calculate Garwood interval
            _yerr = np.abs(poisson_interval(h, w2) - h)
        else:
            # w2 to errors directly if specified previously
            _yerr = np.sqrt(w2)
    else:
        _yerr = None

    ############################
    # Stacking, norming, density
    def get_stack(_h):
        if NH > 1:
            return np.cumsum(_h, axis=0)
        else:
            return _h

    def get_density(h, density=True, binwnorm=None, bins=bins):
        assert (not density) ^ (
            binwnorm is None
        ), "Can only calculate density or binwnorm"
        per_hist_norm = np.sum(h, axis=1 if NH > 1 else 0)
        if binwnorm is not None:
            overallnorm = binwnorm * per_hist_norm
        else:
            overallnorm = np.ones(NH)
        binnorms = np.outer(overallnorm, np.ones_like(bins[:-1]))
        binnorms /= np.outer(np.diff(bins), per_hist_norm).T
        if binnorms.ndim == 2 and len(binnorms) == 1:  # Unwrap if [[1,2,3]]
            binnorms = binnorms[0]
        return binnorms

    if density or binwnorm is not None:
        density_arr = get_density(h, density, binwnorm)
        if stack:
            h = get_stack(h)
            h *= get_density(h, density, binwnorm)[-1]
        else:
            h *= density_arr
        if _yerr is not None:
            for i in range(len(density_arr)):
                _yerr[i] = _yerr[i] * density_arr[i]

    if stack and not density and binwnorm is None:
        h = get_stack(h)

    # Stack
    if stack and NH > 1:
        h = h[::-1]
        _labels = _labels[::-1]
        _chunked_kwargs = _chunked_kwargs[::-1]

    #################################
    # Split and reshape for iteration
    h = h.reshape(NH, -1)
    if yerr is not None:
        if _yerr.ndim == 3:
            # Already correct format
            pass
        elif _yerr.ndim == 2 and NH == 1:
            # Broadcast ndim 2 to ndim 3
            if _yerr.shape[-2] == 2:  # [[1,1], [1,1]]
                _yerr = _yerr.reshape(NH, 2, _yerr.shape[-1])
            elif _yerr.shape[-2] == 1:  # [[1,1]]
                _yerr = np.tile(_yerr, 2).reshape(NH, 2, _yerr.shape[-1])
            else:
                raise ValueError("yerr format is not understood")
        elif _yerr.ndim == 2:
            # Broadcast yerr (nh, N) to (nh, 2, N)
            _yerr = np.tile(_yerr, 2).reshape(NH, 2, _yerr.shape[-1])
        elif _yerr.ndim == 1:
            # Broadcast yerr (1, N) to (nh, 2, N)
            _yerr = np.tile(_yerr, 2 * NH).reshape(NH, 2, _yerr.shape[-1])
        else:
            raise ValueError("yerr format is not understood")
        # Split
        _yerr_lo = _yerr[:, 0]
        _yerr_hi = _yerr[:, 1]

    ##########
    # Plotting
    return_artists = []
    if histtype == "step":
        for i in range(NH):
            if edges:
                _bins = [bins[0], *bins, bins[-1]]
                _h = [0, *h[i], h[i][-1], 0]
            else:
                _bins, _h = bins, [*h[i], h[i][-1]]
            _kwargs = _chunked_kwargs[i]
            _label = _labels[i]
            _step_label = _label if yerr is None else None
            (_s,) = ax.step(
                _bins, _h, where="post", label=_step_label, marker="", **_kwargs
            )
            if yerr is not None or w2 is not None:
                if "color" not in _kwargs:
                    _kwargs["color"] = _s.get_color()
                _e = ax.errorbar(
                    _bin_centers,
                    h[i],
                    yerr=[_yerr_lo[i], _yerr_hi[i]],
                    linestyle="none",
                    **_kwargs
                )
                _eleg = ax.errorbar(
                    [], [], yerr=1, xerr=1, color=_s.get_color(), label=_label
                )
            return_artists.append(
                StepArtists(
                    _s,
                    _e if yerr is not None or w2 is not None else None,
                    _eleg if yerr is not None or w2 is not None else None,
                )
            )
        _artist = _s

    elif histtype == "fill":
        for i in range(NH):
            _h = np.r_[h[i], h[i][-1]]
            _kwargs = _chunked_kwargs[i]
            _f = ax.fill_between(bins, _h, step="post", label=_labels[i], **_kwargs)
        return_artists.append(FillArtists(_f))
        _artist = _f

    elif histtype == "errorbar":
        err_defaults = {
            "linestyle": "none",
            "marker": ".",
            "markersize": 10.0,
            "elinewidth": 1,
        }
        for k, v in err_defaults.items():
            if k not in kwargs.keys():
                kwargs[k] = v
            for kwarg_row in _chunked_kwargs:
                if k not in kwarg_row.keys():
                    kwarg_row[k] = v

        for i in range(NH):
            if yerr is None:
                _yerri = None
            else:
                _yerri = [_yerr_lo[i], _yerr_hi[i]]
            _e = ax.errorbar(
                _bin_centers, h[i], yerr=_yerri, label=_labels[i], **_chunked_kwargs[i]
            )
            return_artists.append(ErrorBarArtists(_e))
        _artist = ax.plot(_bin_centers, h[0], lw=0, ms=0, alpha=0)[0]
    # Add sticky edges for autoscale
    _artist.sticky_edges.y.append(0)

    if binticks:
        _slice = int(round(float(len(bins)) / len(ax.get_xticks()))) + 1
        ax.set_xticks(bins[::_slice])

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
    cmin=None,
    cmax=None,
    ax=None,
    **kwargs
):
    """
    Create a 2D histogram plot from `np.histogram`-like inputs.

    Parameters
    ----------
    H : object
        Histogram object with containing values and optionally bins. Can be:

        - `np.histogram` tuple
        - `boost_histogram` histogram object
        - raw histogram values, provided `bins` is specified.

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

    x_axes_label = ""
    y_axes_label = ""

    # Input check
    if hasattr(H, "axes") and hasattr(H, "to_numpy"):
        # Hist compat
        if len(H.axes) != 2:
            raise ValueError("Not a 2D histogram")

        x_axes_label = get_histogram_axes_title(H.axes[0])
        y_axes_label = get_histogram_axes_title(H.axes[1])

        H, xbins, ybins = H.to_numpy()

    elif hasattr(H, "to_numpy"):
        # Generic (Uproot 4) support
        H, xbins, ybins = H.to_numpy(flow=False)

    elif hasattr(H, "numpy"):
        # uproot/TH2
        _tup = H.numpy()
        if len(_tup) != 2:
            raise ValueError("numpy() method not understood")
        else:
            H, xy = _tup
            if len(xy) == 1 and isinstance(xy, list):
                if len(xy[0]) == 2 and isinstance(xy[0], tuple):
                    xbins, ybins = xy[0]
                else:
                    raise ValueError("Input not understood")
            else:
                raise ValueError("Input not understood")

    H = H.T

    if ax is None:
        ax = plt.gca()

    if xbins is None:
        xbins = np.arange(H.shape[1] + 1)
    if ybins is None:
        ybins = np.arange(H.shape[0] + 1)

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

    if len(ax.get_xticks()) > len(xbins) * 0.7:
        ax.set_xticks(xbins)
    if len(ax.get_yticks()) > len(ybins) * 0.7:
        ax.set_yticks(ybins)

    if cbar:
        cax = append_axes(ax, size=cbarsize, pad=cbarpad, position=cbarpos)
        cb_obj = plt.colorbar(pc, cax=cax)
    else:
        cb_obj = None

    plt.sca(ax)

    if labels is not None:
        if labels is True:
            _labels = H
        elif H.shape == labels.shape:
            _labels = labels
        elif labels is False:
            pass
        else:
            raise ValueError(
                "Labels not understood, either specify a bool or a" "Histlike array "
            )
        _xbin_centers = xbins[1:] - np.diff(xbins) / float(2)
        _ybin_centers = ybins[1:] - np.diff(ybins) / float(2)
        for ix, xc in enumerate(_xbin_centers):
            for iy, yc in enumerate(_ybin_centers):
                color = "black" if pc.norm(H[iy, ix]) > 0.5 else "lightgrey"
                ax.text(xc, yc, _labels[iy, ix], ha="center", va="center", color=color)

    return ColormeshArtists(pc, cb_obj)


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
    bbox = leg.get_frame().get_bbox()

    return bbox


def _draw_text_bbox(ax):
    """
    Draw legend() and fetch it's bbox
    """
    fig = ax.figure
    textboxes = []
    for k in ax.get_children():
        if type(k) == AnchoredText:
            textboxes.append(k)

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

    while overlap(ax, _draw_leg_bbox(ax)) > 0:
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[-1] * 1.05)
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


def append_axes(ax, size=0.1, pad=0.1, position="right"):
    """
    Append a side ax to the current figure and return it.
    Figure is automatically extended along the direction of the added axes to
    accommodate it. Unfortunately can not be reliably chained.
    """
    fig = ax.figure
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height

    def convert(fraction, position=position):
        if isinstance(fraction, str):
            if fraction.endswith("%"):
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

    def extend_ratio(ax):
        ax.figure.canvas.draw()
        orig_size = ax.get_position().size
        new_size = 0
        for itax in ax.figure.axes:
            new_size += itax.get_position().size

        return new_size / orig_size

    if position in ["right"]:
        divider.set_horizontal([axes_size.Fixed(width)] + xsizes)
        fig.set_size_inches(
            fig.get_size_inches()[0] * extend_ratio(ax)[0], fig.get_size_inches()[1]
        )
    elif position in ["left"]:
        divider.set_horizontal(xsizes[::-1] + [axes_size.Fixed(width)])
        fig.set_size_inches(
            fig.get_size_inches()[0] * extend_ratio(ax)[0], fig.get_size_inches()[1]
        )
    elif position in ["top"]:
        divider.set_vertical([axes_size.Fixed(height)] + xsizes[::-1])
        fig.set_size_inches(
            fig.get_size_inches()[0], fig.get_size_inches()[1] * extend_ratio(ax)[1]
        )
        ax.get_shared_x_axes().join(ax, yhax)
    elif position in ["bottom"]:
        divider.set_vertical(xsizes + [axes_size.Fixed(height)])
        fig.set_size_inches(
            fig.get_size_inches()[0], fig.get_size_inches()[1] * extend_ratio(ax)[1]
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
    from collections import OrderedDict

    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))

    if isinstance(order, OrderedDict):
        ordered_label_list = list(order.keys())
    elif isinstance(order, (list, tuple, np.ndarray)):
        ordered_label_list = order
    elif order is None:
        ordered_label_list = labels
    else:
        raise TypeError("Unexpected values type of order: {}".format(type(order)))

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

    from mplhep.label import ExpText, ExpSuffix

    for text in text_list:
        for ax in fig.get_axes():
            exp_labels = [t for t in ax.get_children() if isinstance(t, ExpText)]
            suffixes = [t for t in ax.get_children() if isinstance(t, ExpSuffix)]
            for exp_label, suffix_text in zip(exp_labels, suffixes):
                if exp is not None:
                    exp_label.set_text(exp)
                suffix_text.set_text(text)
        if text == "":
            name_ext = ""
        else:
            name_ext = "_" + text.lower()
        if exp is not None:
            name_ext = exp.lower() + name_ext
        save_name = name.split(".")[0] + name_ext + "." + name.split(".")[1]
        fig.savefig(save_name)
