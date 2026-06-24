from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

plt.switch_backend("Agg")


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
def test_snop_style_variants(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    mh.rcParams.clear()
    plt.style.use(mh.style.SNOplus1)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(mh.style.SNOplus1)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
def test_snop_style_str_alias(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    mh.rcParams.clear()
    plt.style.use(mh.style.SNOplus1)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use("SNOplus")
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    ("style", "str_alias"),
    [
        (mh.style.SNOplus, "SNOplus"),
        (mh.style.SNOplus, "SNOplus1"),
    ],
    ids=["SNOplus", "SNOplus1"],
)
def test_snop_style_string_aliases(fig_test, fig_ref, style, str_alias):
    """Test that string aliases work for all SNO+ style variants."""
    plt.rcParams.update(plt.rcParamsDefault)

    mh.rcParams.clear()
    plt.style.use(style)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(str_alias)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default")
def test_snop_text_loc():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    locs = ["top left", "top right", "bottom left", "bottom right"]
    for i, ax in enumerate(axs.flatten()):
        mh.snoplus.text(text="SNO+ Preliminary", loc=locs[i], ax=ax)
        ax.set_title(f"loc={locs[i]}")
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default")
def test_snop_text_xy():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    locs = [(0.1, 0.2), (0.2, 0.1), (0.4, 0.5), (0.5, 0.4)]
    for i, ax in enumerate(axs.flatten()):
        mh.snoplus.text(
            text="SNO+ Preliminary", x=locs[i][0], y=locs[i][1], ax=ax, fontsize=8
        )
        ax.set_title(f"(x,y)={locs[i]}")
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default")
def test_snop_legend():
    fig, axs = plt.subplots()
    np.random.seed(0)
    x = np.random.normal(size=1000)
    c, b = np.histogram(x, bins=50)
    x_pts = np.linspace(-4, 4, len(c))
    y_err = np.abs(np.random.normal(size=len(c)) + 20)
    axs.errorbar(x_pts, c, yerr=y_err, fmt=".", label="Test Error", color="black")
    axs.hist(b[:-1], b, weights=c, histtype="step", label="Test Hist", color="red")
    axs.plot(x_pts, x_pts, label="Test Line")
    mh.snoplus.legend(axs)
    return fig
