from __future__ import annotations

import collections.abc
import inspect
import logging
from typing import TYPE_CHECKING, Any, NamedTuple, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)

from ._utils import (
    _align_marker as align_marker,
)
from ._utils import (
    _get_histogram_axes_title as get_histogram_axes_title,
)
from ._utils import (
    _get_plottable_protocol_bins,
    _hist_object_handler,
    _invert_collection_order,
)
from ._utils import (
    _get_plottables as get_plottables,
)
from ._utils import (
    _isLight as isLight,
)
from ._utils import (
    _process_histogram_parts as process_histogram_parts,
)
from ._utils import (
    _to_padded2d as to_padded2d,
)
from .utils import (
    append_axes,
)

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


class StairsArtists(NamedTuple):
    stairs: Any
    errorbar: Any
    legend_artist: Any


class ErrorBarArtists(NamedTuple):
    errorbar: Any


class ColormeshArtists(NamedTuple):
    pcolormesh: Any
    cbar: Any
    text: Any


Hist1DArtists = Union[StairsArtists, ErrorBarArtists]
Hist2DArtists = ColormeshArtists


def soft_update_kwargs(kwargs, mods, rc=True):
    not_default = [k for k, v in mpl.rcParamsDefault.items() if v != mpl.rcParams[k]]
    respect = [
        "hatch.linewidth",
        "lines.linewidth",
        "patch.linewidth",
        "lines.linestyle",
    ]
    aliases = {"ls": "linestyle", "lw": "linewidth"}
    kwargs = {aliases.get(k, k): v for k, v in kwargs.items()}
    for key, val in mods.items():
        rc_modded = (key in not_default) or (
            key in [k.split(".")[-1] for k in not_default if k in respect]
        )
        if key not in kwargs and (rc and not rc_modded):
            kwargs[key] = val
    return kwargs


