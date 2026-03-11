"""Tests for mplhep.funcplot() function.

This function was completely untested. These tests cover:
- Single function plotting
- Multiple function plotting
- Stacked function plotting
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

os.environ['RUNNING_PYTEST'] = 'true'

import pytest

import mplhep as mh

plt.switch_backend('Agg')


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_funcplot_single():
    """Test funcplot() with a single function."""
    fig, ax = plt.subplots(figsize=(10, 10))
    mh.funcplot(np.sin, range=(0, 2 * np.pi), ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_funcplot_multiple():
    """Test funcplot() with multiple functions."""
    fig, ax = plt.subplots(figsize=(10, 10))
    mh.funcplot([np.sin, np.cos], range=(0, 2 * np.pi), ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_funcplot_stack():
    """Test funcplot() with stacked functions."""
    fig, ax = plt.subplots(figsize=(10, 10))

    def f1(x):
        return np.abs(np.sin(x))

    def f2(x):
        return np.abs(np.cos(x))

    mh.funcplot([f1, f2], range=(0, 2 * np.pi), ax=ax, stack=True)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_funcplot_single_stack():
    """Test funcplot() with a single function in stack mode."""
    fig, ax = plt.subplots(figsize=(10, 10))
    mh.funcplot(lambda x: x**2, range=(0, 3), ax=ax, stack=True)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True, baseline_dir='../baseline')
def test_funcplot_kwargs():
    """Test funcplot() with additional kwargs passed to ax.plot."""
    fig, ax = plt.subplots(figsize=(10, 10))
    mh.funcplot(np.sin, range=(0, 2 * np.pi), ax=ax, color='red', linewidth=3)
    return fig
