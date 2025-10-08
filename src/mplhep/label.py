from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as mtext
from matplotlib import rcParams

from ._deprecate import deprecate_parameter

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


class ExpLabel(mtext.Text):
    def __repr__(self):
        return f"Experiment Label: Text({self._x}, {self._y}, {self._text!r})"


class ExpText(mtext.Text):
    def __repr__(self):
        return f"Experiment Text: Text({self._x}, {self._y}, {self._text!r})"


class LumiText(mtext.Text):
    def __repr__(self):
        return f"Luminosity Text: Text({self._x}, {self._y}, {self._text!r})"


class SuppText(mtext.Text):
    def __repr__(self):
        return f"Supplementary Text: Text({self._x}, {self._y}, {self._text!r})"


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


def _pixel_to_axis(extent: Any, ax: Axes | None = None) -> Any:
    """Transform pixel bbox extents to axis fractions."""
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


def _lumi_line(
    *,
    year: str | float | None = None,
    lumi: str | float | None = None,
    lumi_format: str = "{0}",
    lumi_unit: str = "fb^{-1}",
    com: str | float | None = None,
) -> str:
    """Format luminosity line for standard layout."""
    # Set default values
    com_str = str(com) if com is not None else "13"
    year_str = f", {year}" if year is not None else ""

    if lumi is not None:
        # Format luminosity with unit
        lumi_str = lumi_format.format(lumi)
        lumi_with_unit = f"{lumi_str} $\\mathrm{{{lumi_unit}}}$"
        _lumi = f"{lumi_with_unit}{year_str} ({com_str} TeV)"
    else:
        _lumi = f"$\\ ${year_str} ({com_str} TeV)"

    return _lumi.rstrip()


def _lumi_line_atlas(
    *,
    year: str | float | None = None,  # noqa: ARG001
    lumi: str | float | None = None,
    lumi_format: str = "{0}",
    lumi_unit: str = "fb^{-1}",
    com: str | float | None = None,
) -> str:
    """Format luminosity line for ATLAS-style layout."""
    # Format center-of-mass energy
    if com is not None:
        com_str = f"$\\sqrt{{s}} = \\mathrm{{{com}\\ TeV}}$"
    else:
        com_str = "$\\sqrt{s} = \\mathrm{13\\ TeV}$"

    if lumi is not None:
        # Format luminosity with unit
        lumi_str = lumi_format.format(lumi)
        lumi_with_unit = f"{lumi_str} $\\mathrm{{{lumi_unit}}}$"
        _lumi = f"{com_str}, {lumi_with_unit}"
    else:
        _lumi = com_str

    return _lumi.rstrip()


def _fontsize_to_points(fontsize: str | float) -> float:
    """Convert fontsize (string or number) to numeric points."""
    if isinstance(fontsize, str):
        return mpl.font_manager.FontProperties(size=fontsize).get_size_in_points()
    return float(fontsize)


