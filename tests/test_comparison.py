import boost_histogram as bh
import numpy as np
import pytest

from mplhep import EnhancedPlottableHistogram, get_difference


def test_difference_simple_values():
    """
    Test difference with simple values.
    """

    # h1 = make_hist(data=[1] * 50, bins=1, range=(0, 3))
    # h2 = make_hist(data=[1] * 100, bins=1, range=(0, 3))
    # h1 = EnhancedPlottableHistogram(
    #     np.array([100]), edges=np.array([0, 1]), variances=np.array([100])
    # )
    # h2 = EnhancedPlottableHistogram(
    #     np.array([50]), edges=np.array([0, 1]), variances=np.array([50])
    # )
    bins = bh.axis.Regular(1, 0, 2)
    h1 = bh.Histogram(bins)
    h1.fill([1] * 100)
    h2 = bh.Histogram(bins)
    h2.fill([1] * 50)

    values, high_uncertainty, low_uncertainty = get_difference(
        h1, h2, h1_uncertainty_type="sqrt"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([12.24744871391589])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_difference(
        h1, h2, h1_uncertainty_type="poisson"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([12.233780151938355])
    assert pytest.approx(low_uncertainty) == np.array([13.104772168594577])

    # No variances
    h1 = EnhancedPlottableHistogram(np.array([100]), edges=np.array([0, 1]))
    h2 = EnhancedPlottableHistogram(np.array([50]), edges=np.array([0, 1]))
    values, high_uncertainty, low_uncertainty = get_difference(h1, h2)
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])
