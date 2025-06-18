import numpy as np

from .utils import _check_counting_histogram, make_plottable_histogram


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


def get_difference(h1, h2, h1_uncertainty_type="sqrt"):
    """
    Compute the difference between two histograms.

    Parameters
    ----------
    h1 : histogram
    h2 : histogram
    h1_uncertainty_type : str, optional
        What kind of bin uncertainty to use for h1: "sqrt" for symmetrical uncertainties, "poisson" for asymmetrical uncertainties.

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
    _check_counting_histogram(h1_plottable)
    _check_counting_histogram(h2_plottable)

    h1_plottable.method = h1_uncertainty_type

    h_diff = h1_plottable + -1 * h2_plottable

    h1_plottable.errors()

    if h1_plottable.variances() is None or h2_plottable.variances() is None:
        return (
            h_diff.values(),
            np.zeros_like(h_diff.values()),
            np.zeros_like(h_diff.values()),
        )

    if h1_uncertainty_type == "poisson":
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
