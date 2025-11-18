"""
Collection of functions to plot histograms
"""

from __future__ import annotations

import contextlib
import re

import matplotlib.pyplot as plt
import numpy as np

from ._utils import (
    EnhancedPlottableHistogram,
    _check_counting_histogram,
)
from ._utils import (
    _make_plottable_histogram as make_plottable_histogram,
)
from .comparison_functions import (
    _check_binning_consistency,
    get_comparison,
)
from .plot import (
    histplot,
    model,
)
from .utils import (
    _get_model_type,
    set_fitting_ylabel_fontsize,
    subplots,
)


def _get_math_text(text):
    """
    Search for text between $ and return it.

    Parameters
    ----------
    text : str
        The input string.

    Returns
    -------
    str
        The text between $ or the input string if no $ are found.
    """
    match = re.search(r"\$(.*?)\$", text)
    if match:
        return match.group(1)
    return text


def hists(
    h1,
    h2,
    xlabel=None,
    ylabel=None,
    h1_label="h1",
    h2_label="h2",
    flow="hint",
    fig=None,
    ax_main=None,
    ax_comparison=None,
    **comparison_kwargs,
):
    """
    Compare two histograms.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The first histogram to compare.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The second histogram to compare.
    xlabel : str, optional
        The label for the x-axis. Default is None.
    ylabel : str, optional
        The label for the y-axis. Default is None.
    h1_label : str, optional
        The label for the first histogram. Default is "h1".
    h2_label : str, optional
        The label for the second histogram. Default is "h2".
    flow : str, optional
        Whether to plot the under/overflow bin. If "show", add additional under/overflow bin.
        If "sum", add the under/overflow bin content to first/last bin.
        If "hint", draw markers at the axis to indicate presence of under/overflow.
        If "none", do nothing. Default is "hint".
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    **comparison_kwargs : optional
        Arguments to be passed to comparison(), including the choice of the comparison function and the treatment of the uncertainties (see documentation of comparison() for details).

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    ax_main : matplotlib.axes.Axes
        The main axes for the histogram comparison.
    ax_comparison : matplotlib.axes.Axes
        The axes for the comparison plot.

    See Also
    --------
    comparison : Plot the comparison between two histograms.

    """
    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram(h1_plottable)
    _check_counting_histogram(h2_plottable)

    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = subplots(nrows=2)
    elif fig is None or ax_main is None or ax_comparison is None:
        msg = "Need to provide fig, ax_main and ax_comparison (or none of them)."
        raise ValueError(msg)

    histplot(h1_plottable, ax=ax_main, label=h1_label, histtype="step", flow=flow)
    histplot(h2_plottable, ax=ax_main, label=h2_label, histtype="step", flow=flow)

    # Only set xlim if not showing flow bins (histplot handles xlim for flow="show")
    if flow != "show":
        xlim = (h1_plottable.edges_1d()[0], h1_plottable.edges_1d()[-1])
        ax_main.set_xlim(xlim)

    ax_main.set_ylabel(ylabel)
    ax_main.legend()
    _ = ax_main.xaxis.set_ticklabels([])

    comparison(
        h1_plottable,
        h2_plottable,
        ax_comparison,
        xlabel=xlabel,
        h1_label=h1_label,
        h2_label=h2_label,
        flow=flow,
        **comparison_kwargs,
    )

    fig.align_ylabels()

    return fig, ax_main, ax_comparison


