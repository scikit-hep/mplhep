import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Bbox
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size


########################################
# Histogram plotter

def histplot(h, bins, weights=None, yerr=None,
             stack=False, density=False,
             histtype='step', label=None, edges=False,
             ax=None, **kwargs):

    if ax is None:
        ax = plt.gca()
    else:
        if not isinstance(ax, plt.Axes):
            raise ValueError("ax must be a matplotlib Axes object")

    # mpl updated to new methods
    _mpl_up = np.prod([int(v) >= int(ref)
                       for v, ref in zip(mpl.__version__.split('.')[:3],
                                         [3, 3, 3])
                       ]).astype(bool)

    # arg check
    if histtype != 'step':
        assert edges is False, "edges is only valid with histtype='step'"
    # Preprocess
    h = np.asarray(h)
    bins = np.asarray(bins)
    assert bins.ndim == 1, "bins need to be 1 dimensional"
    assert bins.shape[0] == h.shape[-1] + 1, "len along main axis of h has "\
                                             "to be smaller by 1 than len "\
                                             "of bins"
    _nh = h.ndim

    if label is None:
        _labels = [None]*_nh
    elif isinstance(label, str):
        _labels = [label]*_nh
    elif not np.iterable(label):
        _labels = [str(label)]*_nh
    else:
        _labels = [str(lab) for lab in label]

    # Get current
    ymin, ymax = ax.get_ylim()

    # Apply weights
    if weights is not None:
        weights = np.asarray(weights)
        h = h * weights

    _bin_widths = np.diff(bins)
    if density:
        _norm = (np.sum(h, axis=1 if h.ndim > 1 else 0)
                 / (np.ones_like(h) * _bin_widths).T).T
        h = h / _norm

    if yerr is not None:
        if hasattr(yerr, '__len__'):
            _yerr = np.asarray(yerr)
        else:
            if yerr is True:
                assert stack is False, "Automatic errorbars not defined for " \
                                       " stacked plot"
                _yerr = np.sqrt(h)
        _bin_centers = bins[1:] - _bin_widths / 2

    # Stack
    if stack and _nh > 1:
        h = np.cumsum(h, axis=0)[::-1]

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
                    _bins = [bins[0], *bins, bins[-1]]
                    _h = [0, *np.r_[h, h[-1]], 0]
                else:
                    _bins, _h = bins, np.r_[h, h[-1]]
            else:
                _h = h
                _bins = bins
            _label = _labels[0]
            _step_label = _label if yerr is None else None
            _s, = ax.step(_bins, _h, where=_where, label=_step_label, **kwargs)
            if yerr is not None:
                ax.errorbar(_bin_centers, h, yerr=_yerr, color=_s.get_color(),
                            ls='none', **kwargs)
                ax.errorbar([], [], yerr=1, xerr=1, color=_s.get_color(),
                            label=_label)
        else:
            for i in range(_nh):
                if not _mpl_up:  # Back-comp
                    if edges:
                        _bins = [bins[0], *bins, bins[-1]]
                        _h = [0, *np.r_[h[i], h[i][-1]], 0]
                    else:
                        _bins, _h = bins, np.r_[h[i], h[i][-1]]
                else:
                    _h = h[i]
                _label = _labels[i]
                _step_label = _label if yerr is None else None
                _s, = ax.step(_bins, _h, where=_where, label=_step_label,
                              **kwargs)
                if yerr is not None:
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
            ax.fill_between(bins, _h, step=_where, **kwargs)
        else:
            for i in range(_nh):
                if not _mpl_up:
                    _h = np.r_[h[i], h[i][-1]]
                else:
                    _h = h[i]
                ax.fill_between(bins, _h, step=_where, **kwargs)

    ax.set_ylim(min(1.05*np.min(h) if np.min(h) < 0 else 0, ymin),
                max(1.05*np.max(h), ymax))

    return ax


def hist2dplot(H, xbins=None, ybins=None, weights=None,
               cbar=True, cbarsize="7%", cbarpad=0.2, cbarpos='right',
               cmin=None, cmax=None, ax=None, **kwargs):

    if ax is None:
        ax = plt.gca()

    if xbins is None:
        xbins = np.arange(H.shape[1]+1)
    if ybins is None:
        ybins = np.arange(H.shape[0]+1)

    if cmin is not None:
        H[H < cmin] = None
    if cmax is not None:
        H[H > cmax] = None

    X, Y = np.meshgrid(xbins, ybins)

    pc = ax.pcolormesh(X, Y, H, **kwargs)

    ax.set_xlim(xbins[0], xbins[-1])
    ax.set_ylim(ybins[0], ybins[-1])

    ax.set_xticks(xbins)
    ax.set_yticks(ybins)

    if cbar:
        cax = append_axes(ax, size=cbarsize, pad=cbarpad, position=cbarpos)
        plt.colorbar(pc, cax=cax)

    return H, xbins, ybins, pc


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
    figw = float(w)/(r-left)
    figh = float(h)/(t-b)
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

        return new_size/orig_size

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
