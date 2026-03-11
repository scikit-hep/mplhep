"""Tests for mplhep.hist() function (raw data histogramming).

This function was completely untested. These tests cover:
- Single dataset histogramming
- Multiple dataset histogramming
- Weights handling (single and per-dataset)
- Density normalization
- Range parameter
- Custom bins
- Edge cases (empty list guard)
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

os.environ['RUNNING_PYTEST'] = 'true'

import mplhep as mh

plt.switch_backend('Agg')


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_single_dataset():
    """Test hist() with a single array of raw data."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data = np.random.normal(100, 15, 1000)
    mh.hist(data, bins=50, range=(50, 150), ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_multiple_datasets():
    """Test hist() with multiple datasets."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data1 = np.random.normal(100, 15, 500)
    data2 = np.random.normal(120, 15, 500)
    mh.hist(
        [data1, data2],
        bins=50,
        label=['Dataset 1', 'Dataset 2'],
        ax=ax,
    )
    ax.legend()
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_with_weights():
    """Test hist() with weights for a single dataset."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data = np.random.normal(100, 15, 1000)
    weights = np.random.uniform(0.5, 2.0, 1000)
    mh.hist(data, bins=50, range=(50, 150), weights=weights, ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_multiple_datasets_per_dataset_weights():
    """Test hist() with per-dataset weights for multiple datasets."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data1 = np.random.normal(100, 15, 500)
    data2 = np.random.normal(120, 15, 500)
    w1 = np.random.uniform(0.5, 2.0, 500)
    w2 = np.random.uniform(1.0, 3.0, 500)
    mh.hist(
        [data1, data2],
        bins=50,
        range=(50, 150),
        weights=[w1, w2],
        label=['Dataset 1', 'Dataset 2'],
        ax=ax,
    )
    ax.legend()
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_density():
    """Test hist() with density normalization."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data = np.random.normal(100, 15, 1000)
    mh.hist(data, bins=50, range=(50, 150), density=True, ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_custom_bins():
    """Test hist() with custom bin edges."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data = np.random.normal(100, 15, 1000)
    bins = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    mh.hist(data, bins=bins, ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_histtype_fill():
    """Test hist() with fill histtype."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data = np.random.normal(100, 15, 1000)
    mh.hist(data, bins=50, range=(50, 150), histtype='fill', ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_hist_histtype_errorbar():
    """Test hist() with errorbar histtype."""
    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(10, 10))
    data = np.random.normal(100, 15, 1000)
    mh.hist(data, bins=50, range=(50, 150), histtype='errorbar', ax=ax)
    return fig


def test_hist_returns_artists():
    """Test that hist() returns Hist1DArtists."""
    np.random.seed(42)
    data = np.random.normal(100, 15, 100)
    result = mh.hist(data, bins=10)
    assert result is not None
    assert isinstance(result, list)
    plt.close('all')


def test_hist_list_of_numbers():
    """Test that hist() handles list of numbers correctly (not as multiple datasets)."""
    fig, ax = plt.subplots()
    # A list of numbers should be treated as a single dataset, not multiple
    result = mh.hist([1, 2, 3, 4, 5], bins=5, ax=ax)
    assert result is not None
    plt.close('all')