def _fontsize_axis(ax: Axes, fontsize: str | float) -> float:
    """Convert fontsize to axis fraction units."""
    fontsize_points = _fontsize_to_points(fontsize)
    return (
        fontsize_points
        / (ax.get_position().height * ax.figure.get_size_inches()[1])  # type: ignore[union-attr]
        / ax.figure.dpi
    )


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
    loc: str | None = None,
    x: float | str | None = None,
    y: float | str | None = None,
    pad: float | None = None,
    xpad: float | None = None,
    ypad: float | None = None,
    fontsize: float | None = None,
    white_background: bool = False,
    text_class: type[mtext.Text] = mtext.Text,
    ax: Axes | None = None,
    **kwargs: Any,
) -> mtext.Text:
    """
    Add text to an axis with flexible positioning options.

    Parameters
    ----------
    text : str
        The text to add to the axes.
    loc : str | None, optional
        Location shortcut similar to plt.legend(). Can be:

        - Inside axes: "upper left", "upper right", "lower left", "lower right"
        - Outside axes: "over left", "over right", "under left", "under right"
        - Alternative spellings: "top left", "top right", "bottom left", "bottom right"

        If provided, overrides x and y parameters.
    x : float | str | None, optional
        Horizontal position of the text in normalized axes coordinates (0-1).
        String aliases: "left", "right", "left_in", "right_in", "right_out".
        Ignored if loc is provided.
    y : float | str | None, optional
        Vertical position of the text in normalized axes coordinates (0-1).
        String aliases: "top", "bottom", "top_in", "bottom_in", "top_out", "bottom_out".
        Ignored if loc is provided.
    pad : float | None, optional
        Padding percentage from edges for "in" positions, by default 5.0.
        Applied to the shorter dimension and scaled proportionally for the longer dimension.
    xpad : float | None, optional
        Horizontal padding percentage, overrides pad value for x-direction if provided.
    ypad : float | None, optional
        Vertical padding percentage, overrides pad value for y-direction if provided.
    fontsize : int | float | None, optional
        Font size, by default None (uses rcParams default).
    white_background : bool, optional
        Draw a white rectangle under the text, by default False.
    text_class : type[mtext.Text], optional
        Text class to use for creating the text object, by default mtext.Text.
    ax : matplotlib.axes.Axes | None, optional
        Axes object to add text to. If None, uses current axes.
    **kwargs : Any
        Additional keyword arguments passed to the text constructor.
        Notably 'ha' (horizontal alignment) and 'va' (vertical alignment)
        are set automatically based on position but can be overridden.

    Raises
    ------
    ValueError
        If both loc and x/y parameters are specified, or if x/y positions
        are not valid floats or recognized string aliases.

    Returns
    -------
    matplotlib.text.Text
        The text object that was added to the axes.
    """

    # Handle loc parameter first
    if loc is not None and (x is not None or y is not None):
        error_msg = "Cannot specify both `loc` and `x`/`y` parameters."
        raise ValueError(error_msg)
    if loc is None and x is None and y is None:
        loc = "upper left"
    if loc is not None:
        x, y = _parse_loc_to_xy(loc)

    # Normalize string arguments
    if isinstance(x, str):
        x = x.replace("-", "_").lower()
    if isinstance(y, str):
        y = y.replace("-", "_").lower()

    # Set default padding if not provided
    if (pad is None or pad == 0) and "out" not in (str(x) + str(y)):
        pad = 5.0
    elif pad is None:
        pad = 0

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
        "left": x_padding,
        "right": 1.0 - x_padding,
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
    if x is None and y is not None:
        msg = "Please specify x position if y is given."
        raise ValueError(msg)
    if y is None and x is not None:
        msg = "Please specify y position if x is given."
        raise ValueError(msg)

    assert isinstance(x, (int, float)), f"x should be numeric, got {type(x)}"
    assert isinstance(y, (int, float)), f"y should be numeric, got {type(y)}"

    t = text_class(
        float(x), float(y), text, fontsize=_font_size, transform=transform, **kwargs
    )
    ax._add_text(t)  # type: ignore[attr-defined]

    if white_background:
        t.set_bbox({"facecolor": "white", "edgecolor": "white"})

    return t


