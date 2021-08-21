from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
from matplotlib import rcParams


class ExpText(mtext.Text):
    def __repr__(self):
        return "exptext: Custom Text({}, {}, {})".format(
            self._x, self._y, repr(self._text)
        )


class ExpSuffix(mtext.Text):
    def __repr__(self):
        return "expsuffix: Custom Text({}, {}, {})".format(
            self._x,
            self._y,
            repr(self._text),
        )


def exp_text(
    exp="",
    text="",
    loc=0,
    *,
    ax=None,
    fontname=None,
    fontsize=None,
    exp_weight="bold",
    italic=(False, False),
    pad=0,
):
    """Add typical LHC experiment primary label to the axes.
    Parameters
    ----------
        text : string, optional
            Secondary experiment label, typically not-bold and smaller
            font-size. For example "Simulation" or "Preliminary"
        loc : int, optional
            Label positon:
            - 0 : Above axes, left aligned
            - 1 : Top left corner
            - 2 : Top left corner, multiline
            - 3 : Split EXP above axes, rest of label in top left corner"
        ax : matplotlib.axes.Axes, optional
            Axes object (if None, last one is fetched)
        fontname : string, optional
            Name of font to be used.
        fontsize : string, optional
            Defines size of "secondary label". Experiment label is 1.3x larger.
        exp_weight : string, optional
            Set fontweight of <exp> label. Default "bold".
        italic : (bool, bool), optional
            Tuple of bools to switch which label is italicized
        pad : float, optional
            Additional padding from axes border in units of axes fraction size.
    Returns
    -------
        ax : matplotlib.axes.Axes
            A matplotlib `Axes <https://matplotlib.org/3.1.1/api/axes_api.html>`
            object
    """

    _font_size = rcParams["font.size"] if fontsize is None else fontsize
    fontname = "TeX Gyre Heros" if fontname is None else fontname

    if ax is None:
        ax = plt.gca()

    loc1_dict = {
        0: {"xy": (0.001, 1 + pad), "va": "bottom"},
        1: {"xy": (0.05, 0.95 - pad), "va": "top"},
    }

    loc2_dict = {
        0: {"xy": (0.001, 1.005 + pad), "va": "bottom"},
        1: {"xy": (0.05, 0.9550 - pad), "va": "bottom"},
        2: {"xy": (0.05, 0.9450 - pad), "va": "top"},
        3: {"xy": (0.05, 0.95 - pad), "va": "top"},
        4: {"xy": (0.05, 0.9550 - pad), "va": "bottom"},
    }

    if loc not in [0, 1, 2, 3, 4]:
        raise ValueError(
            "loc must be in {0, 1, 2}:\n"
            "0 : Above axes, left aligned\n"
            "1 : Top left corner\n"
            "2 : Top left corner, multiline\n"
            "3 : Split EXP above axes, rest of label in top left corner\n"
        )

    def pixel_to_axis(extent, ax=None):
        # Transform pixel bbox extends to axis fractions
        if ax is None:
            ax = plt.gca()

        extent = extent.transformed(ax.transData.inverted())

        def dist(tup):
            return abs(tup[1] - tup[0])

        dimx, dimy = dist(ax.get_xlim()), dist(ax.get_ylim())
        x, y = ax.get_xlim()[0], ax.get_ylim()[0]
        x0, y0, x1, y1 = extent.extents

        return extent.from_extents(
            abs(x0 - x) / dimx,
            abs(y0 - y) / dimy,
            abs(x1 - x) / dimx,
            abs(y1 - y) / dimy,
        )

    if loc in [0, 3]:
        _exp_loc = 0
    else:
        _exp_loc = 1
    _formater = ax.get_yaxis().get_major_formatter()
    if type(mpl.ticker.ScalarFormatter()) == type(_formater) and _exp_loc == 0:
        ax.figure.canvas.draw()
        _sci_box = pixel_to_axis(ax.get_yaxis().offsetText.get_window_extent())
        _sci_offset = _sci_box.width * 1.1
        loc1_dict[_exp_loc]["xy"] = (_sci_offset, loc1_dict[_exp_loc]["xy"][-1])
        if loc == 0:
            loc2_dict[_exp_loc]["xy"] = (_sci_offset, loc2_dict[_exp_loc]["xy"][-1])

    exptext = ExpText(
        *loc1_dict[_exp_loc]["xy"],
        text=exp,
        transform=ax.transAxes,
        ha="left",
        va=loc1_dict[_exp_loc]["va"],
        fontsize=_font_size * 1.3,
        fontweight=exp_weight,
        fontstyle="italic" if italic[0] else "normal",
        fontname=fontname,
    )
    ax._add_text(exptext)

    ax.figure.canvas.draw()
    _dpi = ax.figure.dpi
    _exp_xoffset = exptext.get_window_extent().width / _dpi * 1.05
    if loc == 0:
        _t = mtransforms.offset_copy(
            exptext._transform, x=_exp_xoffset, units="inches", fig=ax.figure
        )
    elif loc in [1, 4]:
        _t = mtransforms.offset_copy(
            exptext._transform,
            x=_exp_xoffset,
            y=-exptext.get_window_extent().height / _dpi,
            units="inches",
            fig=ax.figure,
        )
    elif loc == 2:
        _t = mtransforms.offset_copy(
            exptext._transform,
            y=-exptext.get_window_extent().height / _dpi,
            units="inches",
            fig=ax.figure,
        )
    elif loc == 3:
        _t = mtransforms.offset_copy(exptext._transform, units="inches", fig=ax.figure)

    expsuffix = ExpSuffix(
        *loc2_dict[loc]["xy"],
        text=text,
        transform=_t,
        ha="left",
        va=loc2_dict[loc]["va"],
        fontsize=_font_size,
        fontname=fontname,
        fontstyle="italic" if italic[1] else "normal",
    )
    ax._add_text(expsuffix)

    return exptext, expsuffix


