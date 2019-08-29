# Log styles
from . import styles_cms as style
from . import plot
__all__ = [style, plot]


def cmslabel(ax, paper=False, supplementary=False, data=False, year=2017,
             lumi=None, llabel=None, rlabel=None, fontname=None,
             fontsize=None):
    from matplotlib import rcParams
    import matplotlib.pyplot as plt
    _font_size = rcParams['font.size'] if fontsize is None else fontsize
    fontname = 'TeX Gyre Heros' if fontname is None else fontname

    # CMS label
    cms = ax.annotate('CMS',
                      xy=(0.001, 1),
                      xycoords='axes fraction',
                      fontsize=_font_size * 1.3,
                      fontname=fontname,
                      ha='left',
                      va='bottom',
                      fontweight='bold',
                      annotation_clip=False)

    # Right label
    if rlabel is not None:
        _lumi = rlabel
    else:
        if lumi is not None:
            _lumi = r'{lumi}, {year} (13 TeV)'.format(lumi=str(lumi) +
                                                      r' $\mathrm{fb^{-1}}$',
                                                      year=str(year))
        else:
            _lumi = '{} (13 TeV)'.format(str(year))

    ax.annotate(_lumi,
                xy=(1, 1.008),
                xycoords='axes fraction',
                fontsize=_font_size * 0.95,
                fontweight='normal',
                fontname=fontname,
                ha='right',
                va='bottom',
                annotation_clip=False)

    # Left label
    if llabel is not None:
        _label = llabel
    else:
        _label = ""
        if not data:
            _label = " ".join(["Simulation", _label])
        if not paper:
            _label = " ".join([_label, "Preliminary"])
        if supplementary:
            _label = " ".join([_label, "Supplementary"])

        _label = " ".join(_label.split())

    ax.annotate(_label,
                xy=(0.001, 1.005),
                xycoords='axes fraction',
                fontsize=_font_size,
                fontname=fontname,
                xytext=(cms.get_window_extent(
                    renderer=plt.gcf().canvas.get_renderer()).width * 1.06, 0),
                textcoords='offset points',
                fontstyle='italic',
                ha='left',
                va='bottom',
                annotation_clip=False)
    return ax


def ticks(ax):
    import matplotlib.ticker as plticker
    xl = ax.get_xlim()
    ax.xaxis.set_major_locator(
        plticker.MultipleLocator(base=(xl[-1] - xl[0]) / 5))
    ax.xaxis.set_minor_locator(
        plticker.MultipleLocator(base=(xl[-1] - xl[0]) / 40))
    yl = ax.get_ylim()
    ax.yaxis.set_major_locator(
        plticker.MultipleLocator(base=(yl[-1] - yl[0]) / 5))
    ax.yaxis.set_minor_locator(
        plticker.MultipleLocator(base=(yl[-1] - yl[0]) / 40))

    return ax

