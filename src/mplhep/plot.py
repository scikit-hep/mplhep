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
    EnhancedPlottableHistogram,
    _check_counting_histogram,
    _get_plottable_protocol_bins,
    _hist_object_handler,
    _invert_collection_order,
)
from ._utils import (
    _align_marker as align_marker,
)
from ._utils import (
    _get_histogram_axes_title as get_histogram_axes_title,
)
from ._utils import (
    _get_plottables as get_plottables,
)
from ._utils import (
    _isLight as isLight,
)
from ._utils import (
    _make_plottable_histogram as make_plottable_histogram,
)
from ._utils import (
    _process_histogram_parts as process_histogram_parts,
)
from ._utils import (
    _to_padded2d as to_padded2d,
)
from .comparison_functions import (
    _check_binning_consistency,
)
from .utils import (
    _get_model_type,
    append_axes,
    set_fitting_ylabel_fontsize,
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
def hist(
    x,
    bins=10,
    *,
    range=None,
    density=False,
    weights=None,
    yerr: ArrayLike | bool | None = True,
    histtype: str = "step",
    label=None,
    ax: mpl.axes.Axes | None = None,
    **kwargs,
):
    """
    Create histogram from unbinned data, matching `plt.hist` API but using `histplot`.

    This function provides a convenient way to histogram raw data values while
    benefiting from the extended features of `histplot`, such as automatic error
    bar calculation, bin-width normalization, and HEP-style plotting options.

    Parameters
    ----------
    x : array-like or list of array-like
        Input values to histogram. Can be a single array or a list of arrays
        for multiple histograms.
    bins : int or sequence, default: 10
        Number of bins or bin edges. If an integer, defines the number of
        equal-width bins in the range. If a sequence, defines the bin edges.
    range : tuple, optional
        The lower and upper range of the bins as (min, max). If not provided,
        range is (x.min(), x.max()). Values outside the range are ignored.
    density : bool, default: False
        If True, normalize histogram to form a probability density.
    weights : array-like, optional
        Array of weights, of the same shape as `x`. Each value in `x`
        contributes its associated weight towards the bin count.
    yerr : array-like or bool, default: True
        Histogram uncertainties. If True (default), sqrt(N) errors or poissonian
        interval when weights are specified. Can also be an array of errors.
    histtype : {'step', 'fill', 'errorbar', 'band'}, default: "step"
        Type of histogram to plot (see `histplot` for details).
    label : str or list of str, optional
        Label(s) for legend entry.
    ax : matplotlib.axes.Axes, optional
        Axes object to plot on. If None, uses current axes.
    **kwargs
        Additional keyword arguments passed to `histplot`.

    Returns
    -------
    List[Hist1DArtists]
        Artists created by histplot.

    Examples
    --------
    >>> import mplhep as mh
    >>> import numpy as np
    >>> data = np.random.normal(100, 15, 1000)
    >>> mh.hist(data, bins=50, range=(50, 150))

    >>> # Multiple datasets
    >>> data1 = np.random.normal(100, 15, 1000)
    >>> data2 = np.random.normal(120, 15, 1000)
    >>> mh.hist([data1, data2], bins=50, label=['Dataset 1', 'Dataset 2'])

    See Also
    --------
    histplot : Plot pre-binned histograms
    matplotlib.pyplot.hist : Matplotlib histogram function

    """
    # Store range parameter to avoid shadowing builtin
    hist_range = range

    # Handle multiple datasets
    if isinstance(x, (list, tuple)) and not isinstance(x[0], (int, float, np.number)):
        # Multiple datasets - histogram each one
        datasets = x

        # Process bins - if integer, we need to find a common range
        if isinstance(bins, (int, np.integer)):
            if hist_range is None:
                # Find common range across all datasets
                all_data = np.concatenate([np.asarray(d).ravel() for d in datasets])
                hist_range = (np.min(all_data), np.max(all_data))
            bin_edges = np.linspace(hist_range[0], hist_range[1], bins + 1)
        else:
            bin_edges = np.asarray(bins)

        # Histogram each dataset
        hist_values = []
        hist_w2 = []
        for dataset in datasets:
            data_arr = np.asarray(dataset).ravel()
            w = None if weights is None else np.asarray(weights).ravel()

            h, _ = np.histogram(data_arr, bins=bin_edges, weights=w, density=False)
            hist_values.append(h)

            # Calculate w2 for error estimation if weights are provided
            if w is not None:
                h_w2, _ = np.histogram(
                    data_arr, bins=bin_edges, weights=w**2, density=False
                )
                hist_w2.append(h_w2)

        # Pass to histplot
        w2_arg = hist_w2 if weights is not None and len(hist_w2) > 0 else None
        # If w2 is provided, don't pass yerr (w2 will be used for error calculation)
        # If yerr is explicitly an array, still pass it
        yerr_arg = None if w2_arg is not None and isinstance(yerr, bool) else yerr
        return histplot(
            hist_values,
            bin_edges,
            yerr=yerr_arg,
            w2=w2_arg,
            density=density,
            histtype=histtype,
            label=label,
            ax=ax,
            **kwargs,
        )
    # Single dataset
    x = np.asarray(x).ravel()
    w = None if weights is None else np.asarray(weights).ravel()

    # Create histogram
    if isinstance(bins, (int, np.integer)):
        if hist_range is None:
            hist_range = (np.min(x), np.max(x))
        bin_edges = np.linspace(hist_range[0], hist_range[1], bins + 1)
    else:
        bin_edges = np.asarray(bins)

    h, _ = np.histogram(x, bins=bin_edges, weights=w, density=False)

    # Calculate w2 for error estimation if weights are provided
    w2_arg = None
    if w is not None:
        h_w2, _ = np.histogram(x, bins=bin_edges, weights=w**2, density=False)
        w2_arg = h_w2

    # If w2 is provided, don't pass yerr (w2 will be used for error calculation)
    # If yerr is explicitly an array, still pass it
    yerr_arg = None if w2_arg is not None and isinstance(yerr, bool) else yerr

    # Pass to histplot
    return histplot(
        h,
        bin_edges,
        yerr=yerr_arg,
        w2=w2_arg,
        density=density,
        histtype=histtype,
        label=label,
        ax=ax,
        **kwargs,
    )


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
    w2method : callable, optional
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
    histtype : {'step', 'fill', 'errorbar', 'bar', 'barstep', 'band'}, optional, default: "step"
        Type of histogram to plot:

        - "step": skyline/step/outline of a histogram using [plt.stairs](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs).
        - "fill": filled histogram using [plt.stairs](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs).
        - "errorbar": single marker histogram using [plt.errorbar](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.errorbar.html#matplotlib-axes-axes-errorbar).
        - "bar": If multiple data are given the bars are arranged side by side using [plt.bar](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html#matplotlib-axes-axes-bar). If only one histogram is provided, it will be treated as "fill" histtype.
        - "barstep": If multiple data are given the steps are arranged side by side using [plt.stairs](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs). Supports yerr representation. If one histogram is provided, it will be treated as "step" histtype.
        - "band": filled band spanning the yerr range of the histogram using [plt.stairs](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stairs.html#matplotlib-axes-axes-stairs).

    label : str or list, optional
        Label for legend entry.
    sort : str, optional {'label'/'l', 'yield'/'y'}
        "label"/"l": sort histograms alphabetically by label, "yield"/"y": sort by total histogram yield. Append '_r' to reverse the order.
    ax : matplotlib.axes.Axes, optional
        Axes object (if None, last one is fetched or one is created)
    flow :  str, optional { "show", "sum", "hint", "none"}
        Whether plot the under/overflow bin. If "show", add additional under/overflow bin.
        If "sum", add the under/overflow bin content to first/last bin.
        If "hint", draw markers at the axis to indicate presence of under/overflow.
        If "none", do nothing.
    **kwargs :
        Keyword arguments passed to underlying matplotlib functions -
        {'stairs', 'errorbar'}.

    Other parameters
    ----------------
    w2 : iterable, optional
        Sum of the histogram weights squared for poissonian interval error
        calculation
    xerr : bool or float, optional
        Size of xerr if ``histtype == 'errorbar'``. If ``True``, bin-width will be used.
    edges : bool, default: True, optional
        Specifies whether to draw first and last edges of the histogram.
    binticks : bool, default: False, optional
        Attempts to draw x-axis ticks coinciding with bin boundaries if feasible.
    xoffsets : bool, default: False,
        If True, the bin "centers" of plotted histograms will be offset within their bin.

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

    _chunked_kwargs: list[dict[str, Any]] = [{} for _ in hists]
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
        if "color" not in kwargs or kwargs.get("color") is None:
            # Inverse default color cycle
            _colors = [ax._get_lines.get_next_color() for _ in plottables]  # type: ignore[attr-defined]
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
        if underflow != 0.0:
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
        if overflow != 0.0:
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
    cbarextend=None,
    cmin=None,
    cmax=None,
    mask=None,
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
    cbarextend : bool, optional, default None (auto)
        Extends figure size to keep original axes size same as without cbar.
        If None (default), automatically set to True for single-axes figures
        and False for multi-axes figures to prevent layout issues.
    cmin : float, optional
        Colorbar minimum.
    cmax : float, optional
        Colorbar maximum.
    mask : 2D array (H-like), optional
        Boolean mask to hide cells. Cells with False value are not shown.
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

    # Auto-detect cbarextend: only extend for single-axes figures
    if cbarextend is None:
        cbarextend = len(ax.figure.axes) == 1

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
    if mask is not None:
        H[~mask.T] = None

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


def model(
    stacked_components=None,
    stacked_labels=None,
    stacked_colors=None,
    unstacked_components=None,
    unstacked_labels=None,
    unstacked_colors=None,
    xlabel=None,
    ylabel=None,
    stacked_kwargs=None,
    unstacked_kwargs_list=None,
    model_sum_kwargs=None,
    function_range=None,
    model_uncertainty=True,
    model_uncertainty_label="MC stat. unc.",
    fig=None,
    ax=None,
    flow="hint",
):
    """
    Plot model made of a collection of histograms.

    Parameters
    ----------
    stacked_components : list of histogram (e.g. Hist, boost_histogram, np.histogram, TH1), optional
        The list of histograms to be stacked composing the model. Default is None.
    stacked_labels : list of str, optional
        The labels of the model stacked components. Default is None.
    stacked_colors : list of str, optional
        The colors of the model stacked components. Default is None.
    unstacked_components : list of histogram (e.g. Hist, boost_histogram, np.histogram, TH1), optional
        The list of histograms not to be stacked composing the model. Default is None.
    unstacked_labels : list of str, optional
        The labels of the model unstacked components. Default is None.
    unstacked_colors : list of str, optional
        The colors of the model unstacked components. Default is None.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    stacked_kwargs : dict, optional
        The keyword arguments used when plotting the stacked components in plot_hist() or plot_function(), one of which is called only once. Default is None.
    unstacked_kwargs_list : list of dict, optional
        The list of keyword arguments used when plotting the unstacked components in plot_hist() or plot_function(), one of which is called once for each unstacked component. Default is None.
    model_sum_kwargs : dict, optional
        The keyword arguments for the plot_hist() function for the sum of the model components.
        Has no effect if all the model components are stacked or if the model is one unstacked element.
        The special keyword "show" can be used with a boolean to specify whether to show or not the sum of the model components.
        Default is None. If None is provided, this is set to {"show": True, "label": "Model", "color": "navy"}.
    function_range : tuple, optional (mandatory if the model is made of functions)
        The range for the x-axis if the model is made of functions.
    model_uncertainty : bool, optional
        If False, set the model uncertainties to zeros. Default is True.
    model_uncertainty_label : str, optional
        The label for the model uncertainties. Default is "MC stat. unc.".
    fig : matplotlib.figure.Figure or None, optional
        The Figure object to use for the plot. Create a new one if none is provided.
    ax : matplotlib.axes.Axes or None, optional
        The Axes object to use for the plot. Create a new one if none is provided.
    flow : str, optional
        Whether to show under/overflow bins. Options: "show", "sum", "hint", "none". Default is "hint".


    Returns
    -------
    fig : matplotlib.figure.Figure
        The Figure object containing the plot.
    ax : matplotlib.axes.Axes
        The Axes object containing the plot.

    """
    if model_sum_kwargs is None:
        model_sum_kwargs = {"show": True, "label": "Model", "color": "navy"}
    if unstacked_kwargs_list is None:
        unstacked_kwargs_list = []
    if stacked_kwargs is None:
        stacked_kwargs = {}
    if unstacked_components is None:
        unstacked_components = []
    if stacked_components is None:
        stacked_components = []

    # Create copies of the kwargs arguments passed as lists/dicts to avoid modifying them
    stacked_kwargs = stacked_kwargs.copy()
    unstacked_kwargs_list = unstacked_kwargs_list.copy()
    model_sum_kwargs = model_sum_kwargs.copy()

    components = stacked_components + unstacked_components

    if len(components) == 0:
        msg = "Need to provide at least one model component."
        raise ValueError(msg)

    model_type = _get_model_type(components)

    if model_type == "histograms":
        components = [
            (
                make_plottable_histogram(c)
                if not isinstance(c, EnhancedPlottableHistogram)
                else c
            )
            for c in components
        ]
        _check_counting_histogram(components)
        _check_binning_consistency(components)

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    elif fig is None or ax is None:
        msg = "Need to provide fig and ax (or none of them)."
        raise ValueError(msg)

    if model_type == "histograms":
        xlim = (components[0].edges_1d()[0], components[0].edges_1d()[-1])
    else:
        if function_range is None:
            msg = "Need to provide function_range for model made of functions."
            raise ValueError(msg)
        xlim = function_range

    if len(stacked_components) > 0:
        # Plot the stacked components
        stacked_kwargs.setdefault("edgecolor", "black")
        stacked_kwargs.setdefault("linewidth", 0.5)
        if model_type == "histograms":
            stacked_kwargs.setdefault("histtype", "fill")
            histplot(
                stacked_components,
                ax=ax,
                stack=True,
                color=stacked_colors,
                label=stacked_labels,
                flow=flow,
                **stacked_kwargs,
            )
            if model_uncertainty and len(unstacked_components) == 0:
                histplot(
                    sum(stacked_components),
                    ax=ax,
                    label=model_uncertainty_label,
                    histtype="band",
                    flow=flow,
                )
        else:
            funcplot(
                stacked_components,
                ax=ax,
                stack=True,
                colors=stacked_colors,
                labels=stacked_labels,
                range=xlim,
                **stacked_kwargs,
            )

    if len(unstacked_components) > 0:
        # Plot the unstacked components
        if unstacked_colors is None:
            unstacked_colors = [None] * len(unstacked_components)
        if unstacked_labels is None:
            unstacked_labels = [None] * len(unstacked_components)
        if len(unstacked_kwargs_list) == 0:
            unstacked_kwargs_list = [{}] * len(unstacked_components)
        for component, color, label, unstacked_kwargs in zip(
            unstacked_components,
            unstacked_colors,
            unstacked_labels,
            unstacked_kwargs_list,
        ):
            if model_type == "histograms":
                unstacked_kwargs.setdefault("histtype", "step")
                histplot(
                    component,
                    ax=ax,
                    stack=False,
                    color=color,
                    label=label,
                    flow=flow,
                    **unstacked_kwargs,
                )
            else:
                funcplot(
                    component,
                    ax=ax,
                    stack=False,
                    color=color,
                    label=label,
                    range=xlim,
                    **unstacked_kwargs,
                )
        # Plot the sum of all the components
        if model_sum_kwargs.pop("show", True) and (
            len(unstacked_components) > 1 or len(stacked_components) > 0
        ):
            if model_type == "histograms":
                model_sum_kwargs.setdefault("yerr", False)
            if model_type == "histograms":
                histplot(
                    sum(components),
                    ax=ax,
                    histtype="step",
                    flow=flow,
                    **model_sum_kwargs,
                )
                if (
                    model_uncertainty
                    and model_sum_kwargs.get("yerr", False) is not True
                ):
                    histplot(
                        sum(components),
                        ax=ax,
                        label=model_uncertainty_label,
                        histtype="band",
                        flow=flow,
                    )
            else:

                def sum_function(x):
                    return sum(f(x) for f in components)

                funcplot(
                    sum_function,
                    ax=ax,
                    range=xlim,
                    **model_sum_kwargs,
                )
        elif (
            model_uncertainty
            and len(stacked_components) == 0
            and len(unstacked_components) == 1
            and model_type == "histograms"
        ):
            histplot(
                sum(components),
                ax=ax,
                label=model_uncertainty_label,
                histtype="band",
                flow=flow,
            )

    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    set_fitting_ylabel_fontsize(ax)
    ax.legend()

    return fig, ax