# Lumi text
def lumitext(text="", ax=None, fontname=None, fontsize=None):
    """Add typical LHC experiment top-right label. Usually used to indicate year
    or aggregate luminosity in the plot.
    Parameters
    ----------
        text : string, optional
            Secondary experiment label, typically not-bold and smaller
            font-size. For example "Simulation" or "Preliminary"
        ax : matplotlib.axes.Axes, optional
            Axes object (if None, last one is fetched)
        fontname : string, optional
            Name of font to be used.
        fontsize : string, optional
            Defines size of "secondary label". Experiment label is 1.3x larger.
    Returns
    -------
        ax : matplotlib.axes.Axes
            A matplotlib `Axes <https://matplotlib.org/3.1.1/api/axes_api.html>`_ object
    """

    _font_size = rcParams["font.size"] if fontsize is None else fontsize
    fontname = "TeX Gyre Heros" if fontname is None else fontname

    if ax is None:
        ax = plt.gca()

    ax.text(
        x=1,
        y=1.005,
        s=text,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=_font_size * 0.95,
        fontweight="normal",
        fontname=fontname,
    )

    return ax


# Wrapper
def exp_label(
    exp="",
    loc=0,
    *,
    data=False,
    label="",
    year=None,
    lumi=None,
    llabel=None,
    rlabel=None,
    fontname=None,
    fontsize=None,
    exp_weight="bold",
    pad=0,
    italic=(False, False),
    ax=None,
):
    """A convenience wrapper combining ``<exp>.text`` and ``lumitext`` providing for
    the most common use cases.
    Parameters
    ----------
        loc : int, optional
            Label positon of ``exp_text`` label:
            - 0 : Above axes, left aligned
            - 1 : Top left corner
            - 2 : Top left corner, multiline
            - 3 : Split EXP above axes, rest of label in top left corner"
            - 4 : (1) Top left corner, but align "rlabel" underneath
        ax : matplotlib.axes.Axes, optional
            Axes object (if None, last one is fetched)
        data : bool, optional
            Prevents prepending "Simulation" to experiment label. Default ``False``.
        label : str, optional
            Text to append after <exp> (Simulation) <label>. Typically "Preliminary"
            "Supplementary", "Private Work" or "Work in Progress"
        year : int, optional
            Year when data was collected
        lumi : float, optional
            Aggregate luminosity shown. Should require ``"data"`` to be ``True``.
        llabel : string, optional
            String to manually set left-hand label text. Will overwrite "data" and
            "label" kwargs.
        rlabel : string, optional
            String to manually set right-hand label text.
        fontname : string, optional
            Name of font to be used.
        fontsize : string, optional
            Defines size of "secondary label". Experiment label is 1.3x larger.
        exp_weight : string, optional
            Set fontweight of <exp> label. Default "bold".
        italic : (bool, bool), optional
            Tuple of bools to switch which label is italicized
        pad : float, optional
            Additional padding from axes border in units of axes fraction size.
        exp : string
            Experiment name, unavailable in public ``<experiment>text()``.
    Returns
    -------
        ax : matplotlib.axes.Axes
            A matplotlib `Axes <https://matplotlib.org/3.1.1/api/axes_api.html>`_ object
    """

    if ax is None:
        ax = plt.gca()

    # Right label
    if rlabel is not None:
        _lumi = rlabel
    else:
        if lumi is not None:
            _lumi = r"{lumi}{year} (13 TeV)".format(
                lumi=str(lumi) + r" $\mathrm{fb^{-1}}$",
                year=", " + str(year) if year is not None else "",
            )
        else:
            _lumi = "{} (13 TeV)".format(str(year) if year is not None else "")

    if loc < 4:
        lumitext(text=_lumi, ax=ax, fontname=fontname, fontsize=fontsize)

    # Left label
    if llabel is not None:
        _label = llabel
    else:
        _label = ""
        if not data:
            _label = " ".join(["Simulation", label])
        else:
            _label = label
        _label = " ".join(_label.split())

    exptext, expsuffix = exp_text(
        exp=exp,
        text=_label,
        loc=loc,
        ax=ax,
        fontname=fontname,
        fontsize=fontsize,
        exp_weight=exp_weight,
        italic=italic,
        pad=pad,
    )
    if loc == 4:
        _t = mtransforms.offset_copy(
            exptext._transform,
            y=-exptext.get_window_extent().height / ax.figure.dpi,
            units="inches",
            fig=ax.figure,
        )
        if lumi is not None:
            _lumi = (
                r"$\sqrt{s} = \mathrm{13\ TeV}, " + str(lumi) + r"\ \mathrm{fb}^{-1}$"
            )
        else:
            _lumi = r"$\sqrt{s} = \mathrm{13\ TeV}$"
        explumi = ExpSuffix(
            *exptext.get_position(),
            text=rlabel if rlabel is not None else _lumi,
            transform=_t,
            ha=exptext.get_ha(),
            va="top",
            fontsize=fontsize,
            fontname=fontname,
            fontstyle="normal",
        )
        ax._add_text(explumi)
        return exptext, expsuffix, explumi

    return exptext, expsuffix


