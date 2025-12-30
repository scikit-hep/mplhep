"""
Tests for hist2dplot cbarpos parameter with matplotlib >= 3.6.

This test addresses the bug where using cbarpos="top" or cbarpos="bottom"
causes an AttributeError due to matplotlib 3.6+ making groupers immutable.
The fix uses ax.sharex() instead of the deprecated .join() method.
"""

from __future__ import annotations

import os

os.environ["RUNNING_PYTEST"] = "true"

import matplotlib.pyplot as plt
import numpy as np
import pytest

plt.switch_backend("Agg")

import mplhep as mh


@pytest.fixture
def sample_2d_data():
    """Create sample 2D histogram data."""
    np.random.seed(42)
    xedges = np.linspace(0, 10, 51)
    yedges = np.linspace(0, 10, 51)
    H = np.random.normal(size=(50, 50))
    return H, xedges, yedges


def test_hist2dplot_cbarpos_top(sample_2d_data):
    """Test hist2dplot with cbarpos='top'."""
    H, xedges, yedges = sample_2d_data
    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, cbar=True, cbarpos="top", ax=ax)
    plt.close(fig)


def test_hist2dplot_cbarpos_bottom(sample_2d_data):
    """Test hist2dplot with cbarpos='bottom'."""
    H, xedges, yedges = sample_2d_data
    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, cbar=True, cbarpos="bottom", ax=ax)
    plt.close(fig)


def test_hist2dplot_cbarpos_left(sample_2d_data):
    """Test hist2dplot with cbarpos='left'."""
    H, xedges, yedges = sample_2d_data
    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, cbar=True, cbarpos="left", ax=ax)
    plt.close(fig)


def test_hist2dplot_cbarpos_right(sample_2d_data):
    """Test hist2dplot with cbarpos='right'."""
    H, xedges, yedges = sample_2d_data
    fig, ax = plt.subplots()
    mh.hist2dplot(H, xedges, yedges, cbar=True, cbarpos="right", ax=ax)
    plt.close(fig)


def test_hist2dplot_cbarpos_all_positions(sample_2d_data):
    """Test hist2dplot with all cbarpos positions in one test."""
    H, xedges, yedges = sample_2d_data
    positions = ["top", "bottom", "left", "right"]

    for pos in positions:
        fig, ax = plt.subplots()
        mh.hist2dplot(H, xedges, yedges, cbar=True, cbarpos=pos, ax=ax)
        plt.close(fig)


@pytest.mark.mpl_image_compare(style="default", remove_text=True, tolerance=10)
def test_hist2dplot_cbarpos_top_visual():
    """Visual comparison test for cbarpos='top'."""
    np.random.seed(42)
    xedges = np.linspace(0, 10, 21)
    yedges = np.linspace(0, 10, 21)
    x = np.random.normal(5, 2, 1000)
    y = np.random.normal(5, 2, 1000)
    H, _, _ = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots(figsize=(8, 7))
    mh.hist2dplot(H, xedges, yedges, cbar=True, cbarpos="top", ax=ax)

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True, tolerance=10)
def test_hist2dplot_cbarpos_bottom_visual():
    """Visual comparison test for cbarpos='bottom'."""
    np.random.seed(42)
    xedges = np.linspace(0, 10, 21)
    yedges = np.linspace(0, 10, 21)
    x = np.random.normal(5, 2, 1000)
    y = np.random.normal(5, 2, 1000)
    H, _, _ = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots(figsize=(8, 7))
    mh.hist2dplot(H, xedges, yedges, cbar=True, cbarpos="bottom", ax=ax)

    return fig
