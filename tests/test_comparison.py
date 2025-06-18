import boost_histogram as bh
import numpy as np
import pytest

from mplhep import get_difference

# Difference


def test_difference_simple_values():
    """
    Test difference with simple values.
    """
    bins = bh.axis.Regular(1, 1, 2, overflow=False, underflow=False)
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
    h1 = np.histogram([1] * 100, bins=[1, 2])
    h2 = np.histogram([1] * 50, bins=[1, 2])
    values, high_uncertainty, low_uncertainty = get_difference(h1, h2)
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variance
    h1 = bh.Histogram(bins)
    h1.fill([1] * 100)
    values, high_uncertainty, low_uncertainty = get_difference(h1, h2)
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])
