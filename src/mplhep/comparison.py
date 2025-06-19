import numpy as np

from .utils import (
    EnhancedPlottableHistogram,
    _check_counting_histogram,
    make_plottable_histogram,
)


def _check_binning_consistency(hist_list):  # TODO: test
    """
    Check that all the histograms in the provided list share the same definition of their bins.

    Parameters
    ----------
    hist_list : list of histograms

    Raise
    -----
    ValueError
        If the histograms do not share the same dimensionality or if their bins are not equal.

    """
    for h in hist_list:
        if len(h.axes) != len(hist_list[0].axes):
            msg = "Histograms must have same dimensionality."
            raise ValueError(msg)
        for i in range(len(h.axes)):
            if h.axes[i] != hist_list[0].axes[i]:
                msg = "The bins of the histograms must be equal."
                raise ValueError(msg)


def get_difference(h1, h2, h1_w2method="sqrt"):
    """
    Compute the difference between two histograms.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
    h1_w2method : str, optional
        What kind of bin uncertainty to use for h1: "sqrt" for the Poisson standard deviation derived from the variance stored in the histogram object, "poisson" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "sqrt".

    Returns
    -------
    difference_values : numpy.ndarray
        The difference values.
    difference_uncertainties_low : numpy.ndarray
        The lower uncertainties on the difference.
    difference_uncertainties_high : numpy.ndarray
        The upper uncertainties on the difference.
    """

    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram([h1_plottable, h2_plottable])

    h1_plottable.method = h1_w2method
    h2_plottable.method = (
        h1_w2method  # Does not matter for difference, but keeps consistency
    )

    h_diff = h1_plottable + -1 * h2_plottable

    h1_plottable.errors()

    if h1_plottable.variances() is None or h2_plottable.variances() is None:
        return (
            h_diff.values(),
            np.zeros_like(h_diff.values()),
            np.zeros_like(h_diff.values()),
        )

    if h1_w2method == "poisson":
        uncertainties_low, uncertainties_high = (
            h1_plottable.yerr_lo,
            h1_plottable.yerr_hi,
        )

        difference_uncertainties_low = np.sqrt(
            uncertainties_low**2 + h2_plottable.variances()
        )
        difference_uncertainties_high = np.sqrt(
            uncertainties_high**2 + h2_plottable.variances()
        )

    else:
        h_diff.method = "sqrt"
        h_diff.errors()
        difference_uncertainties_low, difference_uncertainties_high = (
            h_diff.yerr_lo,
            h_diff.yerr_hi,
        )

    return (
        h_diff.values(),
        difference_uncertainties_low,
        difference_uncertainties_high,
    )


def get_ratio_variances(h1, h2):
    """
    Calculate the variances of the ratio of two uncorrelated histograms (h1/h2).

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The first histogram.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The second histogram.

    Returns
    -------
    ratio_variances : np.ndarray
        The variances of the ratio of the two histograms.

    Raises
    ------
    ValueError
        If the bins of the histograms are not equal.
    """
    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram([h1_plottable, h2_plottable])

    np.seterr(divide="ignore", invalid="ignore")
    ratio_variances = np.where(
        h2_plottable.values() != 0,
        h1_plottable.variances() / h2_plottable.values() ** 2
        + h2_plottable.variances()
        * h1_plottable.values() ** 2
        / h2_plottable.values() ** 4,
        np.nan,
    )
    np.seterr(divide="warn", invalid="warn")

    return ratio_variances


