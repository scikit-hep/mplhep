from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.decorators import check_figures_equal

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

"""
Tests for LaTeX-dependent styles (CMSTex, DUNETex, ATLASTex, LHCbTex, etc.)

To test run:
pytest tests/test_styles_latex.py --mpl

When adding new tests, run:
pytest tests/test_styles_latex.py --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")

pytestmark = [
    pytest.mark.latex,
    pytest.mark.skipif(sys.platform != "linux", reason="Linux only"),
]


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_cmstex():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(mh.style.CMSTex)
    fig, ax = plt.subplots()
    mh.cms.label("Preliminary")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_roottex():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(mh.style.ROOTTex)
    fig, ax = plt.subplots()
    ax.set_xlabel(r"$p_T$ [GeV]")
    ax.set_ylabel(r"Events / 10 GeV")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dunetex():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(mh.style.DUNETex)
    fig, ax = plt.subplots()
    mh.dune.label(text="Preliminary")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dunetex1():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(mh.style.DUNETex1)
    fig, ax = plt.subplots()
    mh.dune.label(text="Preliminary")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_atlastex():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(mh.style.ATLASTex)
    fig, ax = plt.subplots()
    mh.atlas.label(text="Preliminary")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcbtex1():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use([mh.style.LHCbTex1, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    mh.lhcb.label("Preliminary")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcbtex2():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use([mh.style.LHCbTex2, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    mh.lhcb.label("Preliminary")

    return fig


@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    ("mplhep_style", "str_alias"),
    [
        (mh.style.CMSTex, "CMSTex"),
        (mh.style.ROOTTex, "ROOTTex"),
        (mh.style.DUNETex, "DUNETex"),
        (mh.style.DUNETex1, "DUNETex1"),
        (mh.style.ATLASTex, "ATLASTex"),
        (mh.style.LHCbTex1, "LHCbTex1"),
        (mh.style.LHCbTex2, "LHCbTex2"),
    ],
    ids=[
        "CMSTex",
        "ROOTTex",
        "DUNETex",
        "DUNETex1",
        "ATLASTex",
        "LHCbTex1",
        "LHCbTex2",
    ],
)
def test_latex_style_str_alias(fig_test, fig_ref, mplhep_style, str_alias):
    """Test that string aliases work for all LaTeX style variants."""
    plt.rcParams.update(plt.rcParamsDefault)

    mh.rcParams.clear()
    plt.style.use(mplhep_style)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(str_alias)
    fig_test.subplots()
