"""
Tests for issue #511: Add mplhep.hist() function to match plt.hist() API.

https://github.com/scikit-hep/mplhep/issues/511
"""

from __future__ import annotations

import os

os.environ["RUNNING_PYTEST"] = "true"

import matplotlib.pyplot as plt
import numpy as np
import pytest

plt.switch_backend("Agg")

import mplhep as hep


def test_hist_basic():
    """Test basic hist functionality with single dataset."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    fig, ax = plt.subplots()
    artists = hep.hist(data, bins=50, range=(50, 150), ax=ax)

    assert len(artists) == 1
    assert ax.get_xlabel() == ""
    plt.close(fig)


def test_hist_multiple_datasets():
    """Test hist with multiple datasets."""
    np.random.seed(42)
    data1 = np.random.normal(100, 15, 500)
    data2 = np.random.normal(120, 15, 500)

    fig, ax = plt.subplots()
    artists = hep.hist(
        [data1, data2],
        bins=50,
        range=(50, 150),
        label=["Dataset 1", "Dataset 2"],
        ax=ax,
    )

    assert len(artists) == 2
    plt.close(fig)


def test_hist_with_weights():
    """Test hist with weights."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)
    weights = np.random.uniform(0.5, 1.5, 1000)

    fig, ax = plt.subplots()
    artists = hep.hist(data, bins=50, weights=weights, ax=ax)

    assert len(artists) == 1
    plt.close(fig)


def test_hist_density():
    """Test hist with density normalization."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    fig, ax = plt.subplots()
    artists = hep.hist(data, bins=50, density=True, ax=ax)

    assert len(artists) == 1
    plt.close(fig)


def test_hist_histtype():
    """Test hist with different histtypes."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    for histtype in ["step", "fill", "errorbar"]:
        fig, ax = plt.subplots()
        artists = hep.hist(data, bins=50, histtype=histtype, ax=ax)
        assert len(artists) == 1
        plt.close(fig)


def test_hist_with_yerr_false():
    """Test hist with yerr=False."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    fig, ax = plt.subplots()
    artists = hep.hist(data, bins=50, yerr=False, ax=ax)

    assert len(artists) == 1
    plt.close(fig)


def test_hist_with_custom_bins():
    """Test hist with custom bin edges."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)
    bins = [50, 70, 90, 100, 110, 130, 150]

    fig, ax = plt.subplots()
    artists = hep.hist(data, bins=bins, ax=ax)

    assert len(artists) == 1
    plt.close(fig)


def test_hist_api_compatibility():
    """Test that hist provides similar results to plt.hist + histplot workflow."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    # Using the new hist function
    fig1, ax1 = plt.subplots()
    hep.hist(data, bins=50, range=(50, 150), ax=ax1)

    # Using manual workflow
    fig2, ax2 = plt.subplots()
    h, bins = np.histogram(data, bins=50, range=(50, 150))
    hep.histplot(h, bins, ax=ax2)

    # Both should produce similar plots
    # (we're not checking exact equality due to potential floating point differences)
    assert ax1.get_xlim() == ax2.get_xlim()

    plt.close(fig1)
    plt.close(fig2)


@pytest.mark.mpl_image_compare(style="default", remove_text=False, tolerance=10)
def test_hist_visual_single():
    """Visual test for single dataset histogram."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    fig, ax = plt.subplots(figsize=(8, 6))
    hep.hist(data, bins=50, range=(50, 150), label="Test Data", ax=ax)
    ax.set_xlabel("Value")
    ax.set_ylabel("Counts")
    ax.legend()

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False, tolerance=10)
def test_hist_visual_multiple():
    """Visual test for multiple dataset histograms."""
    np.random.seed(42)
    data1 = np.random.normal(100, 15, 1000)
    data2 = np.random.normal(120, 12, 1000)

    fig, ax = plt.subplots(figsize=(8, 6))
    hep.hist(
        [data1, data2],
        bins=50,
        range=(50, 150),
        label=["Distribution 1", "Distribution 2"],
        ax=ax,
    )
    ax.set_xlabel("Value")
    ax.set_ylabel("Counts")
    ax.legend()

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False, tolerance=10)
def test_hist_visual_fill():
    """Visual test with fill histtype."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    fig, ax = plt.subplots(figsize=(8, 6))
    hep.hist(data, bins=50, range=(50, 150), histtype="fill", alpha=0.5, ax=ax)
    ax.set_xlabel("Value")
    ax.set_ylabel("Counts")

    return fig