def get_ratio(
    h1,
    h2,
    h1_w2method="sqrt",
    ratio_uncertainty_type="uncorrelated",
):
    """
    Compute the ratio h1/h2 between two uncorrelated histograms h1 and h2.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The numerator histogram.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The denominator histogram.
    h1_w2method : str, optional
        What kind of bin uncertainty to use for h1: "sqrt" for the Poisson standard deviation derived from the variance stored in the histogram object, "poisson" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "sqrt".
    ratio_uncertainty_type : str, optional
        How to treat the uncertainties of the histograms:
        * "uncorrelated" for the comparison of two uncorrelated histograms,
        * "split" for scaling down the uncertainties of h1 by bin contents of h2, i.e. assuming zero uncertainty coming from h2 in the ratio uncertainty.
        Default is "uncorrelated".

    Returns
    -------
    ratio_values : numpy.ndarray
        The ratio values.
    ratio_uncertainties_low : numpy.ndarray
        The lower uncertainties on the ratio.
    ratio_uncertainties_high : numpy.ndarray
        The upper uncertainties on the ratio.

    Raises
    ------
    ValueError
        If the ratio_uncertainty_type is not valid.
    """

    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram([h1_plottable, h2_plottable])

    ratio_values = np.where(
        h2_plottable.values() != 0,
        h1_plottable.values() / h2_plottable.values(),
        np.nan,
    )

    h1_plottable.method = h1_w2method
    h2_plottable.method = "sqrt"

    h1_plottable.errors()

    if h1_plottable.variances() is None or h2_plottable.variances() is None:
        return (
            ratio_values,
            np.zeros_like(h1_plottable.values()),
            np.zeros_like(h1_plottable.values()),
        )

    uncertainties_low, uncertainties_high = h1_plottable.yerr_lo, h1_plottable.yerr_hi

    if ratio_uncertainty_type == "uncorrelated":
        if h1_w2method == "poisson":
            h1_plottable_high = EnhancedPlottableHistogram(
                h1_plottable.values(),
                edges=h1_plottable.axes[0].edges,
                variances=uncertainties_high**2,
                kind=h1_plottable.kind,
                w2method=h1_plottable.method,
            )
            h1_plottable_low = EnhancedPlottableHistogram(
                h1_plottable.values(),
                edges=h1_plottable.axes[0].edges,
                variances=uncertainties_low**2,
                kind=h1_plottable.kind,
                w2method=h1_plottable.method,
            )
            ratio_uncertainties_low = np.sqrt(
                get_ratio_variances(h1_plottable_low, h2_plottable)
            )
            ratio_uncertainties_high = np.sqrt(
                get_ratio_variances(h1_plottable_high, h2_plottable)
            )
        else:
            ratio_uncertainties_low = np.sqrt(
                get_ratio_variances(h1_plottable, h2_plottable)
            )
            ratio_uncertainties_high = ratio_uncertainties_low

    elif ratio_uncertainty_type == "split":
        if h1_w2method == "poisson":
            ratio_uncertainties_low = uncertainties_low / h2_plottable.values()
            ratio_uncertainties_high = uncertainties_high / h2_plottable.values()

        else:
            h1_scaled_uncertainties = np.where(
                h2_plottable.values() != 0,
                np.sqrt(h1_plottable.variances()) / h2_plottable.values(),
                np.nan,
            )
            ratio_uncertainties_low = h1_scaled_uncertainties
            ratio_uncertainties_high = ratio_uncertainties_low
    else:
        msg = "ratio_uncertainty_type must be one of ['uncorrelated', 'split']."
        raise ValueError(msg)

    return (
        ratio_values,
        ratio_uncertainties_low,
        ratio_uncertainties_high,
    )


def get_pull(h1, h2, h1_w2method="sqrt"):
    """
    Compute the pull between two histograms.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The first histogram.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The second histogram.
    h1_w2method : str, optional
        What kind of bin uncertainty to use for h1: "sqrt" for the Poisson standard deviation derived from the variance stored in the histogram object, "poisson" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "sqrt".

    Returns
    -------
    pull_values : numpy.ndarray
        The pull values.
    pull_uncertainties_low : numpy.ndarray
        The lower uncertainties on the pull. Always ones.
    pull_uncertainties_high : numpy.ndarray
        The upper uncertainties on the pull. Always ones.
    """
    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram([h1_plottable, h2_plottable])

    if h1_plottable.variances() is None or h2_plottable.variances() is None:
        msg = "Both histograms must have variances defined to compute the pull."
        raise ValueError(msg)

    h1_plottable.method = h1_w2method
    h2_plottable.method = "sqrt"

    if h1_plottable.method == "poisson":
        h1_plottable.errors()

        h1_variances = np.where(
            h1_plottable.values() >= h2_plottable.values(),
            h1_plottable.yerr_lo**2,
            h1_plottable.yerr_hi**2,
        )
    else:
        h1_variances = h1_plottable.variances()

    pull_values = np.where(
        h1_variances + h2_plottable.variances() != 0,
        (h1_plottable.values() - h2_plottable.values())
        / np.sqrt(h1_variances + h2_plottable.variances()),
        np.nan,
    )
    pull_uncertainties_low = np.ones_like(pull_values)
    pull_uncertainties_high = pull_uncertainties_low

    return (
        pull_values,
        pull_uncertainties_low,
        pull_uncertainties_high,
    )