########################################
# Histogram plotter
def histplot(
    H,  # Histogram object, tuple or array
    bins=None,  # Bins to be supplied when h is a value array or iterable of array
    *,
    yerr: ArrayLike | bool | None = None,
    w2=None,
    w2method=None,
    stack: bool = False,
    density: bool = False,
    binwnorm=None,
    histtype: str = "step",
    xerr=False,
    label=None,
    sort=None,
    edges=True,
    binticks=False,
    xoffsets=None,
    ax: mpl.axes.Axes | None = None,
    flow="hint",
    **kwargs,
):
    """
    Create a 1D histogram plot from `np.histogram`-like inputs.

    Parameters
    ----------
        H : object
            Histogram object with containing values and optionally bins. Can be:

            - `np.histogram` tuple
            - PlottableProtocol histogram object
            - `boost_histogram` classic (<0.13) histogram object
            - raw histogram values, provided `bins` is specified.

            Or list thereof.
        bins : iterable, optional
            Histogram bins, if not part of ``H``.
        yerr : iterable or bool, optional
            Histogram uncertainties. Following modes are supported:
            - True, sqrt(N) errors or poissonian interval when ``w2`` is specified
            - shape(N) array of for one sided errors or list thereof
            - shape(Nx2) array of for two sided errors or list thereof
        w2 : iterable, optional
            Sum of the histogram weights squared for poissonian interval error
            calculation
        w2method: callable, optional
            Function calculating CLs with signature ``low, high = fcn(w, w2)``. Here
            ``low`` and ``high`` are given in absolute terms, not relative to w.
            Default is ``None``. If w2 has integer values (likely to be data) poisson
            interval is calculated, otherwise the resulting error is symmetric
            ``sqrt(w2)``. Specifying ``poisson`` or ``sqrt`` will force that behaviours.
        stack : bool, optional
            Whether to stack or overlay non-axis dimension (if it exists). N.B. in
            contrast to ROOT, stacking is performed in a single call aka
            ``histplot([h1, h2, ...], stack=True)`` as opposed to multiple calls.
        density : bool, optional
            If true, convert sum weights to probability density (i.e. integrates to 1
            over domain of axis) (Note: this option conflicts with ``binwnorm``)
        binwnorm : float, optional
            If true, convert sum weights to bin-width-normalized, with unit equal to
                supplied value (usually you want to specify 1.)
        histtype: {'step', 'fill', 'errorbar', 'bar', 'barstep', 'band'}, optional, default: "step"
            Type of histogram to plot:
            - "step": skyline/step/outline of a histogram using `plt.stairs <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs>`_
            - "fill": filled histogram using `plt.stairs <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs>`_
            - "errorbar": single marker histogram using `plt.errorbar <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.errorbar.html#matplotlib-axes-axes-errorbar>`_
            - "bar": If multiple data are given the bars are arranged side by side using `plt.bar <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html#matplotlib-axes-axes-bar>`_ If only one histogram is provided, it will be treated as "fill" histtype
            - "barstep": If multiple data are given the steps are arranged side by side using `plt.stairs <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs>`_ . Supports yerr representation. If one histogram is provided, it will be treated as "step" histtype.
            - "band": filled band spanning the yerr range of the histogram using `plt.stairs <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs>`_
        xerr:  bool or float, optional
            Size of xerr if ``histtype == 'errorbar'``. If ``True``, bin-width will be used.
        label : str or list, optional
            Label for legend entry.
        sort: {'label'/'l', 'yield'/'y'}, optional
            Append '_r' for reverse.
        edges : bool, default: True, optional
            Specifies whether to draw first and last edges of the histogram
        binticks : bool, default: False, optional
            Attempts to draw x-axis ticks coinciding with bin boundaries if feasible.
        xoffsets: bool, default: False,
            If True, the bin "centers" of plotted histograms will be offset within their bin.
        ax : matplotlib.axes.Axes, optional
            Axes object (if None, last one is fetched or one is created)
        flow :  str, optional { "show", "sum", "hint", "none"}
            Whether plot the under/overflow bin. If "show", add additional under/overflow bin.
            If "sum", add the under/overflow bin content to first/last bin.
        **kwargs :
            Keyword arguments passed to underlying matplotlib functions -
            {'stairs', 'errorbar'}.
    Returns
    -------
        List[Hist1DArtists]

    """

    # ax check
    if ax is None:
        ax = plt.gca()
    elif not isinstance(ax, plt.Axes):
        msg = "ax must be a matplotlib Axes object"
        raise ValueError(msg)

    # arg check
    _allowed_histtype = ["fill", "step", "errorbar", "band", "bar", "barstep"]
    _err_message = f"Select 'histtype' from: {_allowed_histtype}, got '{histtype}'"
    assert histtype in _allowed_histtype, _err_message
    assert flow is None or flow in {
        "show",
        "sum",
        "hint",
        "none",
    }, "flow must be show, sum, hint, or none"
    if hasattr(H, "values") or hasattr(H[0], "values"):  # Check for hist-like inputs
        assert bins is None, (
            "When plotting hist(-like) objects, specifying bins is not allowed."
        )
        assert w2 is None, (
            "When plotting hist(-like) objects, specifying w2 is not allowed."
        )
    if w2 is not None:
        assert np.array(w2).shape == np.array(H).shape, (
            "w2 must have the same shape as H"
        )

    # Convert 1/0 etc to real bools
    stack = bool(stack)
    density = bool(density)
    edges = bool(edges)
    binticks = bool(binticks)

    # Process input
    hists = list(process_histogram_parts(H, bins))
    final_bins, xtick_labels = _get_plottable_protocol_bins(hists[0].axes[0])
    _bin_widths = np.diff(final_bins)
    _bin_centers = final_bins[1:] - _bin_widths / float(2)
    assert final_bins.ndim == 1, "bins need to be 1 dimensional"
    _x_axes_label = ax.get_xlabel()
    x_axes_label = (
        _x_axes_label
        if _x_axes_label != ""
        else get_histogram_axes_title(hists[0].axes[0])
    )

    _labels: list[str | None]
    if label is None:
        _labels = [None] * len(hists)
    elif isinstance(label, str):
        _labels = [label] * len(hists)
    elif not np.iterable(label):
        _labels = [str(label)] * len(hists)
    else:
        _labels = [str(lab) for lab in label]

    def iterable_not_string(arg):
        return isinstance(arg, collections.abc.Iterable) and not isinstance(arg, str)

    _chunked_kwargs: list[dict[str, Any]] = []
    for _ in range(len(hists)):
        _chunked_kwargs.append({})
    for kwarg, kwarg_content in kwargs.items():
        # Check if iterable
        if iterable_not_string(kwarg_content):
            # Check if tuple of floats or ints (can be used for colors)
            if isinstance(kwarg_content, tuple) and all(
                isinstance(x, (int, float)) for x in kwarg_content
            ):
                for i in range(len(_chunked_kwargs)):
                    _chunked_kwargs[i][kwarg] = kwarg_content
            else:
                for i, kw in enumerate(kwarg_content):
                    _chunked_kwargs[i][kwarg] = kw
        else:
            for i in range(len(_chunked_kwargs)):
                _chunked_kwargs[i][kwarg] = kwarg_content

    # Sorting
    if sort is not None:
        if isinstance(sort, str):
            if sort.split("_")[0] in ["l", "label"] and isinstance(_labels, list):
                order = np.argsort(label)  # [::-1]
            elif sort.split("_")[0] in ["y", "yield"]:
                _yields = [np.sum(_h.values()) for _h in hists]  # type: ignore[var-annotated]
                order = np.argsort(_yields)
            if len(sort.split("_")) == 2 and sort.split("_")[1] == "r":
                order = order[::-1]
        elif isinstance(sort, (list, np.ndarray)):
            if len(sort) != len(hists):
                msg = f"Sort indexing array is of the wrong size - {len(sort)}, {len(hists)} expected."
                raise ValueError(msg)
            order = np.asarray(sort)
        else:
            msg = f"Sort type: {sort} not understood."
            raise ValueError(msg)
        hists = [hists[ix] for ix in order]
        _chunked_kwargs = [_chunked_kwargs[ix] for ix in order]
        _labels = [_labels[ix] for ix in order]

    plottables, flow_info = get_plottables(
        hists,
        bins=final_bins,
        w2=w2,
        w2method=w2method,
        yerr=yerr,
        stack=stack,
        density=density,
        binwnorm=binwnorm,
        flow=flow,
        xoffsets=xoffsets,
    )
    flow_bins, underflow, overflow = flow_info

    ##########
    # Plotting
    return_artists: list[StairsArtists | ErrorBarArtists] = []

    if histtype == "bar" and len(plottables) == 1:
        histtype = "fill"
    elif histtype == "barstep" and len(plottables) == 1:
        histtype = "step"

    # # customize color cycle assignment when stacking to match legend
    if stack:
        plottables = plottables[::-1]
        _chunked_kwargs = _chunked_kwargs[::-1]
        _labels = _labels[::-1]
        if "color" not in kwargs:
            # Inverse default color cycle
            _colors = []
            for _ in range(len(plottables)):
                _colors.append(ax._get_lines.get_next_color())  # type: ignore[attr-defined]
            _colors.reverse()
            for i in range(len(plottables)):
                _chunked_kwargs[i].update({"color": _colors[i]})

    if "bar" in histtype:
        if kwargs.get("bin_width") is None:
            _full_bin_width = 0.8
        else:
            _full_bin_width = kwargs.pop("bin_width")
        _shift = np.linspace(
            -(_full_bin_width / 2), _full_bin_width / 2, len(plottables), endpoint=False
        )
        _shift += _full_bin_width / (2 * len(plottables))

    if "step" in histtype:
        for i in range(len(plottables)):
            do_errors = yerr is not False and (
                (yerr is not None or w2 is not None)
                or plottables[i].variances() is not None
            )

            _kwargs = _chunked_kwargs[i]

            if _kwargs.get("bin_width"):
                _kwargs.pop("bin_width")

            _label = _labels[i] if do_errors else None
            _step_label = _labels[i] if not do_errors else None

            _kwargs = soft_update_kwargs(_kwargs, {"linewidth": 1.5})

            _plot_info = plottables[i].to_stairs()
            _plot_info["baseline"] = None if not edges else 0

            if _kwargs.get("color") is None:
                _kwargs["color"] = ax._get_lines.get_next_color()  # type: ignore[attr-defined]

            if histtype == "step":
                _s = ax.stairs(
                    **_plot_info,
                    label=_step_label,
                    **_kwargs,
                )
                if do_errors:
                    _kwargs = soft_update_kwargs(_kwargs, {"color": _s.get_edgecolor()})
                    _ls = _kwargs.pop("linestyle", "-")
                    _kwargs["linestyle"] = "none"
                    _plot_info = plottables[i].to_errorbar()
                    del _plot_info["xerr"]
                    _e = ax.errorbar(
                        **_plot_info,
                        **_kwargs,
                    )
                    _e_leg = ax.errorbar(
                        [],
                        [],
                        yerr=1,
                        xerr=None,
                        color=_s.get_edgecolor(),
                        label=_label,
                        linestyle=_ls,
                    )
                return_artists.append(
                    StairsArtists(
                        _s,
                        _e if do_errors else None,
                        _e_leg if do_errors else None,
                    )
                )
                _artist = _s

            # histtype = barstep
            else:
                if _kwargs.get("edgecolor") is None:
                    edgecolor = _kwargs.get("color")
                else:
                    edgecolor = _kwargs.pop("edgecolor")

                _b = ax.bar(
                    plottables[i].centers + _shift[i],
                    plottables[i].values(),
                    width=_full_bin_width / len(plottables),
                    label=_step_label,
                    align="center",
                    edgecolor=edgecolor,
                    fill=False,
                    **_kwargs,
                )

                if do_errors:
                    _ls = _kwargs.pop("linestyle", "-")
                    # _kwargs["linestyle"] = "none"
                    _plot_info = plottables[i].to_errorbar()
                    _e = ax.errorbar(
                        _plot_info["x"] + _shift[i],
                        _plot_info["y"],
                        yerr=_plot_info["yerr"],
                        linestyle="none",
                        **_kwargs,
                    )
                    _e_leg = ax.errorbar(
                        [],
                        [],
                        yerr=1,
                        xerr=None,
                        color=_kwargs.get("color"),
                        label=_label,
                        linestyle=_ls,
                    )
                return_artists.append(
                    StairsArtists(
                        _b, _e if do_errors else None, _e_leg if do_errors else None
                    )
                )
                _artist = _b  # type: ignore[assignment]

    elif histtype == "bar":
        for i in range(len(plottables)):
            _kwargs = _chunked_kwargs[i]

            if _kwargs.get("bin_width"):
                _kwargs.pop("bin_width")

            _b = ax.bar(
                plottables[i].centers + _shift[i],
                plottables[i].values(),
                width=_full_bin_width / len(plottables),
                label=_labels[i],
                align="center",
                fill=True,
                **_kwargs,
            )
            return_artists.append(StairsArtists(_b, None, None))
        _artist = _b  # type: ignore[assignment]

    elif histtype == "fill":
        for i in range(len(plottables)):
            _kwargs = _chunked_kwargs[i]
            _f = ax.stairs(
                **plottables[i].to_stairs(), label=_labels[i], fill=True, **_kwargs
            )
            return_artists.append(StairsArtists(_f, None, None))
        _artist = _f

    elif histtype == "band":
        band_defaults = {
            "alpha": 0.5,
            "edgecolor": "darkgray",
            "facecolor": "whitesmoke",
            "hatch": "/////",
        }
        for i in range(len(plottables)):
            _kwargs = _chunked_kwargs[i]
            _f = ax.stairs(
                **plottables[i].to_stairband(),
                label=_labels[i],
                fill=True,
                **soft_update_kwargs(_kwargs, band_defaults),
            )
            return_artists.append(StairsArtists(_f, None, None))
        _artist = _f

    elif histtype == "errorbar":
        err_defaults = {
            "linestyle": "none",
            "marker": ".",
            "markersize": 10.0,
            "elinewidth": 1,
        }

        _xerr: np.ndarray | float | int | None

        if xerr is True:
            _xerr = _bin_widths / 2
        elif isinstance(xerr, (int, float)) and not isinstance(xerr, bool):
            _xerr = xerr
        else:
            _xerr = None

        for i in range(len(plottables)):
            _kwargs = _chunked_kwargs[i]
            _plot_info = plottables[i].to_errorbar()
            if yerr is False:
                _plot_info["yerr"] = None
            if not xerr:
                del _plot_info["xerr"]
            if isinstance(xerr, (int, float)) and not isinstance(xerr, bool):
                _plot_info["xerr"] = xerr
            elif isinstance(xerr, (np.ndarray, list)):
                _plot_info["xerr"] = xerr[i]
            _e = ax.errorbar(
                **_plot_info,
                label=_labels[i],
                **soft_update_kwargs(_kwargs, err_defaults),
            )
            return_artists.append(ErrorBarArtists(_e))

        _artist = _e[0]

    # Add sticky edges for autoscale
    if "bar" not in histtype:
        listy = _artist.sticky_edges.y
        assert hasattr(listy, "append"), "cannot append to sticky edges"
        listy.append(0)

    if xtick_labels is None or flow == "show":
        if binticks:
            _slice = round(float(len(final_bins)) / len(ax.get_xticks())) + 1
            ax.set_xticks(final_bins[::_slice])
    else:
        ax.set_xticks(_bin_centers)
        ax.set_xticklabels(xtick_labels)

    if x_axes_label:
        ax.set_xlabel(x_axes_label)

    # Flow extra styling
    if (fig := ax.figure) is None:
        msg = "No figure found"
        raise ValueError(msg)
    if flow == "hint":
        _marker_size = (
            30
            * ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).width
        )
        if underflow > 0.0:
            ax.scatter(
                final_bins[0],
                0,
                _marker_size,
                marker=align_marker("<", halign="right"),
                edgecolor="black",
                zorder=5,
                clip_on=False,
                facecolor="white",
                transform=ax.get_xaxis_transform(),
            )
        if overflow > 0.0:
            ax.scatter(
                final_bins[-1],
                0,
                _marker_size,
                marker=align_marker(">", halign="left"),
                edgecolor="black",
                zorder=5,
                clip_on=False,
                facecolor="white",
                transform=ax.get_xaxis_transform(),
            )

    elif flow == "show":
        underflow_xticklabel = f"<{flow_bins[1]:g}"
        overflow_xticklabel = f">{flow_bins[-2]:g}"

        # Loop over shared x axes to get xticks and xticklabels
        xticks, xticklabels = np.array([]), []
        shared_axes = ax.get_shared_x_axes().get_siblings(ax)
        shared_axes = [
            _ax for _ax in shared_axes if _ax.get_position().x0 == ax.get_position().x0
        ]
        for _ax in shared_axes:
            _xticks = _ax.get_xticks()
            _xticklabels = [label.get_text() for label in _ax.get_xticklabels()]

            # Check if underflow/overflow xtick already exists
            if (
                underflow_xticklabel in _xticklabels
                or overflow_xticklabel in _xticklabels
            ):
                xticks = _xticks
                xticklabels = _xticklabels
                break
            if len(_xticklabels) > 0:
                xticks = _xticks
                xticklabels = _xticklabels

        lw = ax.spines["bottom"].get_linewidth()
        _edges = plottables[0].edges_1d()
        _centers = plottables[0].centers
        _marker_size = (
            20
            * ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).width
        )

        if underflow > 0.0 or underflow_xticklabel in xticklabels:
            # Replace any existing xticks in underflow region with underflow bin center
            _mask = xticks > flow_bins[1]
            xticks = np.insert(xticks[_mask], 0, _centers[0])
            xticklabels = [underflow_xticklabel] + [
                xlab for i, xlab in enumerate(xticklabels) if _mask[i]
            ]

            # Don't draw markers on the top of the top axis
            top_axis = max(shared_axes, key=lambda a: a.get_position().y0)

            # Draw on all shared axes
            for _ax in shared_axes:
                _ax.set_xticks(xticks)
                _ax.set_xticklabels(xticklabels)
                for h in [0, 1]:
                    # Don't draw marker on the top of the top axis
                    if _ax == top_axis and h == 1:
                        continue

                    _ax.plot(
                        [_edges[0], _edges[1]],
                        [h, h],
                        color="white",
                        zorder=5,
                        ls="--",
                        lw=lw,
                        transform=_ax.get_xaxis_transform(),
                        clip_on=False,
                    )

                    _ax.scatter(
                        _centers[0],
                        h,
                        _marker_size,
                        marker=align_marker("d", valign="center"),
                        edgecolor="black",
                        zorder=5,
                        clip_on=False,
                        facecolor="white",
                        transform=_ax.get_xaxis_transform(),
                    )
        if overflow > 0.0 or overflow_xticklabel in xticklabels:
            # Replace any existing xticks in overflow region with overflow bin center
            _mask = xticks < flow_bins[-2]
            xticks = np.insert(xticks[_mask], sum(_mask), _centers[-1])
            xticklabels = [xlab for i, xlab in enumerate(xticklabels) if _mask[i]] + [
                overflow_xticklabel
            ]

            # Don't draw markers on the top of the top axis
            top_axis = max(shared_axes, key=lambda a: a.get_position().y0)

            # Draw on all shared axes
            for _ax in shared_axes:
                _ax.set_xticks(xticks)
                _ax.set_xticklabels(xticklabels)

                for h in [0, 1]:
                    # Don't draw marker on the top of the top axis
                    if _ax == top_axis and h == 1:
                        continue

                    _ax.plot(
                        [_edges[-2], _edges[-1]],
                        [h, h],
                        color="white",
                        zorder=5,
                        ls="--",
                        lw=lw,
                        transform=_ax.get_xaxis_transform(),
                        clip_on=False,
                    )

                    _ax.scatter(
                        _centers[-1],
                        h,
                        _marker_size,
                        marker=align_marker("d", valign="center"),
                        edgecolor="black",
                        zorder=5,
                        clip_on=False,
                        facecolor="white",
                        transform=_ax.get_xaxis_transform(),
                    )

    return return_artists


