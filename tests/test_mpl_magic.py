"""Tests for mpl_magic and related functions."""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pytest

import mplhep as mh

plt.switch_backend("Agg")


def test_mpl_magic_basic():
    """Test mpl_magic with default parameters."""
    fig, ax = plt.subplots()
    h = [1, 3, 2, 4, 3]
    bins = [0, 1, 2, 3, 4, 5]
    ax.stairs(h, bins, label="Test")
    ax.legend()

    result = mh.mpl_magic(ax)
    assert result is ax, "mpl_magic should return the axes object"
    plt.close(fig)


def test_mpl_magic_with_soft_fail():
    """Test mpl_magic with soft_fail parameter."""
    fig, ax = plt.subplots()
    h = [1, 3, 2, 4, 3]
    bins = [0, 1, 2, 3, 4, 5]
    ax.stairs(h, bins, label="Test")
    ax.legend()

    # Should not raise even if legend/text can't fit
    result = mh.mpl_magic(ax, soft_fail=True)
    assert result is ax, "mpl_magic should return the axes object"
    plt.close(fig)


def test_mpl_magic_with_ylow():
    """Test mpl_magic with ylow parameter."""
    fig, ax = plt.subplots()
    h = [1, 3, 2, 4, 3]
    bins = [0, 1, 2, 3, 4, 5]
    ax.stairs(h, bins, label="Test")
    ax.legend()

    result = mh.mpl_magic(ax, ylow=0.5)
    assert result is ax, "mpl_magic should return the axes object"
    # Check that y limit was set
    ylim = ax.get_ylim()
    assert ylim[0] == 0.5, f"Expected ylow=0.5, got {ylim[0]}"
    plt.close(fig)


def test_mpl_magic_with_otol():
    """Test mpl_magic with otol parameters."""
    fig, ax = plt.subplots()
    h = [1, 3, 2, 4, 3]
    bins = [0, 1, 2, 3, 4, 5]
    ax.stairs(h, bins, label="Test")
    ax.legend()

    result = mh.mpl_magic(ax, legend_otol=0.1, yscale_otol=0.1)
    assert result is ax, "mpl_magic should return the axes object"
    plt.close(fig)


def test_mpl_magic_all_params():
    """Test mpl_magic with all parameters."""
    fig, ax = plt.subplots()
    h = [1, 3, 2, 4, 3]
    bins = [0, 1, 2, 3, 4, 5]
    ax.stairs(h, bins, label="Test")
    ax.legend()

    result = mh.mpl_magic(
        ax=ax,
        ylow=0.5,
        legend_otol=0.1,
        yscale_otol=0.1,
        soft_fail=True,
    )
    assert result is ax, "mpl_magic should return the axes object"
    ylim = ax.get_ylim()
    assert ylim[0] == 0.5, f"Expected ylow=0.5, got {ylim[0]}"
    plt.close(fig)


def test_ylow_with_value():
    """Test ylow function with a specific value."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])

    result = mh.plot.ylow(ax, ylow=0.5)
    assert result is ax, "ylow should return the axes object"
    ylim = ax.get_ylim()
    assert ylim[0] == 0.5, f"Expected ylow=0.5, got {ylim[0]}"
    plt.close(fig)


def test_ylow_with_none():
    """Test ylow function with automatic scaling."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])

    result = mh.plot.ylow(ax, ylow=None)
    assert result is ax, "ylow should return the axes object"
    ylim = ax.get_ylim()
    # With positive data, should set to 0
    assert ylim[0] == 0, f"Expected ylow=0 for positive data, got {ylim[0]}"
    plt.close(fig)


def test_ylow_log_scale():
    """Test ylow function with log scale (should not change limits)."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 10, 100])
    ax.set_yscale("log")
    original_ylim = ax.get_ylim()

    result = mh.plot.ylow(ax, ylow=0.5)
    assert result is ax, "ylow should return the axes object"
    # Log scale should not be modified
    assert ax.get_ylim() == original_ylim, "ylow should not modify log scale"
    plt.close(fig)


def test_yscale_legend_basic():
    """Test yscale_legend function."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3], label="Test")
    ax.legend()

    result = mh.plot.yscale_legend(ax)
    assert result is ax, "yscale_legend should return the axes object"
    plt.close(fig)


def test_yscale_legend_with_soft_fail():
    """Test yscale_legend with soft_fail."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3], label="Test")
    ax.legend()

    result = mh.plot.yscale_legend(ax, soft_fail=True)
    assert result is ax, "yscale_legend should return the axes object"
    plt.close(fig)


def test_yscale_anchored_text_basic():
    """Test yscale_anchored_text function."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])

    result = mh.plot.yscale_anchored_text(ax)
    assert result is ax, "yscale_anchored_text should return the axes object"
    plt.close(fig)


def test_yscale_anchored_text_with_soft_fail():
    """Test yscale_anchored_text with soft_fail."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])

    result = mh.plot.yscale_anchored_text(ax, soft_fail=True)
    assert result is ax, "yscale_anchored_text should return the axes object"
    plt.close(fig)