def get_asymmetry(h1, h2):
    """
    Get the asymmetry between two histograms h1 and h2, defined as (h1 - h2) / (h1 + h2).
    Only symmetrical uncertainties are supported.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The first histogram.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The second histogram.

    Returns
    -------
    asymmetry_values : numpy.ndarray
        The asymmetry values.
    asymmetry_uncertainties : numpy.ndarray
        The uncertainties on the asymmetry.
    """
    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram([h1_plottable, h2_plottable])

    hist_sum = h1_plottable + h2_plottable
    hist_diff = h1_plottable + (-1 * h2_plottable)
    asymmetry_values = np.where(
        hist_sum.values() != 0, hist_diff.values() / hist_sum.values(), np.nan
    )

    if h1_plottable.variances() is None or h2_plottable.variances() is None:
        return (
            asymmetry_values,
            np.zeros_like(asymmetry_values),
        )

    asymmetry_variances = get_ratio_variances(hist_diff, hist_sum)

    return (
        asymmetry_values,
        np.sqrt(asymmetry_variances),
    )


def get_efficiency(h1, h2):
    """
    Calculate the ratio of two correlated histograms (h1/h2), in which the entries of h1 are a subsample of the entries of h2.
    The variances are calculated according to the formula given in :ref:`documentation-statistics-label`.

    The following conditions must be fulfilled for the calculation of the efficiency:
    * The bins of the histograms must be equal.
    * The histograms must be unweighted.
    * The bin contents of both histograms must be positive or zero.
    * The bin contents of h1 must be a subsample of the bin contents of h2.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The first histogram.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The second histogram.

    Returns
    -------
    efficiency_values : numpy.ndarray
        The efficiency values.
    efficiency_uncertainties : numpy.ndarray
        The uncertainties on the efficiency values.

    Raises
    ------
    ValueError
        If the histograms are weighted.
    ValueError
        If the bin contents of the histograms are not positive or zero.
    ValueError
        If the bin contents of h1 are not a subsample of the bin contents of h2.
    """
    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram([h1_plottable, h2_plottable])

    if not (h1_plottable.is_unweighted() and h2_plottable.is_unweighted()):
        msg = "The ratio of two correlated histograms (efficiency) can only be computed for unweighted histograms."
        raise ValueError(msg)
    if not (np.all(h1_plottable.values() >= 0) and np.all(h2_plottable.values() >= 0)):
        msg = "The ratio of two correlated histograms (efficiency) can only be computed if the bin contents of both histograms are positive or zero."
        raise ValueError(msg)
    if not np.all(h1_plottable.values() <= h2_plottable.values()):
        msg = "The ratio of two correlated histograms (efficiency) can only be computed if the bin contents of h1 are a subsample of the bin contents of h2."
        raise ValueError(msg)

    efficiency_values = np.where(
        h2_plottable.values() != 0,
        h1_plottable.values() / h2_plottable.values(),
        np.nan,
    )

    k = h1_plottable.values()
    n = h2_plottable.values()

    efficiency_variances = (k + 1) * (k + 2) / (n + 2) / (n + 3) - (k + 1) ** 2 / (
        n + 2
    ) ** 2

    return efficiency_values, np.sqrt(efficiency_variances)