def hist2dplot(
    H,
    xbins=None,
    ybins=None,
    labels=None,
    labels_fontsize=None,
    labels_round=None,
    labels_color=None,
    cbar: bool = True,
    cbarsize="7%",
    cbarpad=0.2,
    cbarpos="right",
    cbarextend=True,
    cmin=None,
    cmax=None,
    ax: mpl.axes.Axes | None = None,
    flow="hint",
    binwnorm=None,
    **kwargs,
):
    """
    Create a 2D histogram plot from `np.histogram`-like inputs.

    Parameters
    ----------
    H : object
        Histogram object with containing values and optionally bins. Can be:

        - `np.histogram` tuple
        - `boost_histogram` histogram object
        - raw histogram values as list of list or 2d-array

    xbins : 1D array-like, optional, default None
        Histogram bins along x axis, if not part of ``H``.
    ybins : 1D array-like, optional, default None
        Histogram bins along y axis, if not part of ``H``.
    labels : 2D array (H-like) or bool, default None, optional
        Array of per-bin labels to display. If ``True`` will
        display numerical values
    labels_fontsize : float, optional, default None
        Fontsize of labels.
    labels_color : str, optional, default None
        Color of labels. If not given, will be decided automatically.
    labels_round : int, optional, default None
        Round labels to given number of decimals
    cbar : bool, optional, default True
        Draw a colorbar. In contrast to mpl behaviors the cbar axes is
        appended in such a way that it doesn't modify the original axes
        width:height ratio.
    cbarsize : str or float, optional, default "7%"
        Colorbar width.
    cbarpad : float, optional, default 0.2
        Colorbar distance from main axis.
    cbarpos : {'right', 'left', 'bottom', 'top'}, optional,  default "right"
        Colorbar position w.r.t main axis.
    cbarextend : bool, optional, default False
        Extends figure size to keep original axes size same as without cbar.
        Only safe for 1 axes per fig.
    cmin : float, optional
        Colorbar minimum.
    cmax : float, optional
        Colorbar maximum.
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched or one is created)
    flow :  str, optional {"show", "sum","hint", None}
            Whether plot the under/overflow bin. If "show", add additional under/overflow bin. If "sum", add the under/overflow bin content to first/last bin. "hint" would highlight the bins with under/overflow contents
    binwnorm : float, optional
        If true, convert sum weights to bin-width-normalized, with unit equal to
            supplied value (usually you want to specify 1.)
    **kwargs :
        Keyword arguments passed to underlying matplotlib function - pcolormesh.

    Returns
    -------
        Hist2DArtist

    """

    # ax check
    if ax is None:
        ax = plt.gca()
    elif not isinstance(ax, plt.Axes):
        msg = "ax must be a matplotlib Axes object"
        raise ValueError(msg)

    h = _hist_object_handler(H, xbins, ybins)

    # TODO: use Histogram everywhere

    H = np.copy(h.values())
    xbins, xtick_labels = _get_plottable_protocol_bins(h.axes[0])
    ybins, ytick_labels = _get_plottable_protocol_bins(h.axes[1])
    # Show under/overflow bins
    # "show": Add additional bin with 2 times bin width
    if (
        hasattr(h, "values")
        and "flow" not in inspect.getfullargspec(h.values).args
        and flow is not None
    ):
        flow = None
    elif flow in ["hint", "show"]:
        xwidth, ywidth = (xbins[-1] - xbins[0]) * 0.05, (ybins[-1] - ybins[0]) * 0.05
        pxbins = np.r_[xbins[0] - xwidth, xbins, xbins[-1] + xwidth]
        pybins = np.r_[ybins[0] - ywidth, ybins, ybins[-1] + ywidth]
        padded = to_padded2d(h)
        hint_xlo, hint_xhi, hint_ylo, hint_yhi = True, True, True, True
        if np.all(padded[0, :] == 0):
            padded = padded[1:, :]
            pxbins = pxbins[1:]
            hint_xlo = False
        if np.all(padded[-1, :] == 0):
            padded = padded[:-1, :]
            pxbins = pxbins[:-1]
            hint_xhi = False
        if np.all(padded[:, 0] == 0):
            padded = padded[:, 1:]
            pybins = pybins[1:]
            hint_ylo = False
        if np.all(padded[:, -1] == 0):
            padded = padded[:, :-1]
            pybins = pybins[:-1]
            hint_yhi = False
        if flow == "show":
            H = padded
            xbins, ybins = pxbins, pybins
    elif flow == "sum":
        H = np.copy(h.values())
        # Sum borders
        try:
            H[0], H[-1] = (
                H[0] + h.values(flow=True)[0, 1:-1],  # type: ignore[call-arg]
                H[-1] + h.values(flow=True)[-1, 1:-1],  # type: ignore[call-arg]
            )
            H[:, 0], H[:, -1] = (
                H[:, 0] + h.values(flow=True)[1:-1, 0],  # type: ignore[call-arg]
                H[:, -1] + h.values(flow=True)[1:-1, -1],  # type: ignore[call-arg]
            )
            # Sum corners to corners
            H[0, 0], H[-1, -1], H[0, -1], H[-1, 0] = (
                h.values(flow=True)[0, 0] + H[0, 0],  # type: ignore[call-arg]
                h.values(flow=True)[-1, -1] + H[-1, -1],  # type: ignore[call-arg]
                h.values(flow=True)[0, -1] + H[0, -1],  # type: ignore[call-arg]
                h.values(flow=True)[-1, 0] + H[-1, 0],  # type: ignore[call-arg]
            )
        except TypeError as error:
            if "got an unexpected keyword argument 'flow'" in str(error):
                msg = (
                    f"The histograms value method {h!r} does not take a 'flow' argument. UHI PlottableHistogram doesn't require this to have, but it is required for this function."
                    f" Implementations like hist/boost-histogram support this argument."
                )
                raise TypeError(msg) from error
    xbin_centers = xbins[1:] - np.diff(xbins) / float(2)
    ybin_centers = ybins[1:] - np.diff(ybins) / float(2)

    _x_axes_label = ax.get_xlabel()
    x_axes_label = (
        _x_axes_label if _x_axes_label != "" else get_histogram_axes_title(h.axes[0])
    )
    _y_axes_label = ax.get_ylabel()
    y_axes_label = (
        _y_axes_label if _y_axes_label != "" else get_histogram_axes_title(h.axes[1])
    )

    H = H.T

    if cmin is not None:
        H[cmin > H] = None
    if cmax is not None:
        H[cmax < H] = None

    X, Y = np.meshgrid(xbins, ybins)

    if binwnorm is not None:
        # No error treatment so we can just scale the values
        H = H * binwnorm
        # Make sure x_bin_width and y_bin_width align with H's dimensions
        X_bin_widths, Y_bin_widths = np.meshgrid(np.diff(xbins), np.diff(ybins))
        # Calculate the bin area array, which aligns with the shape of H
        bin_area = X_bin_widths * Y_bin_widths
        H = H / bin_area

    kwargs.setdefault("shading", "flat")
    pc = ax.pcolormesh(X, Y, H, vmin=cmin, vmax=cmax, **kwargs)

    if x_axes_label:
        ax.set_xlabel(x_axes_label)
    if y_axes_label:
        ax.set_ylabel(y_axes_label)

    ax.set_xlim(xbins[0], xbins[-1])  # type: ignore[arg-type]
    ax.set_ylim(ybins[0], ybins[-1])  # type: ignore[arg-type]

    if xtick_labels is None:  # Ordered axis
        if len(ax.get_xticks()) > len(xbins) * 0.7:
            ax.set_xticks(xbins)
    else:  # Categorical axis
        ax.set_xticks(xbin_centers)
        ax.set_xticklabels(xtick_labels)
    if ytick_labels is None:
        if len(ax.get_yticks()) > len(ybins) * 0.7:
            ax.set_yticks(ybins)
    else:  # Categorical axis
        ax.set_yticks(ybin_centers)
        ax.set_yticklabels(ytick_labels)

    if cbar:
        cax = append_axes(
            ax, size=cbarsize, pad=cbarpad, position=cbarpos, extend=cbarextend
        )
        cb_obj = plt.colorbar(pc, cax=cax)
    else:
        cb_obj = None

    plt.sca(ax)
    if flow == "show":
        if hint_xlo:
            ax.plot(
                [xbins[1]] * 2,
                [0, 1],
                ls="--",
                color="lightgrey",
                clip_on=False,
                transform=ax.get_xaxis_transform(),
            )
        if hint_xhi:
            ax.plot(
                [xbins[-2]] * 2,
                [0, 1],
                ls="--",
                color="lightgrey",
                clip_on=False,
                transform=ax.get_xaxis_transform(),
            )
        if hint_ylo:
            ax.plot(
                [0, 1],
                [ybins[1]] * 2,
                ls="--",
                color="lightgrey",
                clip_on=False,
                transform=ax.get_yaxis_transform(),
            )
        if hint_yhi:
            ax.plot(
                [0, 1],
                [ybins[-2]] * 2,
                ls="--",
                color="lightgrey",
                clip_on=False,
                transform=ax.get_yaxis_transform(),
            )
    elif flow == "hint":
        if (fig := ax.figure) is None:
            msg = "No figure found."
            raise ValueError(msg)
        _marker_size = (
            30
            * ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).width
        )
        if hint_xlo:
            ax.scatter(
                0,
                0,
                _marker_size,
                marker=align_marker("<", halign="right", valign="bottom"),
                edgecolor="black",
                zorder=5,
                clip_on=False,
                facecolor="white",
                transform=ax.transAxes,
            )
        if hint_xhi:
            ax.scatter(
                1,
                0,
                _marker_size,
                marker=align_marker(">", halign="left"),
                edgecolor="black",
                zorder=5,
                clip_on=False,
                facecolor="white",
                transform=ax.transAxes,
            )
        if hint_ylo:
            ax.scatter(
                0,
                0,
                _marker_size,
                marker=align_marker("v", valign="top", halign="left"),
                edgecolor="black",
                zorder=5,
                clip_on=False,
                facecolor="white",
                transform=ax.transAxes,
            )
        if hint_yhi:
            ax.scatter(
                0,
                1,
                _marker_size,
                marker=align_marker("^", valign="bottom"),
                edgecolor="black",
                zorder=5,
                clip_on=False,
                facecolor="white",
                transform=ax.transAxes,
            )

    _labels: np.ndarray | None = None
    if isinstance(labels, bool):
        _labels = H if labels else None
    elif np.iterable(labels):
        label_array = np.asarray(labels).T
        if H.shape == label_array.shape:
            _labels = label_array
        else:
            msg = f"Labels input has incorrect shape (expect: {H.shape}, got: {label_array.shape})"
            raise ValueError(msg)
    elif labels is not None:
        msg = "Labels not understood, either specify a bool or a Hist-like array"
        raise ValueError(msg)

    text_artists = []
    if _labels is not None:
        if (pccmap := pc.cmap) is None:
            msg = "No colormap found."
            raise ValueError(msg)
        for ix, xc in enumerate(xbin_centers):
            for iy, yc in enumerate(ybin_centers):
                normedh = pc.norm(H[iy, ix])
                if labels_color is not None:
                    color = labels_color
                else:
                    color = "black" if isLight(pccmap(normedh)[:-1]) else "lightgrey"
                text_artists.append(
                    ax.text(
                        xc,
                        yc,
                        (
                            _labels[iy, ix].round(labels_round)  # type: ignore[arg-type]
                            if labels_round is not None
                            else _labels[iy, ix]
                        ),
                        ha="center",
                        va="center",
                        color=color,
                        fontsize=labels_fontsize,
                    )
                )

    return ColormeshArtists(pc, cb_obj, text_artists)


