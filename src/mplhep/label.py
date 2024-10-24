from __future__ import annotations

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
from matplotlib import rcParams


class ExpText(mtext.Text):
    def __repr__(self):
        return f"exptext: Custom Text({self._x}, {self._y}, {self._text!r})"


class ExpSuffix(mtext.Text):
    def __repr__(self):
        return f"expsuffix: Custom Text({self._x}, {self._y}, {self._text!r})"


class SuppText(mtext.Text):
    def __repr__(self):
        return f"supptext: Custom Text({self._x}, {self._y}, {self._text!r})"


def exp_text(
    exp="",
    text="",
    supp="",
    loc=0,
    *,
    ax=None,
    fontname=None,
    fontsize=None,
    exp_weight="bold",
    italic=(False, False, False),
    pad=0,
):
    """Add typical LHC experiment primary label to the axes.

    Parameters
    ----------
        text : string, optional
            Secondary experiment label, typically not-bold and smaller
            font-size. For example "Simulation" or "Preliminary"
        loc : int, optional
            Label position:
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
        italic : (bool, bool, bool), optional
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

    loc3_dict = {
        0: {"xy": (1.012, 1 + pad), "va": "top", "ha": "left"},
        1: {"xy": (0.05, 0.945 - pad), "va": "top"},
        2: {"xy": (0.05, 0.935 - pad), "va": "top"},
        3: {"xy": (0.05, 0.940 - pad), "va": "top"},
        4: {"xy": (0.05, 0.9450 - pad), "va": "top"},
    }

    if loc not in [0, 1, 2, 3, 4]:
        msg = (
            "loc must be in {0, 1, 2}:\n"
            "0 : Above axes, left aligned\n"
            "1 : Top left corner\n"
            "2 : Top left corner, multiline\n"
            "3 : Split EXP above axes, rest of label in top left corner\n"
        )
        raise ValueError(msg)

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

    _exp_loc = 0 if loc in [0, 3] else 1
    _formater = ax.get_yaxis().get_major_formatter()
    if isinstance(_formater, mpl.ticker.ScalarFormatter) and _exp_loc == 0:
        _sci_box = pixel_to_axis(
            ax.get_yaxis().offsetText.get_window_extent(ax.figure.canvas.get_renderer())
        )
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

    _dpi = ax.figure.dpi
    _exp_xoffset = (
        exptext.get_window_extent(ax.figure.canvas.get_renderer()).width / _dpi * 1.05
    )
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
        fontsize=_font_size * 1.2 if exp == "ATLAS" else _font_size,
        fontname=fontname,
        fontstyle="italic" if italic[1] else "normal",
    )
    ax._add_text(expsuffix)

    if loc == 0:
        # No transformation, fixed location
        _t = mtransforms.offset_copy(exptext._transform, units="inches", fig=ax.figure)
    elif loc == 1:
        _t = mtransforms.offset_copy(
            exptext._transform,
            y=-exptext.get_window_extent().height / _dpi,
            units="inches",
            fig=ax.figure,
        )
    elif loc in (2, 3):
        _t = mtransforms.offset_copy(
            expsuffix._transform,
            y=-expsuffix.get_window_extent().height / _dpi,
            units="inches",
            fig=ax.figure,
        )
    elif loc == 4:
        _t = mtransforms.offset_copy(
            exptext._transform,
            y=-exptext.get_window_extent().height / _dpi,
            units="inches",
            fig=ax.figure,
        )

    supptext = SuppText(
        *loc3_dict[loc]["xy"],
        text=supp,
        transform=_t,
        ha=loc3_dict[loc].get("ha", "left"),
        va=loc3_dict[loc]["va"],
        fontsize=_font_size / 1.3,
        fontname=fontname,
        rotation=0 if loc != 0 else 90,
        fontstyle="italic" if italic[2] else "normal",
    )
    ax._add_text(supptext)

    return exptext, expsuffix, supptext


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
    pub="",
    year=None,
    lumi=None,
    lumi_format="{0}",
    com=None,
    llabel=None,
    rlabel=None,
    fontname=None,
    fontsize=None,
    exp_weight="bold",
    pad=0,
    italic=(False, False, False),
    ax=None,
):
    """A convenience wrapper combining ``<exp>.text`` and ``lumitext`` providing for
    the most common use cases.

    Parameters
    ----------
        loc : int, optional
            Label position of ``exp_text`` label:
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
        lumi_format : string, optional, default is `"{0}"`
            Format string for luminosity number, e.g. `"{0:.1f}"`
        com: float, optional, default is 13, but can be changed to 7/8/13.6/14 to fit different requirements
        llabel : string, optional
            String to manually set left-hand label text. Will overwrite "data" and
            "label" kwargs.
        rlabel : string, optional
            String to manually set right-hand label text.
        fontname : string, optional
            Name of font to be used.
        fontsize : string, optional
            Defines size of the experiment label and the secondary label.
        exp_weight : string, optional
            Set fontweight of <exp> label. Default "bold".
        italic : (bool, bool, bool), optional
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
    elif lumi is not None:
        _lumi = r"{lumi}{year} ({com} TeV)".format(
            lumi=lumi_format.format(lumi) + r" $\mathrm{fb^{-1}}$",
            year=", " + str(year) if year is not None else "",
            com=str(com) if com is not None else "13",
        )
    else:
        _lumi = "{year} ({com} TeV)".format(
            year=str(year) if year is not None else "",
            com=str(com) if com is not None else "13",
        )

    if loc < 4:
        lumitext(text=_lumi, ax=ax, fontname=fontname, fontsize=fontsize)

    # Left label
    if llabel is not None:
        _label = llabel
    else:
        _label = label
        if pub:
            _label = " ".join(["Supplementary", _label])
        if not data:
            _label = " ".join(["Simulation", _label])
        _label = " ".join(_label.split())

    exptext, expsuffix, supptext = exp_text(
        exp=exp,
        text=_label,
        supp=pub if loc != 4 else "",  # Special handling for loc4
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
            supptext._transform,
            y=-supptext.get_window_extent().height / ax.figure.dpi,
            units="inches",
            fig=ax.figure,
        )

        if com is not None:
            _com_label = r"\mathrm{" + str(com) + r"\ TeV}"
        else:
            _com_label = r"\mathrm{13\ TeV}"

        if lumi is not None:
            _lumi = (
                r"$\sqrt{s} = " + _com_label + ", " + str(lumi) + r"\ \mathrm{fb}^{-1}$"
            )
        else:
            _lumi = r"$\sqrt{s} = " + _com_label + "$"
        explumi = ExpSuffix(
            *exptext.get_position(),
            text=rlabel if rlabel is not None else _lumi,
            transform=_t,
            ha=supptext.get_ha(),
            va="top",
            fontsize=fontsize,
            fontname=fontname,
            fontstyle="normal",
        )
        ax._add_text(explumi)

        _t = mtransforms.offset_copy(
            explumi._transform,
            y=-explumi.get_window_extent().height / ax.figure.dpi,
            units="inches",
            fig=ax.figure,
        )
        _font_size = rcParams["font.size"] if fontsize is None else fontsize
        supptext = SuppText(
            *explumi.get_position(),
            text=pub,
            transform=_t,
            ha=explumi.get_ha(),
            va="top",
            fontsize=_font_size / 1.3,
            fontname=fontname,
            fontstyle="italic" if italic[2] else "normal",
        )
        ax._add_text(supptext)
        return exptext, expsuffix, supptext, explumi

    return exptext, expsuffix, supptext


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
    labels : list of tuples, optional
        Mapping of label versions to be produced along with desired savename
        modifications. By default:
        [
            ("", ""),
            ("Preliminary", "pas"),
            ("Supplementary", "supp"),
            ("Work in Progress", "wip"),
        ]
        If supplied strings contain suffixes such as ".png" the names will be assumed
        to be absolute and will ignore ``fname``.
        If current label contains "Simulation" this will be preserved.
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

    label_base = next(ch for ch in ax.get_children() if isinstance(ch, ExpSuffix))
    _sim = "Simulation" if "Simulation" in label_base.get_text() else ""

    for label_text, suffix in labels:
        label_base.set_text(" ".join([_sim, label_text]).lstrip())

        if "." in suffix:  # absolute paths
            save_name = suffix
        else:
            if len(suffix) > 0:
                suffix = "_" + suffix  # noqa: PLW2901
            if "." in fname:
                save_name = f"{fname.split('.')[0]}{suffix}.{fname.split('.')[1]}"
            else:
                save_name = f"{fname}{suffix}"

        path_dir = os.path.join(*save_name.split("/")[:-1])
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        if isinstance(ax.figure, plt.Figure):
            ax.figure.savefig(save_name, **kwargs)


def save_variations(fig, name, text_list=None, exp=None):
    """Lite ``savelabels``

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