def get_comparison(
    h1,
    h2,
    comparison,
    h1_w2method="sqrt",
):
    """
    Compute the comparison between two histograms.

    Parameters
    ----------
    h1 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The first histogram for comparison.
    h2 : histogram (e.g. Hist, boost_histogram, np.histogram, TH1)
        The second histogram for comparison.
    comparison : str
        The type of comparison ("ratio", "split_ratio", "pull", "difference", "relative_difference", "efficiency", or "asymmetry").
        When the `split_ratio` option is used, the uncertainties of h1 are scaled down by the bin contents of h2, i.e. assuming zero uncertainty coming from h2 in the ratio uncertainty.
    h1_w2method : str, optional
        What kind of bin uncertainty to use for h1: "sqrt" for the Poisson standard deviation derived from the variance stored in the histogram object, "poisson" for asymmetrical uncertainties based on a Poisson confidence interval. Default is "sqrt".
        Asymmetrical uncertainties are not supported for the asymmetry and efficiency comparisons.

    Returns
    -------
    values : numpy.ndarray
        The comparison values.
    lower_uncertainties : numpy.ndarray
        The lower uncertainties on the comparison values.
    upper_uncertainties : numpy.ndarray
        The upper uncertainties on the comparison values.

    Raises
    ------
    ValueError
        If the comparison is not valid.
    ValueError
        If h1_w2method is not one of ["sqrt", "poisson"].
    ValueError
        If the h1_w2method is "poisson" and the comparison is "asymmetry" or "efficiency".
    """

    h1_plottable = make_plottable_histogram(h1)
    h2_plottable = make_plottable_histogram(h2)

    if h1_w2method not in ["sqrt", "poisson"]:
        msg = f"h1_w2method must be one of ['sqrt', 'poisson'], got {h1_w2method}."
        raise ValueError(msg)

    _check_binning_consistency([h1_plottable, h2_plottable])
    _check_counting_histogram([h1_plottable, h2_plottable])

    np.seterr(divide="ignore", invalid="ignore")

    if comparison == "ratio":
        values, lower_uncertainties, upper_uncertainties = get_ratio(
            h1_plottable, h2_plottable, h1_w2method, "uncorrelated"
        )
    elif comparison == "split_ratio":
        values, lower_uncertainties, upper_uncertainties = get_ratio(
            h1_plottable, h2_plottable, h1_w2method, "split"
        )
    elif comparison == "relative_difference":
        values, lower_uncertainties, upper_uncertainties = get_ratio(
            h1_plottable, h2_plottable, h1_w2method, "uncorrelated"
        )
        values -= 1  # relative difference is ratio-1
    elif comparison == "pull":
        values, lower_uncertainties, upper_uncertainties = get_pull(
            h1_plottable, h2_plottable, h1_w2method
        )
    elif comparison == "difference":
        values, lower_uncertainties, upper_uncertainties = get_difference(
            h1_plottable, h2_plottable, h1_w2method
        )
    elif comparison == "asymmetry":
        if h1_w2method == "poisson":
            msg = "Poisson asymmetrical uncertainties are not supported for the asymmetry comparison."
            raise ValueError(msg)
        values, uncertainties = get_asymmetry(h1_plottable, h2_plottable)
        lower_uncertainties = uncertainties
        upper_uncertainties = uncertainties
    elif comparison == "efficiency":
        if h1_w2method == "poisson":
            msg = "Poisson asymmetrical uncertainties are not supported for the efficiency comparison."
            raise ValueError(msg)
        values, uncertainties = get_efficiency(h1_plottable, h2_plottable)
        lower_uncertainties = uncertainties
        upper_uncertainties = uncertainties
    else:
        msg = f"{comparison} not available as a comparison ('ratio', 'split_ratio', 'pull', 'difference', 'relative_difference', 'asymmetry' or 'efficiency')."
        raise ValueError(msg)
    np.seterr(divide="warn", invalid="warn")

    return values, lower_uncertainties, upper_uncertainties
