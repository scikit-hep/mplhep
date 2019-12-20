import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Bbox
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

from .error_estimation import poisson_interval

# mpl updated to new methods
from packaging import version
_mpl_up_version = '3.3.3'
_mpl_up = version.parse(mpl.__version__) >= version.parse(_mpl_up_version)

########################################
# Histogram plotter


def histplot(h, bins, weights=None, yerr=None, variances=None,
             stack=False, density=False,
             histtype='step', label=None, edges=False, binticks=False,
             ax=None, **kwargs):

    if ax is None:
        ax = plt.gca()
    else:
        if not isinstance(ax, plt.Axes):
            raise ValueError("ax must be a matplotlib Axes object")

    # arg check
    if histtype != 'step':
        assert edges is False, "edges is only valid with histtype='step'"
    _allowed_histtype = ['fill', 'step', 'errorbar']
    _err_message = "Select 'histtype' from: {}".format(_allowed_histtype)
    assert histtype in _allowed_histtype, _err_message
    # Preprocess
    h = np.asarray(h)
    bins = np.asarray(bins)
    assert bins.ndim == 1, "bins need to be 1 dimensional"
    assert bins.shape[0] == h.shape[-1] + 1, "len along main axis of h has "\
                                             "to be smaller by 1 than len "\
                                             "of bins"
    assert variances is None or yerr is None, "Can only supply errors or variances"

    if h.ndim == 1:
        _nh = 1
    elif h.ndim > 1:
        _nh = len(h)
    else:
        raise ValueError("Input cannot be handled")

    # Find a better way to unwrap to "real" dimentionality
    if h.ndim == 2 and len(h) == 1:  # Unwrap if [[1,2,3]]
        h = h[0]

    if label is None:
        _labels = [None] * _nh
    elif isinstance(label, str):
        _labels = [label] * _nh
    elif not np.iterable(label):
        _labels = [str(label)] * _nh
    else:
        _labels = [str(lab) for lab in label]

    # Apply weights
    if weights is not None:
        weights = np.asarray(weights)
        h = h * weights

    _bin_widths = np.diff(bins)
    _bin_centers = bins[1:] - _bin_widths / float(2)

    if yerr is not None:
        # yerr is array
        if hasattr(yerr, '__len__'):
            _yerr = np.asarray(yerr)
            if _yerr.ndim == 3 and len(_yerr) == 1:  # Unwrap if [[1,2,3]]
                _yerr = _yerr[0][0]
        # yerr is a number
        elif isinstance(yerr, (int, float)) and not isinstance(yerr, bool):
            _yerr = np.ones_like(h) * yerr
        # yerr is automatic
        else:
            if yerr is True:
                assert stack is False, "Automatic errorbars not defined for " \
                                       "stacked plot"
                _yerr = np.sqrt(h)

    elif variances is not None:
        int_variances = np.around(variances).astype(int)
        if np.all(np.isclose(variances, int_variances, 0.000001)):
            # If variances are integers (true data hist), calculate Garwood interval
            _yerr = np.abs(poisson_interval(h, variances) - h)
        else:
            # Variances to errors directly if specified previously
            _yerr = np.sqrt(variances)
    else:
        _yerr = None

    if density:
        _norm = (np.sum(h, axis=1 if h.ndim > 1 else 0) /
                 (np.ones_like(h) * _bin_widths).T).T
        h = h / _norm

        if _yerr is not None:
            _yerr /= _norm

    # Stack
    if stack and _nh > 1:
        h = np.cumsum(h, axis=0)[::-1]
        _labels = _labels[::-1]

    if not _mpl_up:
        _where = 'post'
    elif edges:
        _where = 'edges'
    else:
        _where = 'between'

    if histtype == 'step':
        if _nh == 1:
            if not _mpl_up:  # Back-comp
                if edges:
                    # 3.6 and up
                    # _bins = [bins[0], *bins, bins[-1]]
                    # _h = [0, *np.r_[h, h[-1]], 0]
                    _bins = np.r_[bins[0], bins, bins[-1]]
                    _h = np.r_[0, h, h[-1], 0]
                else:
                    _bins, _h = bins, np.r_[h, h[-1]]
            else:
                _h = h
                _bins = bins
            _label = _labels[0]
            _step_label = _label if yerr is None else None
            _s, = ax.step(_bins, _h, where=_where, label=_step_label, **kwargs)
            if yerr is not None or variances is not None:
                ax.errorbar(_bin_centers, h, yerr=_yerr, color=_s.get_color(),
                            ls='none', **kwargs)
                ax.errorbar([], [], yerr=1, xerr=1, color=_s.get_color(),
                            label=_label)
        else:
            for i in range(_nh):
                if not _mpl_up:  # Back-comp
                    if edges:
                        # 3.6 and up
                        # _bins = [bins[0], *bins, bins[-1]]
                        # _h = [0, *np.r_[h[i], h[i][-1]], 0]
                        _bins = np.r_[bins[0], bins, bins[-1]]
                        _h = np.r_[0, h[i], h[i][-1], 0]
                    else:
                        _bins, _h = bins, np.r_[h[i], h[i][-1]]
                else:
                    _h = h[i]
                _label = _labels[i]
                _step_label = _label if yerr is None else None
                _s, = ax.step(_bins, _h, where=_where, label=_step_label,
                              **kwargs)
                if yerr is not None or variances is not None:
                    ax.errorbar(_bin_centers, h[i], yerr=_yerr[i],
                                color=_s.get_color(), ls='none', **kwargs)
                    ax.errorbar([], [], yerr=1, xerr=1, color=_s.get_color(),
                                label=_label)

    elif histtype == 'fill':
        if _nh == 1:
            if not _mpl_up:
                _h = np.r_[h, h[-1]]
            else:
                _h = h
            ax.fill_between(bins, _h, step=_where, label=_labels[0], **kwargs)
        else:
            for i in range(_nh):
                if not _mpl_up:
                    _h = np.r_[h[i], h[i][-1]]
                else:
                    _h = h[i]
                ax.fill_between(bins, _h, step=_where,
                                label=_labels[i], **kwargs)

    elif histtype == 'errorbar':
        err_defaults = {
            'linestyle': 'none',
            'marker': '.',
            'markersize': 10.,
            'elinewidth': 1,
        }
        if _yerr is None:
            _yerr = np.zeros_like(h)
        for k, v in err_defaults.items():
            if k not in kwargs.keys():
                kwargs[k] = v
        if _nh == 1:
            ax.errorbar(_bin_centers, h, yerr=_yerr, ls='none',
                        label=_labels[0], **kwargs)
        else:
            for i in range(_nh):
                ax.errorbar(_bin_centers, h[i], yerr=_yerr[i], ls='none',
                            label=_labels[0], **kwargs)

    # Get current
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin if np.min(h) < 0 else 0, np.max([ymax, 1.2 * np.max(h)]))

    if binticks:
        _slice = int(round(float(len(bins)) / len(ax.get_xticks()))) + 1
        ax.set_xticks(bins[::_slice])

    return ax