def append_text(
    s: str,
    txt_obj: mtext.Text,
    loc: str = "right",
    pad: str | float = "auto",
    ax: Axes | None = None,
    text_class: type[mtext.Text] = mtext.Text,
    **kwargs: Any,
) -> mtext.Text:
    """
    Append text relative to an existing text object.

    Parameters
    ----------
    s : str
        The text string to append.
    txt_obj : matplotlib.text.Text
        The existing text object to append to.
    loc : str, default "right"
        Location relative to the existing text. Options are "right", "below", "above", or "left".
    pad : str | float, default "auto"
        Padding between texts. If "auto", uses automatic spacing.
        If float, specifies padding as percentage of axes size.
    ax : matplotlib.axes.Axes | None, optional
        Axes object. If None, uses current axes.
    text_class : type[mtext.Text], optional
        Text class to use for creating the new text object.
    **kwargs : Any
        Additional keyword arguments passed to the text constructor.

    Returns
    -------
    matplotlib.text.Text
        The appended text object.

    """
    ax = ax if ax is not None else plt.gca()
    fontsize = _fontsize_to_points(kwargs.get("fontsize", rcParams["font.size"]))

    ax_width = ax.get_position().width * ax.figure.get_size_inches()[0]  # type: ignore[union-attr]
    ax_height = ax.get_position().height * ax.figure.get_size_inches()[1]  # type: ignore[union-attr]
    bbox, _, descent = txt_obj._get_layout(ax.figure.canvas.get_renderer())  # type: ignore[attr-defined,union-attr]
    width, height = bbox.width, bbox.height
    dpi = ax.figure.dpi
    text_height = height / ax_height / dpi
    text_height_corr = fontsize / 20 / ax_height / dpi
    text_width = width / ax_width / dpi
    text_width_corr = fontsize / 3 / ax_width / dpi
    yoffset = descent / ax_height / dpi

    # Account for horizontal alignment of the reference text
    ref_ha = txt_obj.get_horizontalalignment()
    ref_x = txt_obj.get_position()[0]
    if ref_ha == "center":
        ref_left = ref_x - text_width / 2
        ref_right = ref_x + text_width / 2
    elif ref_ha == "right":
        ref_left = ref_x - text_width
        ref_right = ref_x
    else:  # "left" or default
        ref_left = ref_x
        ref_right = ref_x + text_width

    if loc == "right":
        pad_offset = 0.0 if pad == "auto" else float(pad) / 100
        _x = ref_right + (text_width_corr if pad == "auto" else pad_offset)
        va = txt_obj.get_verticalalignment()
        if va == "bottom":
            _y = txt_obj.get_position()[1] + yoffset + text_height_corr
        elif va == "top":
            _y = txt_obj.get_position()[1] + yoffset - text_height
        elif va == "baseline":
            _y = txt_obj.get_position()[1] + text_height_corr
        else:
            msg = f"Text option `verticalalignment={va}` not recognized."
            raise ValueError(msg)
        va = "baseline"
        ha = "left"
    elif loc == "below":
        _x = ref_left
        pad_offset = 0.0 if pad == "auto" else float(pad) / 100
        va = txt_obj.get_verticalalignment()
        ref_y = txt_obj.get_position()[1]

        # Calculate the actual bottom edge of the reference text
        if va == "bottom":
            # For bottom alignment, the text sits on the yoffset (descent) line
            ref_bottom = ref_y
        elif va == "top":
            # For top alignment, bottom is at position - text_height + yoffset
            ref_bottom = ref_y + yoffset - text_height
        elif va == "baseline":
            # For baseline alignment, need to account for descent below baseline
            ref_bottom = ref_y - yoffset
        else:
            msg = f"Text option `verticalalignment={va}` not recognized."
            raise ValueError(msg)

        # Add proper spacing: always include descent offset plus padding
        auto_spacing = text_height_corr if pad == "auto" else pad_offset
        _y = ref_bottom - yoffset - auto_spacing
        va = "top"
        ha = "left"
    elif loc == "above":
        _x = ref_left
        pad_offset = 0.0 if pad == "auto" else float(pad) / 100
        va = txt_obj.get_verticalalignment()
        ref_y = txt_obj.get_position()[1]
        # Calculate the top edge of the reference text
        if va == "bottom":
            ref_top = ref_y + yoffset + text_height
        elif va == "top":
            ref_top = ref_y + yoffset
        elif va == "baseline":
            # Special case: baseline positioning - use a smaller offset than full text height
            ref_top = ref_y + text_height
        else:
            msg = f"Text option `verticalalignment={va}` not recognized."
            raise ValueError(msg)
        _y = ref_top + pad_offset
        va = "bottom"
        ha = "left"
    elif loc == "left":
        pad_offset = 0.0 if pad == "auto" else float(pad) / 100
        _x = ref_left - (text_width_corr if pad == "auto" else pad_offset)
        va = txt_obj.get_verticalalignment()
        if va == "bottom":
            _y = txt_obj.get_position()[1] + yoffset + text_height_corr
        elif va == "top":
            _y = txt_obj.get_position()[1] + yoffset - text_height
        elif va == "baseline":
            _y = txt_obj.get_position()[1] + text_height_corr
        else:
            msg = f"Text option `verticalalignment={va}` not recognized."
            raise ValueError(msg)
        va = "baseline"
        ha = "right"
    else:
        msg = f'Kwarg `loc={loc}` is not a valid specifier. Choose from `["right", "below", "above", "left"]`'
        raise RuntimeError(msg)
    txt_artist = text_class(_x, _y, s, va=va, ha=ha, transform=ax.transAxes, **kwargs)
    ax._add_text(txt_artist)  # type: ignore[attr-defined]
    return txt_artist


