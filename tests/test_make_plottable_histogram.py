import os

import boost_histogram as bh
import hist
import numpy as np
import pytest
import uproot

from mplhep import EnhancedPlottableHistogram, make_plottable_histogram


@pytest.fixture
def data():
    """
    Pytest fixture that returns a dummy data list to be reused across multiple tests.
    """
    return [0.5] + [1.1, 1.9] + [2.1, 2.5, 2.9]  # noqa: RUF005


@pytest.fixture
def basic_hist():
    edges = np.array([[0, 1], [1, 2], [2, 3]])
    values = np.array([1.0, 2.0, 3.0])
    variances = values
    return EnhancedPlottableHistogram(values, edges=edges, variances=variances)


def test_make_plottable_histogram_from_numpy_hist(basic_hist, data):
    basic_hist.set_variances(None)  # Numpy histograms do not have variances

    bins = [0, 1, 2, 3]
    h_numpy = np.histogram(data, bins=bins)
    h_plottable = make_plottable_histogram(h_numpy)

    assert h_plottable == basic_hist


def test_make_plottable_histogram_from_boost_hist(basic_hist, data):
    bins = bh.axis.Regular(3, 0, 3)
    h_boost_histogram = bh.Histogram(bins)
    h_boost_histogram.fill(data)
    h_plottable = make_plottable_histogram(h_boost_histogram)

    assert h_plottable == basic_hist


def test_make_plottable_histogram_from_hist(basic_hist, data):
    bins = hist.axis.Regular(3, 0, 3)
    h_hist = hist.Hist(bins)
    h_hist.fill(data)
    h_plottable = make_plottable_histogram(h_hist)

    assert h_plottable == basic_hist


def test_make_plottable_histogram_from_uproot(basic_hist, data):
    filename = "_temp_test_make_plottable_histogram_from_uproot.root"
    bins = hist.axis.Regular(3, 0, 3)
    h = hist.Hist(bins)
    h.fill(data)

    with uproot.recreate(filename) as f:
        f["test_hist"] = h

    with uproot.open(filename) as f:
        h_uproot = f["test_hist"]

    h_plottable = make_plottable_histogram(h_uproot)

    os.remove(filename)

    assert h_plottable == basic_hist


def test_make_plottable_histogram_from_root_hist(basic_hist, data):
    ROOT = pytest.importorskip("ROOT")

    h_root = ROOT.TH1F("h1", "h1", 3, 0.0, 3.0)
    for value in data:
        h_root.Fill(value)

    h_plottable = make_plottable_histogram(h_root)

    assert h_plottable == basic_hist