def comparison(
    h1,
    h2,
    ax,
    xlabel="",
    h1_label="h1",
    h2_label="h2",
    comparison="ratio",
    comparison_ylabel=None,
    comparison_ylim=None,
    h1_w2method="sqrt",
    flow="hint",
    **histplot_kwargs,
):
    """
    Plot the comparison between two histograms.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The first histogram for comparison.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The second histogram for comparison.
    ax : matplotlib.axes.Axes
        The axes to plot the comparison.
    xlabel : str, optional
        The label for the x-axis. Default is "".
    h1_label : str, optional
        The label for the first histogram. Default is "h1".
    h2_label : str, optional
        The label for the second histogram. Default is "h2".
    comparison : str, optional
        The type of comparison to plot ("ratio", "split_ratio", "pull", "difference", "relative_difference", "efficiency", or "asymmetry"). Default is "ratio".
        When the `split_ratio` option is used, both the h1 and h2 uncertainties are scaled down by the h2 bin contents, and the h2 adjusted uncertainties are shown separately as a hatched area.
    comparison_ylabel : str, optional
        The label for the y-axis. Default is the explicit formula used to compute the comparison plot.
    comparison_ylim : tuple or None, optional
        The y-axis limits for the comparison plot. Default is None. If None, standard y-axis limits are setup.
    h1_w2method : str, optional
        What kind of bin uncertainty to use for h1: "sqrt" for the Poisson standard deviation derived from the variance stored in the histogram object, "poisson" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "sqrt".
        Asymmetrical uncertainties are not supported for the asymmetry and efficiency comparisons.
    flow : str, optional
        Whether to plot the under/overflow bin. If "show", add additional under/overflow bin.
        If "sum", add the under/overflow bin content to first/last bin.
        If "hint", draw markers at the axis to indicate presence of under/overflow.
        If "none", do nothing. Default is "hint".
    **histplot_kwargs : optional
        Arguments to be passed to histplot(), called in case the comparison is "pull", or plot_error_hist(), called for every other comparison case. In the former case, the default arguments are histtype="stepfilled" and color="darkgrey". In the later case, the default argument is color="black".

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the plotted comparison.

    See Also
    --------
    hists : Compare two histograms and plot the comparison.

    """
    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    h1_label = _get_math_text(h1_label)
    h2_label = _get_math_text(h2_label)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram(h1_plottable)
    _check_counting_histogram(h2_plottable)

    # When flow="show", we need to compute comparison on flow-included values
    # so that the comparison histogram also has underflow/overflow bins
    used_flow_bins = False
    if flow == "show":
        # Try to get flow bins if they exist (from original histogram objects, not plottable)
        try:
            # Access flow bins from the original histogram objects
            h1_flow_values = h1.values(flow=True)
            h2_flow_values = h2.values(flow=True)
            h1_flow_variances = h1.variances(flow=True)
            h2_flow_variances = h2.variances(flow=True)

            # Check if histogram actually has flow bins (length should be +2)
            if len(h1_flow_values) == len(h1_plottable.values()) + 2:
                # Use the original histograms which already have flow bins
                h1_for_comparison = h1
                h2_for_comparison = h2
                used_flow_bins = True
            else:
                # No actual flow bins, use regular histograms
                h1_for_comparison = h1_plottable
                h2_for_comparison = h2_plottable
        except (AttributeError, TypeError):
            # Histogram doesn't support flow bins, use regular histograms
            h1_for_comparison = h1_plottable
            h2_for_comparison = h2_plottable
    else:
        h1_for_comparison = h1_plottable
        h2_for_comparison = h2_plottable

    if used_flow_bins:
        # Compute comparison on flow-included values directly
        # Since get_comparison() would strip flow bins, we compute it ourselves
        h1_vals_flow = h1_for_comparison.values(flow=True)
        h2_vals_flow = h2_for_comparison.values(flow=True)
        h1_vars_flow = h1_for_comparison.variances(flow=True)
        h2_vars_flow = h2_for_comparison.variances(flow=True)

        # For now, only support ratio comparison with flow bins
        # Compute ratio: h1/h2
        with np.errstate(divide='ignore', invalid='ignore'):
            comparison_values = np.where(h2_vals_flow != 0, h1_vals_flow / h2_vals_flow, np.nan)
            # Compute uncertainties (symmetric for now)
            if h1_vars_flow is not None and h2_vars_flow is not None:
                # Ratio uncertainty: sqrt((var1/val2^2) + (val1^2 * var2 / val2^4))
                ratio_var = np.where(
                    h2_vals_flow != 0,
                    (h1_vars_flow / h2_vals_flow**2) + (h1_vals_flow**2 * h2_vars_flow / h2_vals_flow**4),
                    np.nan
                )
                lower_uncertainties = np.sqrt(ratio_var)
                upper_uncertainties = lower_uncertainties
            else:
                lower_uncertainties = np.zeros_like(comparison_values)
                upper_uncertainties = np.zeros_like(comparison_values)
    else:
        comparison_values, lower_uncertainties, upper_uncertainties = get_comparison(
            h1_for_comparison, h2_for_comparison, comparison, h1_w2method
        )

    # Use the comparison histogram directly if it has flow bins, otherwise create EnhancedPlottableHistogram
    if used_flow_bins:
        # comparison was computed on flow-included histograms
        # Create a new histogram with the same structure
        import hist as hist_pkg
        num_bins = len(h2_plottable.values())
        edges_1d = h2_plottable.edges_1d()
        start = float(edges_1d[0])
        stop = float(edges_1d[-1])

        axis = hist_pkg.axis.Regular(
            num_bins,
            start,
            stop,
            underflow=True,
            overflow=True,
        )
        # Use Weight storage to properly store values and variances
        comparison_hist = hist_pkg.Hist(axis, storage=hist_pkg.storage.Weight())
        # Set comparison values and variances (including flow bins)
        # With Weight storage, we need to use structured array assignment
        view_flow = comparison_hist.view(flow=True)
        view_flow["value"] = comparison_values
        if np.allclose(lower_uncertainties, upper_uncertainties, equal_nan=True):
            view_flow["variance"] = lower_uncertainties**2
            histplot_kwargs.setdefault("w2method", "sqrt")
        else:
            # For asymmetric errors, we'll store them separately
            view_flow["variance"] = lower_uncertainties**2
            histplot_kwargs.setdefault("yerr", [lower_uncertainties, upper_uncertainties])
        # Use the histogram directly instead of converting to plottable
        # This preserves the flow bin structure
        comparison_plottable = comparison_hist
    else:
        # Regular comparison without flow bins
        if np.allclose(lower_uncertainties, upper_uncertainties, equal_nan=True):
            comparison_plottable = EnhancedPlottableHistogram(
                comparison_values,
                edges=h2_plottable.axes[0].edges,
                variances=lower_uncertainties**2,
                kind=h2_plottable.kind,
                w2method="sqrt",
            )
            histplot_kwargs.setdefault("w2method", "sqrt")
        else:
            comparison_plottable = EnhancedPlottableHistogram(
                comparison_values,
                edges=h2_plottable.axes[0].edges,
                yerr=[lower_uncertainties, upper_uncertainties],
                kind=h2_plottable.kind,
                w2method=h2_plottable.method,
            )
            histplot_kwargs.setdefault(
                "yerr", [comparison_plottable.yerr_lo, comparison_plottable.yerr_hi]
            )

    # Only call errors() if it's an EnhancedPlottableHistogram
    if hasattr(comparison_plottable, 'errors'):
        comparison_plottable.errors()

    if comparison == "pull":
        histplot_kwargs.setdefault("histtype", "fill")
        histplot_kwargs.setdefault("color", "darkgrey")
        histplot(comparison_plottable, ax=ax, flow=flow, **histplot_kwargs)
    else:
        histplot_kwargs.setdefault("color", "black")
        histplot_kwargs.setdefault("histtype", "errorbar")
        histplot(comparison_plottable, ax=ax, flow=flow, **histplot_kwargs)

    if comparison in ["ratio", "split_ratio", "relative_difference"]:
        if comparison_ylim is None:
            if comparison == "relative_difference":
                comparison_ylim = (-1.0, 1.0)
            else:
                comparison_ylim = (0.0, 2.0)

        if comparison == "relative_difference":
            bottom_shift = 0
            ax.axhline(0, ls="--", lw=1.0, color="black")
            ax.set_ylabel(
                r"$\frac{" + h1_label + " - " + h2_label + "}{" + h2_label + "}$"
            )
        else:
            bottom_shift = 1
            ax.axhline(1, ls="--", lw=1.0, color="black")
            ax.set_ylabel(r"$\frac{" + h1_label + "}{" + h2_label + "}$")

        if comparison == "split_ratio":
            if h2_plottable.variances() is None:
                msg = "Cannot plot split ratio with h2 uncertainties not defined."
                raise ValueError(msg)
            with np.errstate(divide="ignore", invalid="ignore"):
                h2_scaled_uncertainties = np.where(
                    h2_plottable.values() != 0,
                    np.sqrt(h2_plottable.variances()) / h2_plottable.values(),
                    np.nan,
                )
            ax.bar(
                x=h2_plottable.centers,
                bottom=np.nan_to_num(
                    bottom_shift - h2_scaled_uncertainties, nan=comparison_ylim[0]
                ),
                height=np.nan_to_num(
                    2 * h2_scaled_uncertainties,
                    nan=comparison_ylim[-1] - comparison_ylim[0],
                ),
                width=np.diff(h2_plottable.edges_1d()),
                edgecolor="dimgrey",
                hatch="////",
                fill=False,
                lw=0,
            )

    elif comparison == "pull":
        if comparison_ylim is None:
            comparison_ylim = (-5.0, 5.0)
        ax.axhline(0, ls="--", lw=1.0, color="black")
        ax.set_ylabel(
            rf"$\frac{{ {h1_label} - {h2_label} }}{{ \sqrt{{\sigma^2_{{{h1_label}}} + \sigma^2_{{{h2_label}}}}} }} $"
        )

    elif comparison == "difference":
        ax.axhline(0, ls="--", lw=1.0, color="black")
        ax.set_ylabel(f"${h1_label} - {h2_label}$")

    elif comparison == "efficiency":
        if comparison_ylim is None:
            comparison_ylim = (0.0, 1.0)
        ax.set_ylabel("Efficiency")

    elif comparison == "asymmetry":
        if comparison_ylim is None:
            comparison_ylim = (-1.0, 1.0)
        ax.axhline(0, ls="--", lw=1.0, color="black")
        ax.set_ylabel(rf"$\frac{{{h1_label} - {h2_label}}}{{{h1_label} + {h2_label}}}$")

    # Only set xlim if not showing flow bins (histplot handles xlim for flow="show")
    if flow != "show":
        xlim = (h1_plottable.edges_1d()[0], h1_plottable.edges_1d()[-1])
        ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    if comparison_ylim is not None:
        ax.set_ylim(comparison_ylim)
    if comparison_ylabel is not None:
        ax.set_ylabel(comparison_ylabel)

    return ax


