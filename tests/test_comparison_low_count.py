"""
Image comparison tests for comparison plots with low-count histograms.

These tests verify the visual output of comparison methods when data contains
zero and single-count bins, particularly with Poisson confidence intervals
(h1_w2method='poisson') which produce asymmetric uncertainties.
"""

import hist
import matplotlib.pyplot as plt
import numpy as np
import pytest

import mplhep
from mplhep.comparison_plotters import comparison

# Comparison types that support Poisson uncertainties
COMPARISONS = [
    "ratio",
    "split_ratio",
    "pull",
    "difference",
    "relative_difference",
]


def _make_low_count_hists():
    """Create deterministic low-count histograms with zero and single-count bins."""
    rng = np.random.default_rng(42)
    h_data = hist.new.Regular(20, -4, 4).Weight()
    h_data.fill(rng.normal(0, 1.0, 50))

    h_model = hist.new.Regular(20, -4, 4).Weight()
    h_model.fill(rng.normal(0, 1.0, 5000))
    h_model = h_model * 0.01  # scale to ~50 total

    return h_data, h_model


@pytest.fixture(autouse=True)
def close_all_figures():
    """Automatically close all figures after each test."""
    yield
    plt.close("all")


@pytest.mark.mpl_image_compare(
    style=mplhep.style.plothist,
    savefig_kwargs={"bbox_inches": "tight"},
    deterministic=True,
    tolerance=0,
)
def test_low_count_comparisons_poisson_vs_sqrt():
    """2x5 grid: poisson (left) vs sqrt (right) for each comparison type."""
    h_data, h_model = _make_low_count_hists()
    n = len(COMPARISONS)
    fig, axes = plt.subplots(n, 2, figsize=(12, 3 * n))
    for row, comp_type in enumerate(COMPARISONS):
        for col, w2method in enumerate(["poisson", "sqrt"]):
            ax = axes[row, col]
            comparison(
                h_data,
                h_model,
                ax,
                comparison=comp_type,
                h1_w2method=w2method,
            )
            ax.autoscale(axis="y")
            ax.set_title(f"{comp_type} ({w2method})")
    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(
    style=mplhep.style.plothist,
    savefig_kwargs={"bbox_inches": "tight"},
    deterministic=True,
    tolerance=0,
)
def test_low_count_comparisons_defaults():
    """1x5 grid: all comparison types with default settings."""
    h_data, h_model = _make_low_count_hists()
    n = len(COMPARISONS)
    fig, axes = plt.subplots(n, 1, figsize=(8, 3 * n))
    for ax, comp_type in zip(axes, COMPARISONS):
        comparison(
            h_data,
            h_model,
            ax,
            comparison=comp_type,
        )
        ax.autoscale(axis="y")
        ax.set_title(comp_type)
    fig.tight_layout()
    return fig