def exp_text(
    exp: str = "",
    text: str = "",
    supp: str | None = None,
    lumi: str | None = None,
    loc: int | None = None,
    *,
    ax: Axes | None = None,
    fontsize: (
        float | str | tuple[float | str, float | str, float | str, float | str] | None
    ) = None,
    fontweight: tuple[str, str, str, str] = ("bold", "normal", "normal", "normal"),
    fontstyle: tuple[str, str, str, str] = ("normal", "italic", "normal", "normal"),
    **kwargs: Any,
) -> tuple[mtext.Text, mtext.Text | None, mtext.Text | None, mtext.Text | None]:
    """Add typical LHC experiment primary label to the axes.

    Parameters
    ----------
    exp : str, optional
        Experiment name, by default "".
    text : str, optional
        Secondary experiment label, typically not-bold and smaller
        font-size. For example "Simulation" or "Preliminary", by default "".
    supp : str | None, optional
        Supplementary text to add (e.g., "Private Work"), by default None.
    lumi : str, optional
        Luminosity information text, by default None.
    loc : int | None, optional
        Label position:
        - 0 : Above axes, left aligned
        - 1 : Top left corner
        - 2 : Top left corner, multiline
        - 3 : Split EXP above axes, rest of label in top left corner
        - 4 : ATLAS-style (top left corner with luminosity below)
        By default None (uses 0).
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched), by default None.
    fontsize : int | float | str | tuple[float | str, float | str, float | str, float | str], optional
        Font size specification. Can be:
        - None: Uses rcParams default with relative scaling (exp=1.3x, text=1x, lumi=0.77x, supp=0.77x)
        - float: Base size with relative scaling applied
        - str: Matplotlib size string ("small", "large", etc.) with relative scaling applied
        - tuple: (exp_size, text_size, lumi_size, supp_size) for explicit control
          Each element can be float or matplotlib size string
    fontweight : tuple[str, str, str, str], optional
        Tuple of fontweights for (exp, text, lumi, supp), by default ("bold", "normal", "normal", "normal").
    fontstyle : tuple[str, str, str, str], optional
        Tuple of fontstyles for (exp, text, lumi, supp), by default ("normal", "italic", "normal", "normal").
    **kwargs
        Additional keyword arguments passed to text functions.

    Returns
    -------
    tuple
        Tuple of text objects (exp_txt, exp_suff, exp_lumi, exp_supp).
        Elements are None if not created.
    """

    loc = 0 if loc is None else loc
    ax = ax if ax is not None else plt.gca()

    # Handle fontsize parameter - can be None, float, str, or tuple
    if isinstance(fontsize, tuple):
        # Tuple: convert each element to points directly
        _fontsize_exp, _fontsize, _fontsize_lumi, _fontsize_supp = [
            _fontsize_to_points(fs) for fs in fontsize
        ]
    else:
        # Single value or None: apply relative scaling
        base_fontsize = (
            rcParams["font.size"] if fontsize is None else _fontsize_to_points(fontsize)
        )
        _fontsize_exp = base_fontsize * 1.3
        _fontsize = base_fontsize
        _fontsize_lumi = base_fontsize / 1.1
        _fontsize_supp = base_fontsize / 1.3
    _inside_pad = max(5, _fontsize_axis(ax, _fontsize_exp) * 100)
    _italic_exp, _italic_suff, _italic_lumi, _italic_supp = fontstyle
    _weight_exp, _weight_suff, _weight_lumi, _weight_supp = fontweight

    # Special cases
    if (
        loc in [0, 3] and ax.get_yaxis().get_major_formatter().get_useOffset()  # type: ignore[attr-defined]
    ):  # Requires figure.draw call, fetch only when needed
        ax.figure.draw(ax.figure.canvas.get_renderer())  # type: ignore[attr-defined]
        _sci_box = _pixel_to_axis(
            ax.get_yaxis().offsetText.get_window_extent(ax.figure.canvas.get_renderer())  # type: ignore[attr-defined]
        )
        _sci_offset = max(0, _sci_box.width * 1.1)
    else:
        _sci_offset = 0

    # Create reusable parameter dictionaries
    base_params = {"ax": ax, **kwargs}
    exp_params = {
        "fontsize": _fontsize_exp,
        "fontweight": _weight_exp,
        "fontstyle": _italic_exp,
        "text_class": ExpLabel,
        **base_params,
    }
    suff_params = {
        "fontsize": _fontsize,
        "fontweight": _weight_suff,
        "fontstyle": _italic_suff,
        "text_class": ExpText,
        **base_params,
    }
    lumi_params = {
        "fontsize": _fontsize_lumi,
        "fontweight": _weight_lumi,
        "fontstyle": _italic_lumi,
        "text_class": LumiText,
        **base_params,
    }
    supp_params = {
        "fontsize": _fontsize_supp,
        "fontweight": _weight_supp,
        "fontstyle": _italic_supp,
        "text_class": SuppText,
        **base_params,
    }

    if lumi is not None and loc != 4:  # All but 'ATLAS' style
        exp_lumi = add_text(lumi, loc="over right", xpad=0, ypad=0, **lumi_params)

    if loc == 0:
        exp_txt = add_text(
            exp,
            loc="over left",
            va="bottom",
            xpad=_sci_offset * 100,
            ypad=0,
            **exp_params,
        )
        exp_suff = append_text(text, exp_txt, loc="right", **suff_params)
        if supp is not None:
            exp_supp = add_text(
                supp,
                x="right_out",
                y="top_in",
                xpad=1,
                ypad=0,
                rotation=90,
                **supp_params,
            )
    elif loc == 1:
        exp_txt = add_text(exp, loc="top left", pad=_inside_pad, **exp_params)
        exp_suff = append_text(text, exp_txt, loc="right", **suff_params)
        if supp is not None:
            exp_supp = append_text(supp, exp_txt, loc="below", **supp_params)
    elif loc == 2:
        exp_txt = add_text(exp, loc="top left", pad=_inside_pad, **exp_params)
        exp_suff = append_text(text, exp_txt, loc="below", **suff_params)
        if supp is not None:
            exp_supp = append_text(supp, exp_suff, loc="below", **supp_params)
    elif loc == 3:
        exp_txt = add_text(
            exp, loc="over left", xpad=_sci_offset * 100, ypad=0, **exp_params
        )
        exp_suff = add_text(text, loc="top left", pad=_inside_pad, **suff_params)
        if supp is not None:
            exp_supp = append_text(supp, exp_suff, loc="below", **supp_params)
    elif loc == 4:
        exp_txt = add_text(exp, loc="top left", pad=_inside_pad, **exp_params)
        exp_suff = append_text(text, exp_txt, loc="right", **suff_params)
        if lumi is not None:
            exp_lumi = append_text(lumi, exp_txt, loc="below", **lumi_params)
        if supp is not None:
            exp_supp = append_text(
                supp,
                exp_txt if lumi is None else exp_lumi,
                loc="below",
                **supp_params,
            )
    else:
        msg = f"Invalid location: {loc}. Valid options are 0-4."
        raise ValueError(msg)

    return (
        exp_txt,
        exp_suff,
        exp_lumi if lumi is not None else None,
        exp_supp if supp is not None else None,
    )