def _make_hist_from_function(func, ref_hist):
    """
    Create a histogram from a function and a reference histogram.
    The returned histogram has the same binning as the reference histogram and
    is filled with the function evaluated at the bin centers of the reference histogram.

    Parameters
    ----------
    func : function
        1D function. The function should support vectorization (i.e. accept a numpy array as input).
    ref_hist : EnhancedPlottableHistogram
        The reference 1D histogram to use for the binning.

    Returns
    -------
    hist : EnhancedPlottableHistogram
        The histogram filled with the function.

    Raises
    ------
    ValueError
        If the reference histogram is not 1D.
    """
    if len(ref_hist.axes) != 1:
        msg = "The reference histogram must be 1D."
        raise ValueError(msg)

    return EnhancedPlottableHistogram(
        func(np.mean(ref_hist.axes[0].edges, axis=1)),
        edges=ref_hist.axes[0].edges,
        variances=np.zeros_like(ref_hist.values()),
        kind=ref_hist.kind,
        w2method=ref_hist.method,
    )


def data_model(
    data_hist,
    stacked_components=None,
    stacked_labels=None,
    stacked_colors=None,
    unstacked_components=None,
    unstacked_labels=None,
    unstacked_colors=None,
    xlabel=None,
    ylabel=None,
    data_label="Data",
    stacked_kwargs=None,
    unstacked_kwargs_list=None,
    model_sum_kwargs=None,
    model_uncertainty=True,
    model_uncertainty_label="MC stat. unc.",
    data_w2method="poisson",
    flow="hint",
    fig=None,
    ax_main=None,
    ax_comparison=None,
    plot_only=None,
    **comparison_kwargs,
):
    """
    Compare data to model. The data uncertainties are computed using the Poisson confidence interval.

    Parameters
    ----------
    data_hist : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The histogram for the data.
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
    data_label : str, optional
        The label for the data. Default is "Data".
    stacked_kwargs : dict, optional
        The keyword arguments used when plotting the stacked components in plot_hist() or plot_function(), one of which is called only once. Default is None.
    unstacked_kwargs_list : list of dict, optional
        The list of keyword arguments used when plotting the unstacked components in plot_hist() or plot_function(), one of which is called once for each unstacked component. Default is None.
    model_sum_kwargs : dict, optional
        The keyword arguments for the plot_hist() function for the sum of the model components.
        Has no effect if all the model components are stacked or if the model is one unstacked element.
        The special keyword "show" can be used with a boolean to specify whether to show or not the sum of the model components.
        Default is None. If None is provided, this is set to {"show": True, "label": "Sum", "color": "navy"}.
    model_uncertainty : bool, optional
        If False, set the model uncertainties to zeros. Default is True.
    model_uncertainty_label : str, optional
        The label for the model uncertainties. Default is "MC stat. unc.".
    data_w2method : str, optional
        What kind of bin uncertainty to use for data_hist: "sqrt" for the Poisson standard deviation derived from the variance stored in the histogram object, "poisson" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "poisson".
    flow : str, optional
        Whether to plot the under/overflow bin. If "show", add additional under/overflow bin.
        If "sum", add the under/overflow bin content to first/last bin.
        If "hint", draw markers at the axis to indicate presence of under/overflow.
        If "none", do nothing. Default is "hint".
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    plot_only : str, optional
        If "ax_main" or "ax_comparison", only the main or comparison axis is plotted on the figure. Both axes are plotted if None is specified, which is the default. This can only be used when fig, ax_main and ax_comparison are not provided by the user.
    **comparison_kwargs : optional
        Arguments to be passed to comparison(), including the choice of the comparison function and the treatment of the uncertainties (see documentation of comparison() for details). If they are not provided explicitly, the following arguments are passed by default: h1_label="Data", h2_label="MC", comparison="split_ratio".

    Returns
    -------
    fig : matplotlib.figure.Figure
        The Figure object containing the plots.
    ax_main : matplotlib.axes.Axes
        The Axes object for the main plot.
    ax_comparison : matplotlib.axes.Axes
        The Axes object for the comparison plot.

    See Also
    --------
    comparison : Plot the comparison between two histograms.

    """
    if model_sum_kwargs is None:
        model_sum_kwargs = {"show": True, "label": "Sum", "color": "navy"}
    if unstacked_kwargs_list is None:
        unstacked_kwargs_list = []
    if stacked_kwargs is None:
        stacked_kwargs = {}
    if unstacked_components is None:
        unstacked_components = []
    if stacked_components is None:
        stacked_components = []

    # Convert input histograms to plottable histograms for binning checks.
    # Keep original histograms for passing to histplot (to preserve flow bin info).
    # If the input is a function, it is left unchanged.
    data_hist_plottable = make_plottable_histogram(data_hist)
    stacked_components_plottable = [
        make_plottable_histogram(component) if not callable(component) else component
        for component in stacked_components
    ]
    unstacked_components_plottable = [
        make_plottable_histogram(component) if not callable(component) else component
        for component in unstacked_components
    ]

    # Create copies of the kwargs arguments passed as lists/dicts to avoid modifying them
    stacked_kwargs = stacked_kwargs.copy()
    unstacked_kwargs_list = unstacked_kwargs_list.copy()
    model_sum_kwargs = model_sum_kwargs.copy()

    # Set flow parameter in kwargs for model plotting
    stacked_kwargs.setdefault("flow", flow)
    model_sum_kwargs.setdefault("flow", flow)
    # Ensure all unstacked kwargs have flow parameter
    # If unstacked_kwargs_list is shorter than unstacked_components, extend it
    while len(unstacked_kwargs_list) < len(unstacked_components):
        unstacked_kwargs_list.append({})
    for i in range(len(unstacked_kwargs_list)):
        if unstacked_kwargs_list[i] is None:
            unstacked_kwargs_list[i] = {}
        else:
            unstacked_kwargs_list[i] = unstacked_kwargs_list[i].copy()
        unstacked_kwargs_list[i].setdefault("flow", flow)

    comparison_kwargs.setdefault("h1_label", data_label)
    comparison_kwargs.setdefault("h2_label", "MC")
    comparison_kwargs.setdefault("comparison", "split_ratio")

    model_components = stacked_components + unstacked_components
    model_components_plottable = stacked_components_plottable + unstacked_components_plottable

    if len(model_components) == 0:
        msg = "Need to provide at least one model component."
        raise ValueError(msg)

    model_type = _get_model_type(model_components)

    if model_type == "histograms":
        _check_binning_consistency([*model_components_plottable, data_hist_plottable])
        for component in [*model_components_plottable, data_hist_plottable]:
            _check_counting_histogram(component)

    if fig is None and ax_main is None and ax_comparison is None:
        if plot_only is None:
            fig, (ax_main, ax_comparison) = subplots(nrows=2)
        elif plot_only == "ax_main":
            _, ax_comparison = plt.subplots()
            fig, ax_main = plt.subplots()
        elif plot_only == "ax_comparison":
            _, ax_main = plt.subplots()
            fig, ax_comparison = plt.subplots()
        else:
            msg = "plot_only must be 'ax_main', 'ax_comparison' or None."
            raise ValueError(msg)
    elif fig is None or ax_main is None or ax_comparison is None:
        msg = "Need to provide fig, ax_main and ax_comparison (or none of them)."
        raise ValueError(msg)
    elif plot_only is not None:
        msg = "Cannot provide fig, ax_main or ax_comparison with plot_only."
        raise ValueError(msg)

    # For flow="show", don't constrain function_range
    if flow == "show":
        func_range = None
    else:
        func_range = [
            data_hist_plottable.edges_1d()[0],
            data_hist_plottable.edges_1d()[-1],
        ]

    model(
        stacked_components=stacked_components,
        stacked_labels=stacked_labels,
        stacked_colors=stacked_colors,
        unstacked_components=unstacked_components,
        unstacked_labels=unstacked_labels,
        unstacked_colors=unstacked_colors,
        ylabel=ylabel,
        stacked_kwargs=stacked_kwargs,
        unstacked_kwargs_list=unstacked_kwargs_list,
        model_sum_kwargs=model_sum_kwargs,
        function_range=func_range,
        model_uncertainty=model_uncertainty,
        model_uncertainty_label=model_uncertainty_label,
        fig=fig,
        ax=ax_main,
    )

    histplot(
        data_hist_plottable,
        ax=ax_main,
        w2method=data_w2method,
        color="black",
        label=data_label,
        histtype="errorbar",
        flow=flow,
    )

    # If flow="show", calculate the correct xlim that includes flow bins
    # We need to compute this manually because model() resets xlim to regular edges
    flow_xlim = None
    if flow == "show":
        # Get the bin width to extend xlim for flow bins
        edges = data_hist_plottable.edges_1d()
        bin_width = edges[1] - edges[0]
        # Extend by 1.5 bin widths on each side to show flow bin labels
        flow_xlim = (edges[0] - 1.5 * bin_width, edges[-1] + 1.5 * bin_width)

    if plot_only == "ax_main":
        ax_main.set_xlabel(xlabel)
    else:
        _ = ax_main.xaxis.set_ticklabels([])
        ax_main.set_xlabel(" ")

    if model_type == "histograms":
        # Sum the original histograms to preserve flow bin information for comparison
        model_hist_orig = sum(model_components)
        # Also sum plottables for variance manipulation
        model_hist_plottable = sum(model_components_plottable)
        if not model_uncertainty:
            model_hist_plottable.set_variances(np.zeros_like(model_hist_plottable.variances()))
            # Need to update the original hist's variances too if it's plottable
            if hasattr(model_hist_orig, 'set_variances'):
                model_hist_orig.set_variances(np.zeros_like(model_hist_orig.variances()))
    else:

        def sum_components(x):
            return sum(f(x) for f in model_components)

        model_hist_orig = _make_hist_from_function(sum_components, data_hist_plottable)
        model_hist_plottable = model_hist_orig

    if comparison_kwargs["comparison"] == "pull" and (
        model_type == "functions" or not model_uncertainty
    ):
        comparison_kwargs.setdefault(
            "comparison_ylabel",
            rf"$\frac{{ {comparison_kwargs['h1_label']} - {comparison_kwargs['h2_label']} }}{{ \sigma_{{{comparison_kwargs['h1_label']}}} }} $",
        )

    ax_main.legend()

    comparison(
        data_hist,
        model_hist_orig,
        ax=ax_comparison,
        xlabel=xlabel,
        w2method=data_w2method,
        flow=flow,
        **comparison_kwargs,
    )

    with contextlib.suppress(Exception):
        ylabel_fontsize = set_fitting_ylabel_fontsize(ax_main)
    ax_comparison.get_yaxis().get_label().set_size(ylabel_fontsize)

    fig.align_ylabels()

    # Restore the xlim for flow bins if needed (some operations may have reset it)
    if flow == "show" and flow_xlim is not None:
        ax_main.set_xlim(flow_xlim)

    return fig, ax_main, ax_comparison
