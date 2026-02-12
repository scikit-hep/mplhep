"""Image comparison tests for the blinding functionality."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pytest

import mplhep as mh
from mplhep._utils import EnhancedPlottableHistogram
from mplhep.blind import loc

plt.switch_backend("Agg")

# Shared histogram data

_h = np.array([2, 5, 10, 15, 20, 18, 12, 8, 4, 1])
_h2 = np.array([1, 3, 7, 10, 14, 12, 9, 5, 2, 1])
_bins = np.linspace(0, 100, 11)


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_blind_spec_formats():
    """Test all blind specification formats in a single figure."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Tuple (value-based)
    mh.histplot(_h, _bins, ax=axes[0, 0], blind=(40, 70))

    # String value-based (j-suffix)
    mh.histplot(_h, _bins, ax=axes[0, 1], blind="30j:60j")

    # String index-based
    mh.histplot(_h, _bins, ax=axes[0, 2], blind="2:7")

    # loc slice
    mh.histplot(_h, _bins, ax=axes[1, 0], blind=loc[20:80])

    # Complex-number UHI convention
    mh.histplot(_h, _bins, ax=axes[1, 1], blind=slice(30j, 70j))

    # Plain integer slice (index-based)
    mh.histplot(_h, _bins, ax=axes[1, 2], blind=slice(3, 7))

    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_blind_histtypes():
    """Test blinding across histtypes and stacking/overlay."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # step (default)
    mh.histplot(_h, _bins, ax=axes[0, 0], blind=(30, 70))

    # step with yerr
    mh.histplot(_h, _bins, ax=axes[0, 1], yerr=True, blind=(30, 70))

    # fill
    mh.histplot(_h, _bins, ax=axes[0, 2], histtype="fill", blind=(30, 70))

    # errorbar
    mh.histplot(
        _h, _bins, ax=axes[1, 0], histtype="errorbar", yerr=True, blind=(30, 70)
    )

    # stacked
    mh.histplot([_h, _h2], _bins, ax=axes[1, 1], stack=True, blind=(30, 70))

    # overlay
    mh.histplot([_h, _h2], _bins, ax=axes[1, 2], blind=(30, 70))

    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_blind_region_patterns():
    """Test multiple regions and open-ended blinding."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Multiple disjoint regions
    mh.histplot(_h, _bins, ax=axes[0], blind=[(10, 30), (60, 90)])

    # Open-ended left
    mh.histplot(_h, _bins, ax=axes[1], blind=(None, 40))

    # Open-ended right
    mh.histplot(_h, _bins, ax=axes[2], blind=(50, None))

    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_blind_index_lists():
    """Test blinding by lists of individual bin indices and mixed lists."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Single int
    mh.histplot(_h, _bins, ax=axes[0, 0], blind=3)

    # List of ints
    mh.histplot(_h, _bins, ax=axes[0, 1], blind=[1, 4, 7])

    # List of ints (adjacent = contiguous gap)
    mh.histplot(_h, _bins, ax=axes[0, 2], blind=[3, 4, 5])

    # Mixed: int + value-range
    mh.histplot(_h, _bins, ax=axes[1, 0], blind=[0, (40, 70)])

    # Mixed: int + index-range string
    mh.histplot(_h, _bins, ax=axes[1, 1], blind=[9, "2:5"])

    # Mixed: int + value-range + loc slice
    mh.histplot(_h, _bins, ax=axes[1, 2], blind=[0, (60, 80), loc[20:40]])

    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_blind_mixed_types():
    """Test mixed index/value specs: loc[idx:valj], slice(idx, valj), string."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # loc[index : value_j] — index 2, value 60
    mh.histplot(_h, _bins, ax=axes[0, 0], blind=loc[2:60j])

    # loc[value_j : index] — value 30, index 8
    mh.histplot(_h, _bins, ax=axes[0, 1], blind=loc[30j:8])

    # slice(index, complex) — index 3, value 70
    mh.histplot(_h, _bins, ax=axes[0, 2], blind=slice(3, 70j))

    # slice(complex, index) — value 20, index 7
    mh.histplot(_h, _bins, ax=axes[1, 0], blind=slice(20j, 7))

    # String mixed — "2:60j"
    mh.histplot(_h, _bins, ax=axes[1, 1], blind="2:60j")

    # String mixed reverse — "30j:8"
    mh.histplot(_h, _bins, ax=axes[1, 2], blind="30j:8")

    fig.tight_layout()
    return fig


# Plottable histograms for comparison tests
def _make_plottables():
    vals1 = np.array([10, 20, 30, 40, 50, 45, 35, 25, 15, 5], dtype=float)
    vals2 = np.array([8, 15, 25, 35, 42, 38, 28, 18, 10, 3], dtype=float)
    edges = np.linspace(0, 100, 11)
    h1 = EnhancedPlottableHistogram(vals1, edges=edges, variances=vals1)
    h2 = EnhancedPlottableHistogram(vals2, edges=edges, variances=vals2)
    return h1, h2


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_blind_comparison_plotters():
    """Test that blinding propagates through comparison plotters."""
    h1, h2 = _make_plottables()

    fig, axes = plt.subplots(
        2, 2, figsize=(14, 10), gridspec_kw={"height_ratios": [3, 1]}
    )

    # comp.hists with value-based blind
    mh.comp.hists(
        h1,
        h2,
        blind=(30, 70),
        fig=fig,
        ax_main=axes[0, 0],
        ax_comparison=axes[1, 0],
    )

    # comp.data_model with value-based blind
    mh.comp.data_model(
        h1,
        stacked_components=[h2],
        blind=(30, 70),
        fig=fig,
        ax_main=axes[0, 1],
        ax_comparison=axes[1, 1],
    )

    return fig
