"""
Collection of functions to plot histograms
"""

from __future__ import annotations

import re

import matplotlib.pyplot as plt
import numpy as np

from .comparison_functions import (
    _check_binning_consistency,
    get_comparison,
)
from .plot import (
    funcplot,
    histplot,
)
from .utils import (
    EnhancedPlottableHistogram,
    _check_counting_histogram,
    make_plottable_histogram,
    set_fitting_ylabel_fontsize,
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


def plot_two_hist_comparison(
    h1,
    h2,
    xlabel=None,
    ylabel=None,
    h1_label="h1",
    h2_label="h2",
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
    fig : matplotlib.figure.Figure or None, optional
        The figure to use for the plot. If fig, ax_main and ax_comparison are None, a new figure will be created. Default is None.
    ax_main : matplotlib.axes.Axes or None, optional
        The main axes for the histogram comparison. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    ax_comparison : matplotlib.axes.Axes or None, optional
        The axes for the comparison plot. If fig, ax_main and ax_comparison are None, a new axes will be created. Default is None.
    **comparison_kwargs : optional
        Arguments to be passed to plot_comparison(), including the choice of the comparison function and the treatment of the uncertainties (see documentation of plot_comparison() for details).

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
    plot_comparison : Plot the comparison between two histograms.

    """
    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram(h1_plottable)
    _check_counting_histogram(h2_plottable)

    if fig is None and ax_main is None and ax_comparison is None:
        fig, (ax_main, ax_comparison) = plt.subplots(
            nrows=2, figsize=(6, 5), gridspec_kw={"height_ratios": [4, 1]}
        )
        fig.subplots_adjust(hspace=0.15)
        ax_main.xaxis.set_ticklabels([])
        ax_main.set_xlabel(" ")
    elif fig is None or ax_main is None or ax_comparison is None:
        msg = "Need to provide fig, ax_main and ax_comparison (or none of them)."
        raise ValueError(msg)

    xlim = (h1_plottable.edges_1d()[0], h1_plottable.edges_1d()[-1])

    histplot(h1_plottable, ax=ax_main, label=h1_label, histtype="step")
    histplot(h2_plottable, ax=ax_main, label=h2_label, histtype="step")
    ax_main.set_xlim(xlim)
    ax_main.set_ylabel(ylabel)
    ax_main.legend()
    _ = ax_main.xaxis.set_ticklabels([])

    plot_comparison(
        h1_plottable,
        h2_plottable,
        ax_comparison,
        xlabel=xlabel,
        h1_label=h1_label,
        h2_label=h2_label,
        **comparison_kwargs,
    )

    fig.align_ylabels()

    return fig, ax_main, ax_comparison


def plot_comparison(
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
    **histplot_kwargs : optional
        Arguments to be passed to histplot(), called in case the comparison is "pull", or plot_error_hist(), called for every other comparison case. In the former case, the default arguments are histtype="stepfilled" and color="darkgrey". In the later case, the default argument is color="black".

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the plotted comparison.

    See Also
    --------
    plot_two_hist_comparison : Compare two histograms and plot the comparison.

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

    if np.allclose(lower_uncertainties, upper_uncertainties, equal_nan=True):
        comparison_plottable = EnhancedPlottableHistogram(
            comparison_values,
            edges=h2_plottable.axes[0].edges,
            variances=lower_uncertainties**2,
            kind=h2_plottable.kind,
            w2method=h2_plottable.method,
        )
    else:
        comparison_plottable = EnhancedPlottableHistogram(
            comparison_values,
            edges=h2_plottable.axes[0].edges,
            yerr=[lower_uncertainties, upper_uncertainties],
            kind=h2_plottable.kind,
            w2method=h2_plottable.method,
        )

    comparison_plottable.errors()

    if comparison == "pull":
        histplot_kwargs.setdefault("histtype", "fill")
        histplot_kwargs.setdefault("color", "darkgrey")
        histplot(comparison_plottable, ax=ax, **histplot_kwargs)
    else:
        histplot_kwargs.setdefault("color", "black")
        histplot_kwargs.setdefault("histtype", "errorbar")
        histplot_kwargs.setdefault("yerr", comparison_plottable.yerr)
        histplot(comparison_plottable, ax=ax, **histplot_kwargs)

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


def _get_model_type(components):
    """
    Check that all components of a model are either all histograms or all functions
    and return the type of the model components.

    Parameters
    ----------
    components : list
        The list of model components.

    Returns
    -------
    str
        The type of the model components ("histograms" or "functions").

    Raises
    ------
    ValueError
        If the model components are not all histograms or all functions.
    """
    if all(callable(x) for x in components):
        return "functions"
    return "histograms"


def plot_model(
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
    model_uncertainty_label="Model stat. unc.",
    fig=None,
    ax=None,
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
        The label for the model uncertainties. Default is "Model stat. unc.".
    fig : matplotlib.figure.Figure or None, optional
        The Figure object to use for the plot. Create a new one if none is provided.
    ax : matplotlib.axes.Axes or None, optional
        The Axes object to use for the plot. Create a new one if none is provided.


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
                **stacked_kwargs,
            )
            if model_uncertainty and len(unstacked_components) == 0:
                histplot(
                    sum(stacked_components),
                    ax=ax,
                    label=model_uncertainty_label,
                    histtype="band",
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
                histplot(
                    sum(components),
                    ax=ax,
                    histtype="step",
                    **model_sum_kwargs,
                )
                if model_uncertainty:
                    histplot(
                        sum(components),
                        ax=ax,
                        label=model_uncertainty_label,
                        histtype="band",
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
                sum(components), ax=ax, label=model_uncertainty_label, histtype="band"
            )

    ax.set_xlim(xlim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    set_fitting_ylabel_fontsize(ax)
    ax.legend()

    return fig, ax


def _make_hist_from_function(func, ref_hist):
    """
    Create a histogram from a function and a reference histogram.
    The returned histogram has the same binning as the reference histogram and
    is filled with the function evaluated at the bin centers of the reference histogram.

    Parameters
    ----------
    func : function
        1D function. The function should support vectorization (i.e. accept a numpy array as input).
    ref_hist : boost_histogram.Histogram
        The reference 1D histogram to use for the binning.

    Returns
    -------
    hist : boost_histogram.Histogram
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


def plot_data_model_comparison(
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
    model_uncertainty_label="Model stat. unc.",
    data_w2method="poisson",
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
        The label for the model uncertainties. Default is "Model stat. unc.".
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
    **comparison_kwargs : optional
        Arguments to be passed to plot_comparison(), including the choice of the comparison function and the treatment of the uncertainties (see documentation of plot_comparison() for details). If they are not provided explicitly, the following arguments are passed by default: h1_label="Data", h2_label="Pred.", comparison="split_ratio".

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
    plot_comparison : Plot the comparison between two histograms.

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
    comparison_kwargs.setdefault("h2_label", "Pred.")
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
            fig, (ax_main, ax_comparison) = plt.subplots(
                nrows=2, figsize=(6, 5), gridspec_kw={"height_ratios": [4, 1]}
            )
            fig.subplots_adjust(hspace=0.15)
            ax_main.xaxis.set_ticklabels([])
            ax_main.set_xlabel(" ")
        elif plot_only == "ax_main":
            fig, ax_main = plt.subplots()
            _, ax_comparison = plt.subplots()
        elif plot_only == "ax_comparison":
            fig, ax_comparison = plt.subplots()
            _, ax_main = plt.subplots()
        else:
            msg = "plot_only must be 'ax_main', 'ax_comparison' or None."
            raise ValueError(msg)
    elif fig is None or ax_main is None or ax_comparison is None:
        msg = "Need to provide fig, ax_main and ax_comparison (or none of them)."
        raise ValueError(msg)
    elif plot_only is not None:
        msg = "Cannot provide fig, ax_main or ax_comparison with plot_only."
        raise ValueError(msg)

    plot_model(
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
    )

    histplot(
        data_hist_plottable,
        ax=ax_main,
        w2method=data_w2method,
        color="black",
        label=data_label,
        histtype="errorbar",
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

    plot_comparison(
        data_hist_plottable,
        model_hist,
        ax=ax_comparison,
        xlabel=xlabel,
        w2method=data_w2method,
        **comparison_kwargs,
    )

    ylabel_fontsize = set_fitting_ylabel_fontsize(ax_main)
    ax_comparison.get_yaxis().get_label().set_size(ylabel_fontsize)

    fig.align_ylabels()

    return fig, ax_main, ax_comparison