def hist2dplot(H, xbins=None, ybins=None, weights=None, labels=None,
               cbar=True, cbarsize="7%", cbarpad=0.2, cbarpos='right',
               cmin=None, cmax=None, ax=None, **kwargs):

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

    pc = ax.pcolormesh(X, Y, H, **kwargs)

    ax.set_xlim(xbins[0], xbins[-1])
    ax.set_ylim(ybins[0], ybins[-1])

    if len(ax.get_xticks()) > len(xbins) * 0.7:
        ax.set_xticks(xbins)
    if len(ax.get_yticks()) > len(ybins) * 0.7:
        ax.set_yticks(ybins)

    if cbar:
        cax = append_axes(ax, size=cbarsize, pad=cbarpad, position=cbarpos)
        plt.colorbar(pc, cax=cax)

    if labels is not None:
        if np.array_equiv(H, labels):
            _labels = labels
        elif labels is True:
            _labels = H
        elif labels is False:
            pass
        else:
            raise ValueError('Labels not understood, either specify a bool or a'
                             'Histlike array ')
        _xbin_centers = xbins[1:] - np.diff(xbins) / float(2)
        _ybin_centers = ybins[1:] - np.diff(ybins) / float(2)
        for ix, xc in enumerate(_xbin_centers):
            for iy, yc in enumerate(_ybin_centers):
                color = 'black' if pc.norm(H[iy, ix]) > 0.5 else 'lightgrey'
                ax.text(xc, yc, _labels[iy, ix], ha='center', va='center', color=color)

    return H, xbins, ybins, pc


