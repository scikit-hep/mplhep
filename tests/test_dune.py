from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.decorators import check_figures_equal

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

plt.switch_backend("Agg")


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
def test_dune_style_variants(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    mh.rcParams.clear()
    plt.style.use(mh.style.DUNE1)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(mh.style.DUNE1)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
def test_dune_style_str_alias(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    mh.rcParams.clear()
    plt.style.use(mh.style.DUNE1)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use("DUNE")
    fig_test.subplots()


@pytest.mark.skip("Fails in Github Action")
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dunetex():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(mh.style.DUNETex)
    fig, ax = plt.subplots()
    mh.dune.label(label="Preliminary")

    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@pytest.mark.skip("Fails in Github Action")
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dunetex1():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(mh.style.DUNETex1)
    fig, ax = plt.subplots()
    mh.dune.label(label="Preliminary")

    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    ("style", "str_alias"),
    [
        (mh.style.DUNE, "DUNE"),
        (mh.style.DUNE1, "DUNE1"),
        # (mh.style.DUNETex, "DUNETex"),  # fails in github action
        # (mh.style.DUNETex1, "DUNETex1"),  # fails in github action
    ],
    ids=[
        "DUNE",
        "DUNE1",
        # "DUNETex",  # fails in github action
        # "DUNETex1"  # fails in github action
    ],
)
def test_dune_style_string_aliases(fig_test, fig_ref, style, str_alias):
    """Test that string aliases work for all DUNE style variants."""
    plt.rcParams.update(plt.rcParamsDefault)

    mh.rcParams.clear()
    plt.style.use(style)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(str_alias)
    fig_test.subplots()


@pytest.mark.mpl_image_compare(style="default")
def test_dune_label_loc():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for i, ax in enumerate(axs.flatten()):
        mh.dune.label(label="Preliminary", loc=i, ax=ax, lumi=50, data=True)
        ax.set_title(f"loc={i}")
    return fig