def savelabels(
    fname: str = "",
    ax: plt.Axes | None = None,
    labels: list | None = None,
    **kwargs,
):
    """
    Save multiple copies of a figure on which axes is located with the
    most commonly used label combinations (or user supplied).

    Example:
        >>> import mplhep as hep
        >>> hep.cms.label(data=False)
        >>> hep.savelabels('test.png')

        This will produces 4 variation on experiment label:
            - "" -> "test.png"
            - "Preliminary" -> "test_pas.png"
            - "Supplementary" -> "test_supp.png"
            - "Work in Progress" -> "test_wip.png"

        Or the combination of labels and filenames can be set manually

        >>> hep.savelabels('test', labels=[("FOO", "foo.pdf"), ("BAR", "bar")])

        Which will produce:
        - "FOO" -> "foo.pdf"
        - "BAR" -> "test_bar.png"

        Passing a list of labels will generate file suffixes by casting
        to snakecase.

    Parameters
    ----------
    fname : str
        Primary filename to be passed to ``plt.savefig``.
    ax : matplotlib.axes.Axes, optional
            Axes object (if None, last one is fetched)
    labels : list, optional
        Mapping of label versions to be produced along with desired savename
        modifications. By default:
        [
            ("", ""),
            ("Preliminary", "pas"),
            ("Supplementary", "supp"),
            ("Work in Progress", "wip"),
        ]
        If supplied strings contain suffixes such as ".png" the names will be assumed
        to be absolute and will not incorporate ``fname``.
        If current label contains "Simulation" this will be perserved.
    """
    if labels is None:
        labels = [
            ("", ""),
            ("Preliminary", "pas"),
            ("Supplementary", "supp"),
            ("Work in Progress", "wip"),
        ]
    if isinstance(labels, list) and isinstance(labels[0], str):
        labels = [(label, label.replace(" ", "_").lower()) for label in labels]
    if ax is None:
        ax = plt.gca()

    label_base = [ch for ch in ax.get_children() if isinstance(ch, ExpSuffix)][0]
    _sim = "Simulation" if "Simulation" in label_base.get_text() else ""

    for label_text, suffix in labels:
        label_base.set_text(" ".join([_sim, label_text]).lstrip())

        if "." in suffix:
            save_name = suffix
        else:
            if len(suffix) > 0:
                suffix = "_" + suffix
            if "." in fname:
                save_name = f"{fname.split('.')[0]}{suffix}.{fname.split('.')[1]}"
            else:
                save_name = f"{fname}{suffix}"

        ax.figure.savefig(save_name, **kwargs)
