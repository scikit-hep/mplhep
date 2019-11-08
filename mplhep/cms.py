from matplotlib import rcParams
import matplotlib.pyplot as plt

# Log styles
from . import styles_cms as style
from . import plot
__all__ = [style, plot]


# CMS label
def cmstext(text="",
            loc=0,
            ax=None,
            fontname=None,
            fontsize=None):

    _font_size = rcParams['font.size'] if fontsize is None else fontsize
    fontname = 'TeX Gyre Heros' if fontname is None else fontname

    if ax is None:
        ax = plt.gca()

    loc1_dict = {
        0: {'xy': (0.001, 1),
            'va': 'bottom',
            },
        1: {'xy': (0.05, 0.95),
            'va': 'top',
            },
    }

    loc2_dict = {
        0: {'xy': (0.001, 1.005),
            'va': 'bottom',
            },
        1: {'xy': (0.05, 0.9550),
            'va': 'bottom',
            },
        2: {'xy': (0.05, 0.9450),
            'va': 'top',
            },
        3: {'xy': (0.05, 0.95),
            'va': 'top',
            },
    }

    if loc not in [0, 1, 2, 3]:
        raise ValueError("loc must be in {0, 1, 2}:\n"
                         "0 : Above axes, left aligned\n"
                         "1 : Top left corner\n"
                         "2 : Top left corner, multiline\n"
                         "3 : Split CMS above axes, rest of label in"
                         "top left corner")

    if loc in [0, 3]:
        _cms_loc = 0
    else:
        _cms_loc = 1
    cms = ax.text(*loc1_dict[_cms_loc]['xy'], s="CMS",
                  transform=ax.transAxes,
                  ha='left',
                  va=loc1_dict[_cms_loc]['va'],
                  fontsize=_font_size * 1.3,
                  fontweight='bold',
                  fontname=fontname
                  )

    from matplotlib import transforms
    cms.draw(ax.figure.canvas.get_renderer())

    if loc == 0:
        _t = transforms.offset_copy(cms._transform,
                                    x=cms.get_window_extent().width * 1.08,
                                    units='dots')
    elif loc == 1:
        _t = transforms.offset_copy(cms._transform,
                                    x=cms.get_window_extent().width * 1.08,
                                    y=-cms.get_window_extent().height,
                                    units='dots')
    elif loc == 2:
        _t = transforms.offset_copy(cms._transform,
                                    y=-cms.get_window_extent().height,
                                    units='dots')
    elif loc == 3:
        _t = transforms.offset_copy(cms._transform, units='dots')

    ax.annotate(text,
                xy=loc2_dict[loc]['xy'],
                xycoords=_t,
                ha='left',
                va=loc2_dict[loc]['va'],
                fontsize=_font_size,
                fontname=fontname,
                fontstyle='italic',
                annotation_clip=False)

    return ax


# Lumi text
def lumitext(text="",
             ax=None,
             fontname=None,
             fontsize=None):

    _font_size = rcParams['font.size'] if fontsize is None else fontsize
    fontname = 'TeX Gyre Heros' if fontname is None else fontname

    if ax is None:
        ax = plt.gca()

    ax.text(x=1, y=1.005, s=text,
            transform=ax.transAxes,
            ha='right',
            va='bottom',
            fontsize=_font_size * 0.95,
            fontweight='normal',
            fontname=fontname,
            )


# Wrapper
def cmslabel(ax, loc=0, data=False, paper=False, supplementary=False,
             year=2017, lumi=None, llabel=None, rlabel=None, fontname=None,
             fontsize=None):

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

    lumitext(text=_lumi,
             ax=ax,
             fontname=fontname,
             fontsize=fontsize)

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

    cmstext(text=_label,
            loc=loc,
            ax=ax,
            fontname=fontname,
            fontsize=fontsize)

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