@deprecate_parameter("label", reason='Use `text="..."` instead.')
@deprecate_parameter("pub", reason='Use `supp="..."` instead.')
@deprecate_parameter(
    "italic",
    reason="Use `fontstyle=(bool, bool, bool, bool)` instead.",
    removed=True,
)
@deprecate_parameter(
    "weight",
    reason='Use `fontweight=("bold", "normal", "normal", "normal")` instead.',
    removed=True,
)
@deprecate_parameter("pub", reason='Use `supp="..."` instead.')
def exp_label(
    *,
    exp: str = "",
    text: str = "",
    supp: str | None = None,
    loc: int | None = None,
    data: bool = False,
    year: str | float | None = None,
    lumi: str | float | None = None,
    lumi_format: str = "{0}",
    com: str | float | None = None,
    llabel: str | None = None,
    rlabel: str | None = None,
    fontsize: (
        float | str | tuple[float | str, float | str, float | str, float | str] | None
    ) = None,
    fontweight: tuple[str, str, str, str] = ("bold", "normal", "normal", "normal"),
    fontstyle: tuple[str, str, str, str] = ("normal", "italic", "normal", "normal"),
    label: str | None = None,  # Deprecated
    pub: Any = None,  # Deprecated  # noqa: ARG001
    ax: Axes | None = None,
    **kwargs: Any,
) -> tuple[mtext.Text, mtext.Text | None, mtext.Text | None, mtext.Text | None]:
    """A convenience wrapper for adding experiment labels with luminosity information.

    This function combines experiment text and luminosity information in a single call,
    providing common labeling layouts for LHC experiment plots.

    Parameters
    ----------
    exp : str, optional
        Experiment name (e.g., "CMS", "ATLAS"), by default "".
    text : str, optional
        Secondary text to append after experiment name, typically "Preliminary",
        "Supplementary", "Private Work", or "Work in Progress", by default "".
    supp : str | None, optional
        Supplementary text to add below main label, by default None.
    loc : int | None, optional
        Label position layout:
        - 0 : Above axes, left aligned
        - 1 : Top left corner, single line
        - 2 : Top left corner, multiline
        - 3 : Split - experiment above axes, secondary text in top left corner
        - 4 : ATLAS-style - top left corner with luminosity below
        By default None (uses 0).
    data : bool, optional
        If False, prepends "Simulation" to the label text. Default False.
    year : str | float | None, optional
        Year when data was collected, by default None.
    lumi : str | float | None, optional
        Integrated luminosity value in fb⁻¹, by default None.
    lumi_format : str, optional
        Format string for luminosity display, by default "{0}".
        Example: "{0:.1f}" for one decimal place.
    com : str | float | None, optional
        Center-of-mass energy in TeV, by default None (uses 13).
        Common values: 7, 8, 13, 13.6, 14.
    llabel : str | None, optional
        Manual override for left-hand label text. Overrides "data" and "text" parameters.
    rlabel : str | None, optional
        Manual override for right-hand label text. Overrides "year", "lumi", "com" parameters.
    fontsize : int | float | str | tuple[float | str, float | str, float | str, float | str] | None, optional
        Font size specification:
        - None: Uses rcParams default with relative scaling
        - float/int: Base size with relative scaling applied
        - str: Matplotlib size string ("small", "large", etc.) with relative scaling
        - tuple: (exp_size, text_size, lumi_size, supp_size) for explicit control
    fontweight : tuple[str, str, str, str], optional
        Font weights for (exp, text, lumi, supp) elements,
        by default ("bold", "normal", "normal", "normal").
    fontstyle : tuple[str, str, str, str], optional
        Font styles for (exp, text, lumi, supp) elements,
        by default ("normal", "italic", "normal", "normal").
    ax : matplotlib.axes.Axes | None, optional
        Axes object to add labels to. If None, uses current axes.
    **kwargs : Any
        Additional keyword arguments passed to text functions.

    Returns
    -------
    tuple[mtext.Text, mtext.Text | None, mtext.Text | None, mtext.Text | None]
        Tuple of text objects: (exp_label, secondary_text, luminosity_text, supplementary_text).
        Elements are None if not created.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import mplhep as mh
    >>> fig, ax = plt.subplots()
    >>> mh.exp_label(exp="CMS", text="Preliminary", lumi=138, year=2018)

    >>> # Custom positioning and formatting
    >>> mh.exp_label(exp="ATLAS", loc=4, lumi=139, lumi_format="{0:.0f}")
    """
    if label is not None and text is None:
        text = label
    if rlabel is None:
        lumi_func = _lumi_line_atlas if loc == 4 else _lumi_line
        rlabel = lumi_func(year=year, lumi=lumi, lumi_format=lumi_format, com=com)
    if llabel is None:
        _data_sim = "Simulation " if not data else ""
        llabel = _data_sim + text

    return exp_text(
        exp=exp,
        text=llabel,
        loc=loc,
        ax=ax,
        supp=supp,
        lumi=rlabel,
        fontsize=fontsize,
        fontweight=fontweight,
        fontstyle=fontstyle,
        **kwargs,
    )


