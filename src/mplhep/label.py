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


def _calculate_dynamic_padding(ax, pad=5, xpad=None, ypad=None):
    """
    Calculate dynamic padding based on axes dimensions.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object
    pad : float, optional
        User-specified padding percentage that overrides dynamic calculation for both dimensions
    xpad : float, optional
        User-specified horizontal padding percentage, overrides pad and dynamic calculation for x-direction
    ypad : float, optional
        User-specified vertical padding percentage, overrides pad and dynamic calculation for y-direction

    Returns
    -------
    tuple[float, float]
        (x_padding, y_padding) in axes fraction units
    """
    # Get axes dimensions to calculate aspect-aware padding
    bbox = ax.get_position()
    fig = ax.figure

    # Handle both Figure and SubFigure cases
    try:
        # Try to get size directly (works for Figure)
        fig_width, fig_height = fig.get_size_inches()
    except AttributeError:
        # For SubFigure, get size from parent figure
        parent_fig = fig.figure if hasattr(fig, "figure") else fig
        fig_width, fig_height = parent_fig.get_size_inches()
        # Scale by the subfigure's relative size if it's a SubFigure
        if hasattr(fig, "get_position"):
            subfig_bbox = fig.get_position()
            fig_width *= subfig_bbox.width
            fig_height *= subfig_bbox.height
    ax_width = bbox.width * fig_width
    ax_height = bbox.height * fig_height

    # Calculate dynamic padding based on the shorter dimension
    shorter_dim = min(ax_width, ax_height)
    longer_dim = max(ax_width, ax_height)
    aspect_ratio = longer_dim / shorter_dim

    # Convert base percentage to proportional values
    base_padding = pad / 100.0

    # Calculate dynamic padding for the longer dimension, scale down to maintain visual consistency
    if ax_width > ax_height:
        # Width is longer, scale x padding down
        dynamic_x_padding = base_padding / aspect_ratio
        dynamic_y_padding = base_padding
    else:
        # Height is longer, scale y padding down
        dynamic_x_padding = base_padding
        dynamic_y_padding = base_padding / aspect_ratio

    # Use user-specified padding if provided, otherwise use dynamic calculation
    x_padding = xpad / 100.0 if xpad is not None else dynamic_x_padding
    y_padding = ypad / 100.0 if ypad is not None else dynamic_y_padding

    return x_padding, y_padding


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
    pad=None,
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

    # Calculate dynamic padding based on axes dimensions
    if pad is None:
        pad = 5 if loc in [1, 2, 3, 4] else 0
    x_padding, y_padding = _calculate_dynamic_padding(ax, pad=pad)

    loc1_dict = {
        0: {"xy": (0, 1), "va": "bottom"},
        1: {"xy": (x_padding, 1 - y_padding), "va": "top"},
    }

    _text_offset = 0.005  # Small offset to align smaller text next to larger text
    loc2_dict = {
        0: {"xy": (0, 1 + y_padding + _text_offset), "va": "bottom"},
        1: {"xy": (x_padding, 1 - y_padding + _text_offset), "va": "bottom"},
        2: {"xy": (x_padding, 1 - y_padding), "va": "top"},
        3: {"xy": (x_padding, 1 - y_padding), "va": "top"},
        4: {"xy": (x_padding, 1 - y_padding + _text_offset), "va": "bottom"},
    }

    _ax_offset = 0.01
    loc3_dict = {
        0: {
            "xy": (1.0 + x_padding + _ax_offset, 1 + y_padding),
            "va": "top",
            "ha": "left",
        },
        1: {"xy": (x_padding, 1 - y_padding), "va": "top"},
        2: {"xy": (x_padding, 1 - y_padding), "va": "top"},
        3: {"xy": (x_padding, 1 - y_padding), "va": "top"},
        4: {"xy": (x_padding, 1 - y_padding), "va": "top"},
    }

    if loc not in [0, 1, 2, 3, 4]:
        msg = (
            "loc must be in {0, 1, 2, 3, 4}:\n"
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
def lumitext(
    text: str = "",
    ax: plt.Axes | None = None,
    fontname: str | None = None,
    fontsize: float | None = None,
    pad: float | None = None,
) -> plt.Axes:
    """Add typical LHC experiment top-right label. Usually used to indicate year
    or aggregate luminosity in the plot.

    Parameters
    ----------
        text : str, optional
            Secondary experiment label, typically not-bold and smaller
            font-size. For example "Simulation" or "Preliminary"
        ax : matplotlib.axes.Axes, optional
            Axes object (if None, last one is fetched)
        fontname : str, optional
            Name of font to be used.
        fontsize : int or float, optional
            Defines size of "secondary label". Experiment label is 1.3x larger.
        pad : float, optional
            Padding value to override dynamic calculation, by default 0.0

    Returns
    -------
        ax : matplotlib.axes.Axes
            A matplotlib `Axes <https://matplotlib.org/3.1.1/api/axes_api.html>`_ object
    """

    _font_size = rcParams["font.size"] if fontsize is None else fontsize
    _font_family = rcParams.get("font.family", "sans-serif")
    _font_family = _font_family[0] if isinstance(_font_family, list) else _font_family
    _font = rcParams.get(f"font.{_font_family}", "DejaVu Sans")
    _font = _font[0] if isinstance(_font, list) else _font
    fontname = _font if fontname is None else fontname

    if ax is None:
        ax = plt.gca()

    # Calculate dynamic padding for consistent positioning
    _pad = 0 if pad is None else pad
    _, y_padding = _calculate_dynamic_padding(ax, pad=_pad)

    ax.text(
        x=1,
        y=1 + y_padding,
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
    pad=None,
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
            _lumi = r"{com}, {lumi}".format(
                com=r"$\sqrt{s} = \mathrm{" + str(com) + r"\ TeV}$"
                if com is not None
                else r"$\sqrt{s} = \mathrm{13\ TeV}$",
                lumi=lumi_format.format(lumi) + r" $\mathrm{fb^{-1}}$",
            )
        else:
            _lumi = r"{com}".format(
                com=r"$\sqrt{s} = \mathrm{" + str(com) + r"\ TeV}$"
                if com is not None
                else r"$\sqrt{s} = \mathrm{13\ TeV}$",
            )

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


def _parse_loc_to_xy(loc):
    """
    Parse location string to x, y coordinates.

    Parameters
    ----------
    loc : str
        Location specification

    Returns
    -------
    tuple[str, str]
        (x, y) position strings
    """
    # Normalize string
    if isinstance(loc, str):
        loc = loc.replace("-", " ").lower().strip()

    # Map location strings to (x, y) coordinates
    loc_map = {
        # Inside positions
        "upper left": ("left_in", "top_in"),
        "upper right": ("right_in", "top_in"),
        "lower left": ("left_in", "bottom_in"),
        "lower right": ("right_in", "bottom_in"),
        # Outside positions (over frame)
        "over left": ("left", "top_out"),
        "over right": ("right", "top_out"),
        "under left": ("left", "bottom_out"),
        "under right": ("right", "bottom_out"),
        # Alternative spellings
        "top left": ("left_in", "top_in"),
        "top right": ("right_in", "top_in"),
        "bottom left": ("left_in", "bottom_in"),
        "bottom right": ("right_in", "bottom_in"),
    }

    if loc in loc_map:
        return loc_map[loc]
    error_msg = f"Invalid location: {loc!r}. Valid options are: {list(loc_map.keys())}"
    raise ValueError(error_msg)


def add_text(
    text: str,
    loc: str | None = "upper left",
    x: float | str | None = None,
    y: float | str | None = None,
    pad: float | None = None,
    xpad: float | None = None,
    ypad: float | None = None,
    fontsize: int | None = None,
    white_background: bool = False,
    ax: plt.Axes | None = None,
    **kwargs,
) -> mtext.Text:
    """
    Add text to an axis.

    Parameters
    ----------
    text : str
        The text to add.
    loc : str | None, optional
        Location shortcut similar to plt.legend(). Can be:
        - "upper left", "upper right", "lower left", "lower right" (inside axes)
        - "over left", "over right", "under left", "under right" (outside axes)
        - Alternative: "top left", "top right", "bottom left", "bottom right"
        If provided, overrides x and y parameters.
    x : float | str | None, optional
        Horizontal position of the text in unit of the normalized x-axis length.
        Aliases: "left", "right", "left_in", "right_in", "right_out".
        Ignored if loc is provided.
    y : float | str | None, optional
        Vertical position of the text in unit of the normalized y-axis length.
        Aliases: "top", "bottom", "top_in", "bottom_in", "top_out", "bottom_out".
        Ignored if loc is provided.
    pad : float, optional
        Padding percentage from edges for "in" positions, by default 5.0. This is applied to the shorter dimension and scaled proportionally for the longer dimension.
    xpad : float | None, optional
        Horizontal padding percentage, overrides pad value for x-direction if provided.
    ypad : float | None, optional
        Vertical padding percentage, overrides pad value for y-direction if provided.
    fontsize : int, optional
        Font size, by default None (uses rcParams default).
    white_background : bool, optional
        Draw a white rectangle under the text, by default False.
    ax : matplotlib.axes.Axes, optional
        Figure axis, by default None.
    kwargs : dict
        Keyword arguments to be passed to the ax.text() function.
        In particular, the keyword arguments ha and va, which are set by default to accommodate to the x and y aliases, can be used to change the text alignment.

    Raises
    ------
    ValueError
        If the x or y position is not a float or a valid position.

    Returns
    -------
    matplotlib.text.Text
        The text object that was added to the axes.
    """

    # Handle loc parameter first
    if loc is not None and (x is not None or y is not None):
        error_msg = "Cannot specify both `loc` and `x`/`y` parameters."
        raise ValueError(error_msg)
    if loc is not None:
        x, y = _parse_loc_to_xy(loc)

    # Normalize string arguments
    if isinstance(x, str):
        x = x.replace("-", "_").lower()
    if isinstance(y, str):
        y = y.replace("-", "_").lower()

    # Set default padding if not provided
    if pad is None and "out" not in (str(x) + str(y)):
        pad = 5.0
    elif pad is None:
        pad = 1.0

    _font_size = rcParams["font.size"] if fontsize is None else fontsize

    # Set default horizontal alignment based on x position
    default_ha = "right" if x in ["right", "right_in"] else "left"

    # Set default vertical alignment based on y position
    default_va = "top" if y in ["top_in", "bottom", "bottom_out"] else "bottom"

    kwargs.setdefault("ha", default_ha)
    kwargs.setdefault("va", default_va)

    if ax is None:
        ax = plt.gca()
    transform = ax.transAxes

    # Calculate dynamic padding based on axes dimensions
    x_padding, y_padding = _calculate_dynamic_padding(ax, pad=pad, xpad=xpad, ypad=ypad)

    x_values = {
        "left": 0.0,
        "right": 1.0,
        "left_in": x_padding,
        "right_in": 1.0 - x_padding,
        "right_out": 1.0 + x_padding,
    }

    y_values = {
        "top": 1.0 + y_padding,
        "bottom": -0.1 - y_padding,
        "top_out": 1.0 + y_padding,
        "bottom_out": -0.1 - y_padding,
        "top_in": 1.0 - y_padding,
        "bottom_in": y_padding,
    }

    if isinstance(x, str):
        if x not in x_values:
            msg = f"{x!r} is not a valid x position."
            raise ValueError(msg)
        x = x_values[x]

    if isinstance(y, str):
        if y not in y_values:
            msg = f"{y!r} is not a valid y position."
            raise ValueError(msg)
        y = y_values[y]

    # At this point, x and y should be float values
    assert isinstance(x, (int, float)), f"x should be numeric, got {type(x)}"
    assert isinstance(y, (int, float)), f"y should be numeric, got {type(y)}"

    t = ax.text(
        float(x),
        float(y),
        text,
        fontsize=_font_size,
        transform=transform,
        **kwargs,
    )

    # Add background
    if white_background:
        t.set_bbox({"facecolor": "white", "edgecolor": "white"})

    return t


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

    from mplhep.label import ExpSuffix, ExpText  # noqa: PLC0415

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