def funcplot(func, range, ax, stack=False, npoints=1000, **kwargs):
    """
    Plot a 1D function on a given range.

    Parameters
    ----------
    func : function or list of functions
        The 1D function or list of functions to plot.
        The function(s) should support vectorization (i.e. accept a numpy array as input).
    range : tuple
        The range of the function(s). The function(s) will be plotted on the interval [range[0], range[1]].
    ax : matplotlib.axes.Axes
        The Axes instance for plotting.
    stack : bool, optional
        Whether to use ax.stackplot() to plot the function(s) as a stacked plot. Default is False.
    npoints : int, optional
        The number of points to use for plotting. Default is 1000.
    **kwargs
        Additional keyword arguments forwarded to ax.plot() (in case stack=False) or ax.stackplot() (in case stack=True).
    """
    x = np.linspace(range[0], range[1], npoints)

    if not stack:
        if not isinstance(func, list):
            ax.plot(x, func(x), **kwargs)
        else:
            ax.plot(
                x,
                np.array([func(x) for func in func]).T,
                **kwargs,
            )
    else:
        if kwargs.get("labels") is None:
            kwargs["labels"] = []

        if not isinstance(func, list):
            func = [func]
        n_collections_before = len(list(ax.collections))
        ax.stackplot(
            x,
            [f(x) for f in func],
            **kwargs,
        )
        # Invert the order of the collection objects to match the top-down order of the stackplot
        _invert_collection_order(ax, n_collections_before)
