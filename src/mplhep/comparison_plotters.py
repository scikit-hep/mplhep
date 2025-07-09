"""
Collection of functions to plot histograms
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from .comparison import (
    _check_binning_consistency,
    get_comparison,
)
from .plot import (
    histplot,
)
from .utils import (
    EnhancedPlottableHistogram,
    _check_counting_histogram,
    _get_math_text,
    make_plottable_histogram,
)


def create_comparison_figure(
    figsize=(6, 5),
    nrows=2,
    gridspec_kw=None,
    hspace=0.15,
):
    """
    Create a figure with subplots for comparison.

    Parameters
    ----------
    figsize : tuple, optional
        Figure size in inches. Default is (6, 5).
    nrows : int, optional
        Number of rows in the subplot grid. Default is 2.
    gridspec_kw : dict, optional
        Additional keyword arguments for the GridSpec. Default is None.
        If None is provided, this is set to {"height_ratios": [4, 1]}.
    hspace : float, optional
        Height spacing between subplots. Default is 0.15.


    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure.
    axes : ndarray
        Array of Axes objects representing the subplots.

    """
    if gridspec_kw is None:
        gridspec_kw = {"height_ratios": [4, 1]}
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]

    fig, axes = plt.subplots(nrows=nrows, figsize=figsize, gridspec_kw=gridspec_kw)
    if nrows > 1:
        fig.subplots_adjust(hspace=hspace)

    for ax in axes[:-1]:
        _ = ax.xaxis.set_ticklabels([])

    return fig, axes


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
        fig, (ax_main, ax_comparison) = create_comparison_figure()
    elif fig is None or ax_main is None or ax_comparison is None:
        raise ValueError(
            "Need to provide fig, ax_main and ax_comparison (or none of them)."
        )

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

    if comparison == "pull":
        histplot_kwargs.setdefault("histtype", "fill")
        histplot_kwargs.setdefault("color", "darkgrey")
        histplot(comparison_plottable, ax=ax, **histplot_kwargs)
    else:
        histplot_kwargs.setdefault("color", "black")
        histplot_kwargs.setdefault("histtype", "errorbar")
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
            with np.errstate(divide="ignore", invalid="ignore"):
                h2_scaled_uncertainties = np.where(
                    h2_plottable.values() != 0,
                    np.sqrt(h2_plottable.variances()) / h2_plottable.values(),
                    np.nan,
                )
            ax.bar(
                x=h2_plottable.axes[0].centers,
                bottom=np.nan_to_num(
                    bottom_shift - h2_scaled_uncertainties, nan=comparison_ylim[0]
                ),
                height=np.nan_to_num(
                    2 * h2_scaled_uncertainties,
                    nan=comparison_ylim[-1] - comparison_ylim[0],
                ),
                width=h2_plottable.axes[0].widths,
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
