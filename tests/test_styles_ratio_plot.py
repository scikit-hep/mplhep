from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import hist
import numpy as np

import mplhep as mh

"""
To test run:
pytest --mpl

When adding new tests, run:
pytest --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


@pytest.fixture
def get_histogram():
    np.random.seed(42)
    x1 = np.random.normal(0, 1, 1000)
    x2 = np.random.normal(0, 1.05, 1000)
    h1 = hist.new.Reg(25, -4, 4).Weight().fill(x1)
    h2 = hist.new.Reg(25, -4, 4).Weight().fill(x2)

    return h1, h2


# Compare styles
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_ratio_plot_atlas(get_histogram):
    # Test suite does not have Helvetica
    plt.style.use([mh.style.ATLAS, {"font.sans-serif": ["Tex Gyre Heros"]}])
    h1, h2 = get_histogram
    fig, _, _ = mh.comp.hists(h1, h2)

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_ratio_plot_cms(get_histogram):
    plt.style.use(mh.style.CMS)
    h1, h2 = get_histogram
    fig, _, _ = mh.comp.hists(h1, h2)

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_ratio_plot_alice(get_histogram):
    plt.style.use(mh.style.ALICE)
    h1, h2 = get_histogram
    fig, _, _ = mh.comp.hists(h1, h2)

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_ratio_plot_lhcb(get_histogram):
    plt.style.use([mh.style.LHCb, {"figure.autolayout": False}])
    h1, h2 = get_histogram
    fig, _, _ = mh.comp.hists(h1, h2)

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_ratio_plot_dune(get_histogram):
    plt.style.use(mh.style.DUNE)
    h1, h2 = get_histogram
    fig, _, _ = mh.comp.hists(h1, h2)

    return fig
