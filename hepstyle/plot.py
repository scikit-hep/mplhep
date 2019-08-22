import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size


def rescale_to_axessize(ax, w, h):
    """ Adjust figure size to axes size in inches
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
    fig = ax.figure
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height

    divider = make_axes_locatable(ax)
    margin_size = axes_size.Fixed(size)
    pad_size = axes_size.Fixed(pad)
    xsizes = [pad_size, margin_size]
    yhax = divider.append_axes(position, size=margin_size, pad=pad_size)

    if position in ["right"]:
        divider.set_horizontal([axes_size.Fixed(width)] + xsizes)
        if extend:
            fig.set_size_inches(fig.get_size_inches()[0] + (size + pad) * 2,
                                fig.get_size_inches()[1])
    elif position in ["left"]:
        divider.set_horizontal(xsizes + [axes_size.Fixed(width)])
        if extend:
            fig.set_size_inches(fig.get_size_inches()[0] + (size + pad) * 2,
                                fig.get_size_inches()[1])
    elif position in ['top']:
        divider.set_vertical([axes_size.Fixed(height)] + xsizes)
        if extend:
            fig.set_size_inches(fig.get_size_inches()[0],
                                fig.get_size_inches()[1] + (size + pad) * 2)
    elif position in ['bottom']:
        divider.set_vertical(xsizes + [axes_size.Fixed(height)])
        if extend:
            fig.set_size_inches(fig.get_size_inches()[0],
                                fig.get_size_inches()[1] + (size + pad) * 2)

    return yhax