def savelabels(
    fname: str = "",
    ax: Axes | None = None,
    labels: list[tuple[str, str]] | list[str] | None = None,
    **kwargs: Any,
) -> None:
    """
    Save multiple copies of a figure with different label variations.

    This function automatically generates multiple versions of a plot with
    different experiment label text variations, useful for creating preliminary
    and final versions of plots.

    Parameters
    ----------
    fname : str
        Primary filename to be passed to ``plt.savefig``. Can include path and extension.
    ax : matplotlib.axes.Axes | None, optional
        Axes object containing the labels to modify. If None, uses current axes.
    labels : list[tuple[str, str]] | list[str] | None, optional
        Label variations to create. Can be:

        - None: Uses default variations [("", ""), ("Preliminary", "pas"),
          ("Supplementary", "supp"), ("Work in Progress", "wip")]
        - List of strings: Creates filename suffixes automatically
        - List of tuples: (label_text, filename_suffix) pairs

        If filename suffix contains "." it's treated as absolute filename.
        If current label contains "Simulation", it will be preserved.
    **kwargs : Any
        Additional keyword arguments passed to ``plt.savefig``.

    Examples
    --------
    >>> import mplhep as mh
    >>> mh.cms.label(data=False)
    >>> mh.savelabels('test.png')
    # Produces: test.png, test_pas.png, test_supp.png, test_wip.png

    >>> mh.savelabels('test', labels=[("FOO", "foo.pdf"), ("BAR", "bar")])
    # Produces: foo.pdf, test_bar.png
    """
    if labels is None:
        labels = [
            ("", ""),
            ("Preliminary", "pas"),
            ("Supplementary", "supp"),
            ("Work in Progress", "wip"),
        ]
    if isinstance(labels, list) and len(labels) > 0 and isinstance(labels[0], str):
        # Convert list of strings to list of tuples
        str_labels: list[str] = labels  # type: ignore[assignment]
        labels = [(label, label.replace(" ", "_").lower()) for label in str_labels]
    if ax is None:
        ax = plt.gca()

    label_base = next(ch for ch in ax.get_children() if isinstance(ch, ExpText))
    _sim = "Simulation" if "Simulation" in label_base.get_text() else ""

    # At this point, labels is guaranteed to be list[tuple[str, str]]
    tuple_labels: list[tuple[str, str]] = labels  # type: ignore[assignment]
    for label_text, suffix in tuple_labels:
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

        path_parts: list[str] = save_name.split("/")[:-1]
        path_dir = os.path.join(*path_parts) if path_parts else ""
        if path_dir and not os.path.exists(path_dir):
            os.makedirs(path_dir)

        if isinstance(ax.figure, plt.Figure):
            ax.figure.savefig(save_name, **kwargs)


def save_variations(
    fig: Figure, name: str, text_list: list[str] | None = None, exp: str | None = None
) -> None:
    """Lite ``savelabels``

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object to save variations of.
    name : str
        Savename to pass to `plt.savefig()`.
    text_list : list[str] | None, optional
        Variations of ExpText text object to cycle through, by default None.
    exp : str | None, optional
        Change experiment name label, by default None.
    """
    if text_list is None:
        text_list = ["Preliminary", ""]

    from mplhep.label import ExpText  # noqa: PLC0415

    for text in text_list:
        for ax in fig.get_axes():
            exp_labels = [t for t in ax.get_children() if isinstance(t, ExpText)]
            suffixes = [t for t in ax.get_children() if isinstance(t, ExpText)]
            for exp_label, suffix_text in zip(exp_labels, suffixes):
                if exp is not None:
                    exp_label.set_text(exp)
                suffix_text.set_text(text)
        name_ext = "" if text == "" else "_" + text.lower()
        if exp is not None:
            name_ext = exp.lower() + name_ext
        save_name = name.split(".")[0] + name_ext + "." + name.split(".")[1]
        fig.savefig(save_name)
