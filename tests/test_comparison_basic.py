import boost_histogram as bh
import numpy as np
import pytest

from mplhep import get_comparison


def test_difference_simple_values():
    """
    Test difference with simple values.
    """
    bins = bh.axis.Regular(1, 1, 2, overflow=False, underflow=False)
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 100)
    h2 = bh.Histogram(bins, storage=bh.storage.Weight())
    h2.fill([1] * 50)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([12.24744871391589])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_uncertainty_type="poisson", comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([12.233780151938355])
    assert pytest.approx(low_uncertainty) == np.array([13.104772168594577])

    # No variances
    h1 = np.histogram([1] * 100, bins=[1, 2])
    h2 = np.histogram([1] * 50, bins=[1, 2])
    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variances
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 100)
    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])


def test_ratio_simple_values():
    """
    Test ratio with simple values.
    """
    bins = bh.axis.Regular(1, 1, 2, overflow=False, underflow=False)
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 10)
    h2 = bh.Histogram(bins, storage=bh.storage.Weight())
    h2.fill([1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.03316625])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_uncertainty_type="poisson", comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.03265575])
    assert pytest.approx(low_uncertainty) == np.array([0.04382563])

    # No variances
    h1 = np.histogram([1] * 10, bins=[1, 2])
    h2 = np.histogram([1] * 100, bins=[1, 2])
    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variances
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 10)
    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])


def test_split_ratio_simple_values():
    """
    Test split ratio with simple values.
    """
    bins = bh.axis.Regular(1, 1, 2, overflow=False, underflow=False)
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 10)
    h2 = bh.Histogram(bins, storage=bh.storage.Weight())
    h2.fill([1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.0316227766016838])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_uncertainty_type="poisson", comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.031086944386636207])
    assert pytest.approx(low_uncertainty) == np.array([0.04266949759891313])

    # No variances
    h1 = np.histogram([1] * 10, bins=[1, 2])
    h2 = np.histogram([1] * 100, bins=[1, 2])
    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_uncertainty_type="poisson", comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variances
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 10)
    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_uncertainty_type="poisson", comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])


def test_pull_simple_values():
    """
    Test pull with simple values.
    """
    bins = bh.axis.Regular(1, 1, 2, overflow=False, underflow=False)
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 50)
    h2 = bh.Histogram(bins, storage=bh.storage.Weight())
    h2.fill([1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="pull"
    )
    assert pytest.approx(values) == np.array([-4.08248290463863])
    assert pytest.approx(high_uncertainty) == np.array([1.0])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="pull", h1_uncertainty_type="poisson"
    )
    assert pytest.approx(values) == np.array([-3.8818568847803108])
    assert pytest.approx(high_uncertainty) == np.array([1.0])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    # No variances
    h1 = np.histogram([1] * 50, bins=[1, 2])
    h2 = np.histogram([1] * 100, bins=[1, 2])
    # will raise an error because no variances
    with pytest.raises(
        ValueError,
        match="Both histograms must have variances defined to compute the pull.",
    ):
        get_comparison(h1, h2, comparison="pull")

    # Variances and no variances
    h1 = bh.Histogram(bins, storage=bh.storage.Weight())
    h1.fill([1] * 50)
    with pytest.raises(
        ValueError,
        match="Both histograms must have variances defined to compute the pull.",
    ):
        get_comparison(h1, h2, comparison="pull")
