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
    fig=None,
    ax_main=None,
    ax_comparison=None,
    flow="hint",
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
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    flow : str, optional
        Whether to show under/overflow bins. Options: "show", "sum", "hint", "none". Default is "hint".
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

    xlim = (h1_plottable.edges_1d()[0], h1_plottable.edges_1d()[-1])

    histplot(h1_plottable, ax=ax_main, label=h1_label, histtype="step", flow=flow)
    histplot(h2_plottable, ax=ax_main, label=h2_label, histtype="step", flow=flow)
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
        Whether to show under/overflow bins. Options: "show", "sum", "hint", "none". Default is "hint".
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

    comparison_values, lower_uncertainties, upper_uncertainties = get_comparison(
        h1_plottable, h2_plottable, comparison, h1_w2method
    )

    # Compute flow bin comparison values
    underflow_comp, overflow_comp = None, None
    h1_under, h1_over = h1_plottable._underflow, h1_plottable._overflow
    h2_under, h2_over = h2_plottable._underflow, h2_plottable._overflow

    if comparison in ("ratio", "split_ratio"):
        if h1_under is not None and h2_under is not None and h2_under != 0:
            underflow_comp = h1_under / h2_under
        if h1_over is not None and h2_over is not None and h2_over != 0:
            overflow_comp = h1_over / h2_over
    elif comparison == "relative_difference":
        if h1_under is not None and h2_under is not None and h2_under != 0:
            underflow_comp = (h1_under / h2_under) - 1
        if h1_over is not None and h2_over is not None and h2_over != 0:
            overflow_comp = (h1_over / h2_over) - 1
    elif comparison == "difference":
        if h1_under is not None and h2_under is not None:
            underflow_comp = h1_under - h2_under
        if h1_over is not None and h2_over is not None:
            overflow_comp = h1_over - h2_over
    elif comparison == "pull":
        # Pull = (h1 - h2) / sqrt(var1 + var2)
        h1_under_var = h1_plottable._underflow_var
        h1_over_var = h1_plottable._overflow_var
        h2_under_var = h2_plottable._underflow_var
        h2_over_var = h2_plottable._overflow_var
        if (
            h1_under is not None
            and h2_under is not None
            and h1_under_var is not None
            and h2_under_var is not None
        ):
            denom = np.sqrt(h1_under_var + h2_under_var)
            if denom != 0:
                underflow_comp = (h1_under - h2_under) / denom
        if (
            h1_over is not None
            and h2_over is not None
            and h1_over_var is not None
            and h2_over_var is not None
        ):
            denom = np.sqrt(h1_over_var + h2_over_var)
            if denom != 0:
                overflow_comp = (h1_over - h2_over) / denom
    elif comparison == "asymmetry":
        if h1_under is not None and h2_under is not None and (h1_under + h2_under) != 0:
            underflow_comp = (h1_under - h2_under) / (h1_under + h2_under)
        if h1_over is not None and h2_over is not None and (h1_over + h2_over) != 0:
            overflow_comp = (h1_over - h2_over) / (h1_over + h2_over)
    elif comparison == "efficiency":
        if h1_under is not None and h2_under is not None and h2_under != 0:
            underflow_comp = h1_under / h2_under
        if h1_over is not None and h2_over is not None and h2_over != 0:
            overflow_comp = h1_over / h2_over

    if np.allclose(lower_uncertainties, upper_uncertainties, equal_nan=True):
        comparison_plottable = EnhancedPlottableHistogram(
            comparison_values,
            edges=h2_plottable.axes[0].edges,
            variances=lower_uncertainties**2,
            kind=h2_plottable.kind,
            w2method="sqrt",
            underflow=underflow_comp,
            overflow=overflow_comp,
        )
        histplot_kwargs.setdefault("w2method", "sqrt")
    else:
        comparison_plottable = EnhancedPlottableHistogram(
            comparison_values,
            edges=h2_plottable.axes[0].edges,
            yerr=[lower_uncertainties, upper_uncertainties],
            kind=h2_plottable.kind,
            w2method=h2_plottable.method,
            underflow=underflow_comp,
            overflow=overflow_comp,
        )
        histplot_kwargs.setdefault(
            "yerr", [comparison_plottable.yerr_lo, comparison_plottable.yerr_hi]
        )

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
    fig=None,
    ax_main=None,
    ax_comparison=None,
    plot_only=None,
    flow="hint",
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
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    plot_only : str, optional
        If "ax_main" or "ax_comparison", only the main or comparison axis is plotted on the figure. Both axes are plotted if None is specified, which is the default. This can only be used when fig, ax_main and ax_comparison are not provided by the user.
    flow : str, optional
        Whether to show under/overflow bins. Options: "show", "sum", "hint", "none". Default is "hint".
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

    # Convert input histograms to plottable histograms.
    # If the input is a function, it is left unchanged.
    data_hist_plottable = make_plottable_histogram(data_hist)
    stacked_components = [
        make_plottable_histogram(component) if not callable(component) else component
        for component in stacked_components
    ]
    unstacked_components = [
        make_plottable_histogram(component) if not callable(component) else component
        for component in unstacked_components
    ]

    # Create copies of the kwargs arguments passed as lists/dicts to avoid modifying them
    stacked_kwargs = stacked_kwargs.copy()
    unstacked_kwargs_list = unstacked_kwargs_list.copy()
    model_sum_kwargs = model_sum_kwargs.copy()

    comparison_kwargs.setdefault("h1_label", data_label)
    comparison_kwargs.setdefault("h2_label", "MC")
    comparison_kwargs.setdefault("comparison", "split_ratio")

    model_components = stacked_components + unstacked_components

    if len(model_components) == 0:
        msg = "Need to provide at least one model component."
        raise ValueError(msg)

    model_type = _get_model_type(model_components)

    if model_type == "histograms":
        _check_binning_consistency([*model_components, data_hist_plottable])
        for component in [*model_components, data_hist_plottable]:
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
        function_range=[
            data_hist_plottable.edges_1d()[0],
            data_hist_plottable.edges_1d()[-1],
        ],
        model_uncertainty=model_uncertainty,
        model_uncertainty_label=model_uncertainty_label,
        fig=fig,
        ax=ax_main,
        flow=flow,
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

    if plot_only == "ax_main":
        ax_main.set_xlabel(xlabel)
    else:
        _ = ax_main.xaxis.set_ticklabels([])
        ax_main.set_xlabel(" ")

    if model_type == "histograms":
        model_hist = sum(model_components)
        if not model_uncertainty:
            model_hist.set_variances(np.zeros_like(model_hist.variances()))
    else:

        def sum_components(x):
            return sum(f(x) for f in model_components)

        model_hist = _make_hist_from_function(sum_components, data_hist_plottable)

    if comparison_kwargs["comparison"] == "pull" and (
        model_type == "functions" or not model_uncertainty
    ):
        comparison_kwargs.setdefault(
            "comparison_ylabel",
            rf"$\frac{{ {comparison_kwargs['h1_label']} - {comparison_kwargs['h2_label']} }}{{ \sigma_{{{comparison_kwargs['h1_label']}}} }} $",
        )

    ax_main.legend()

    comparison(
        data_hist_plottable,
        model_hist,
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

    return fig, ax_main, ax_comparison