#############################################
# Utils
def r_align(ax=None):
    """
    Align axes labels to the right
    """
    if ax is None:
        ax = plt.gca()

    ax.set_xlabel(ax.get_xlabel(), ha='right', x=1)
    ax.set_ylabel(ax.get_ylabel(), ha='right', y=1)

    return ax


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

    vertices = np.concatenate([l.vertices for l in lines])
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

    return ax, bbox


def yscale_legend(ax=None):
    """
    Automatically scale y-axis up to fit in legend()
    """
    if ax is None:
        ax = plt.gca()

    while overlap(*_draw_leg_bbox(ax)) > 0:
        ax = plt.gca()
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[-1] * 1.05)
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
        bbox = Bbox.from_bounds(0, 0,
                                ax.get_window_extent().width,
                                -ax.get_window_extent().height)
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
        r_align
        ylow
        yscale_legend
    """
    if ax is None:
        ax = plt.gca()
    if not info:
        print("Running ROOT/CMS style adjustments (hide with info=False):")

    ax = r_align(ax)
    ax = ylow(ax)
    ax = yscale_legend(ax)

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
    Parameters: aspect: float, optional
                        aspect ratio
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
            self.div._fig.transFigure)
        w = bb.width / self.div._fig.dpi - xabs
        h = bb.height / self.div._fig.dpi - yabs
        return 0, min([w, h])


def make_square_add_cbar(ax, size=.4, pad=0.1):
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
                if position in ['right', 'left']:
                    fraction = width * float(fraction.strip('%')) / 100
                elif position in ['top', 'bottom']:
                    fraction = height * float(fraction.strip('%')) / 100
        return fraction

    size = convert(size)
    pad = convert(pad)

    divider = make_axes_locatable(ax)
    margin_size = axes_size.Fixed(size)
    pad_size = axes_size.Fixed(pad)
    xsizes = [pad_size, margin_size]
    if position in ['top', 'bottom']:
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
        fig.set_size_inches(fig.get_size_inches()[0] * extend_ratio(ax)[0],
                            fig.get_size_inches()[1])
    elif position in ["left"]:
        divider.set_horizontal(xsizes[::-1] + [axes_size.Fixed(width)])
        fig.set_size_inches(fig.get_size_inches()[0] * extend_ratio(ax)[0],
                            fig.get_size_inches()[1])
    elif position in ['top']:
        divider.set_vertical([axes_size.Fixed(height)] + xsizes[::-1])
        fig.set_size_inches(fig.get_size_inches()[0],
                            fig.get_size_inches()[1] * extend_ratio(ax)[1])
        ax.get_shared_x_axes().join(ax, yhax)
    elif position in ['bottom']:
        divider.set_vertical(xsizes + [axes_size.Fixed(height)])
        fig.set_size_inches(fig.get_size_inches()[0],
                            fig.get_size_inches()[1] * extend_ratio(ax)[1])
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
    ax.legend(handles=new_handles[::-1],
              labels=labels[::-1],
              **kwargs
              )

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
        raise TypeError('Unexpected values type of order: {}'.format(
            type(order)))

    ordered_label_list = [
        entry for entry in ordered_label_list if entry in labels
    ]
    ordered_label_values = [by_label[k] for k in ordered_label_list]
    if isinstance(order, OrderedDict):
        ordered_label_list = [order[k] for k in ordered_label_list]
    return ordered_label_values, ordered_label_list
