import re

import boost_histogram as bh
import numpy as np
import pytest

from mplhep import get_comparison


@pytest.fixture
def setup_bh_histograms():
    """
    Fixture factory to create histograms with custom fills.
    """

    def _create(h1_fill=None, h2_fill=None):
        bins = bh.axis.Regular(1, 1, 2, overflow=False, underflow=False)
        h1 = bh.Histogram(bins, storage=bh.storage.Weight())
        h2 = bh.Histogram(bins, storage=bh.storage.Weight())
        if h1_fill is not None:
            h1.fill(h1_fill)
        if h2_fill is not None:
            h2.fill(h2_fill)
        return h1, h2

    return _create


@pytest.fixture
def setup_np_histograms():
    """
    Fixture factory to create numpy histograms with custom fills.
    """

    def _create(h1_fill=None, h2_fill=None):
        bins = [1, 2]
        h1 = (
            np.histogram(h1_fill, bins=bins)
            if h1_fill is not None
            else np.histogram([], bins=bins)
        )
        h2 = (
            np.histogram(h2_fill, bins=bins)
            if h2_fill is not None
            else np.histogram([], bins=bins)
        )
        return h1, h2

    return _create


# --- Difference ---


def test_difference_simple_values(setup_bh_histograms, setup_np_histograms):
    """
    Test difference with simple values.
    """
    h1, h2 = setup_bh_histograms(h1_fill=[1] * 100, h2_fill=[1] * 50)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([12.24744871391589])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_w2method="poisson", comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([12.233780151938355])
    assert pytest.approx(low_uncertainty) == np.array([13.104772168594577])

    # No variances
    h1, h2 = setup_np_histograms(h1_fill=[1] * 100, h2_fill=[1] * 50)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variances
    h1, _ = setup_bh_histograms(h1_fill=[1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="difference"
    )
    assert pytest.approx(values) == np.array([50.0])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])


# --- Ratio ---


def test_ratio_simple_values(setup_bh_histograms, setup_np_histograms):
    """
    Test ratio with simple values.
    """
    h1, h2 = setup_bh_histograms(h1_fill=[1] * 10, h2_fill=[1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.03316625])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_w2method="poisson", comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.03265575])
    assert pytest.approx(low_uncertainty) == np.array([0.04382563])

    # No variances
    h1, h2 = setup_np_histograms(h1_fill=[1] * 10, h2_fill=[1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variances
    h1, _ = setup_bh_histograms(h1_fill=[1] * 10)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])


# --- Split Ratio ---


def test_split_ratio_simple_values(setup_bh_histograms, setup_np_histograms):
    """
    Test split ratio with simple values.
    """
    h1, h2 = setup_bh_histograms(h1_fill=[1] * 10, h2_fill=[1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.0316227766016838])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_w2method="poisson", comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.031086944386636207])
    assert pytest.approx(low_uncertainty) == np.array([0.04266949759891313])

    # No variances
    h1, h2 = setup_np_histograms(h1_fill=[1] * 10, h2_fill=[1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_w2method="poisson", comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variances
    h1, _ = setup_bh_histograms(h1_fill=[1] * 10)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, h1_w2method="poisson", comparison="split_ratio"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])


# --- Pull ---


def test_pull_simple_values(setup_bh_histograms, setup_np_histograms):
    """
    Test pull with simple values.
    """
    h1, h2 = setup_bh_histograms(h1_fill=[1] * 50, h2_fill=[1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="pull"
    )
    assert pytest.approx(values) == np.array([-4.08248290463863])
    assert pytest.approx(high_uncertainty) == np.array([1.0])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="pull", h1_w2method="poisson"
    )
    assert pytest.approx(values) == np.array([-3.8818568847803108])
    assert pytest.approx(high_uncertainty) == np.array([1.0])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    # No variances
    h1, h2 = setup_np_histograms(h1_fill=[1] * 50, h2_fill=[1] * 100)

    # will raise an error because no variances
    with pytest.raises(
        ValueError,
        match="Both histograms must have variances defined to compute the pull.",
    ):
        get_comparison(h1, h2, comparison="pull")

    # Variances and no variances
    h1, _ = setup_bh_histograms(h1_fill=[1] * 50)

    with pytest.raises(
        ValueError,
        match="Both histograms must have variances defined to compute the pull.",
    ):
        get_comparison(h1, h2, comparison="pull")


# --- Asymmetry ---


def test_asymmetry_simple_values(setup_bh_histograms, setup_np_histograms):
    """
    Test asymmetry with simple values.
    """
    h1, h2 = setup_bh_histograms(h1_fill=[1] * 100, h2_fill=[1] * 50)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="asymmetry"
    )
    assert pytest.approx(values) == np.array([0.3333333333333333])
    assert pytest.approx(high_uncertainty) == np.array([0.08606629658238704])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    # No variances
    h1, h2 = setup_np_histograms(h1_fill=[1] * 100, h2_fill=[1] * 50)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="asymmetry"
    )
    assert pytest.approx(values) == np.array([0.3333333333333333])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])

    # Variances and no variances
    h1, _ = setup_bh_histograms(h1_fill=[1] * 100)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h1, h2, comparison="asymmetry"
    )
    assert pytest.approx(values) == np.array([0.3333333333333333])
    assert pytest.approx(high_uncertainty) == np.array([0])
    assert pytest.approx(low_uncertainty) == np.array([0])


# --- Efficiency ---


def test_efficiency_subsample():
    """
    Test subsample error.
    """
    h1 = bh.Histogram(
        bh.axis.Regular(100, -5, 5, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h1.fill(np.random.normal(size=11))
    h2 = bh.Histogram(
        bh.axis.Regular(100, -5, 5, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h2.fill(np.random.normal(size=100))
    with pytest.raises(
        ValueError,
        match=re.escape(
            "The ratio of two correlated histograms (efficiency) can only be computed if the bin contents of h1 are a subsample of the bin contents of h2."
        ),
    ):
        get_comparison(h1, h2, comparison="efficiency")


def test_efficiency_no_variances(setup_np_histograms):
    """
    Test efficiency with no variances.
    """
    h1, h2 = setup_np_histograms(h1_fill=[1] * 10, h2_fill=[1] * 100)

    with pytest.raises(
        RuntimeError,
        match="Variances are not set, cannot determine if histogram is unweighted.",
    ):
        get_comparison(h1, h2, comparison="efficiency")


def simple_efficiency_uncertainty(total, sample):
    """
    Calculate the uncertainty of the efficiency of a sample, derived from the Binomial Statistics.
    """
    efficiency = sample / total
    return np.sqrt(efficiency * (1 - efficiency) / total)


def test_efficiency_simple_values():
    """
    Test efficiency with simple values.
    """
    n1 = 100
    n2 = 10

    h1 = bh.Histogram(
        bh.axis.Regular(1, 0, 2, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h1.fill([1] * n1)
    h2 = bh.Histogram(
        bh.axis.Regular(1, 0, 2, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h2.fill([1] * n2)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )
    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([0.03056316])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    assert pytest.approx(high_uncertainty[0], 0.02) == simple_efficiency_uncertainty(
        n1, n2
    )  # 0.02 relative error
    assert pytest.approx(low_uncertainty[0], 0.02) == simple_efficiency_uncertainty(
        n1, n2
    )  # 0.02 relative error

    # Test with larger numbers
    n1 = 10000000
    n2 = 1000000

    h1 = bh.Histogram(
        bh.axis.Regular(1, 0, 2, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h1.fill([1] * n1)
    h2 = bh.Histogram(
        bh.axis.Regular(1, 0, 2, overflow=False, underflow=False),
        storage=bh.storage.Weight(),
    )
    h2.fill([1] * n2)

    values, high_uncertainty, low_uncertainty = get_comparison(
        h2, h1, comparison="efficiency"
    )

    assert pytest.approx(values) == np.array([0.1])
    assert pytest.approx(high_uncertainty) == np.array([9.48683493e-05])
    assert pytest.approx(low_uncertainty) == high_uncertainty

    assert pytest.approx(high_uncertainty[0]) == simple_efficiency_uncertainty(
        n1, n2
    )  # 1e-6 relative error by default
    assert pytest.approx(low_uncertainty[0]) == simple_efficiency_uncertainty(
        n1, n2
    )  # 1e-6 relative error by default
