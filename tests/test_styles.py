from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.decorators import check_figures_equal

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

"""
To test run:
pytest --mpl

When adding new tests, run:
pytest --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


# Compare styles
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_atlas():
    # Test suite does not have Helvetica
    plt.style.use([mh.style.ATLAS, {"font.sans-serif": ["Tex Gyre Heros"]}])
    fig, ax = plt.subplots()
    mh.atlas.label(text="Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_cms():
    plt.style.use(mh.style.CMS)
    fig, ax = plt.subplots()
    mh.cms.label("Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_alice():
    plt.style.use(mh.style.ALICE)
    fig, ax = plt.subplots()
    mh.alice.label("Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcb():
    plt.style.use([mh.style.LHCb1, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    mh.lhcb.label("Preliminary")
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcb2():
    plt.style.use([mh.style.LHCb2, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    mh.lhcb.label("Preliminary")
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dune():
    plt.style.use(mh.style.DUNE)
    fig, ax = plt.subplots()
    mh.dune.label(text="Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dune1():
    plt.style.use(mh.style.DUNE1)
    fig, ax = plt.subplots()
    mh.dune.label(text="Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_plothist():
    plt.style.use(mh.style.PLOTHIST)
    fig, ax = plt.subplots()
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    "mplhep_style",
    [
        mh.style.ALICE,
        mh.style.ATLAS,
        mh.style.CMS,
        mh.style.DUNE1,
        mh.style.DUNE,
        mh.style.LHCb1,
        mh.style.LHCb2,
        mh.style.ROOT,
    ],
    ids=["ALICE", "ATLAS", "CMS", "DUNE1", "DUNE", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style(fig_test, fig_ref, mplhep_style):
    mh.rcParams.clear()
    plt.style.use(mplhep_style)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(mplhep_style)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
def test_use_style_LHCb_dep(fig_test, fig_ref):
    mh.rcParams.clear()
    with pytest.warns(FutureWarning):
        plt.style.use(mh.style.LHCb)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(mh.style.LHCb)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    ("mplhep_style", "str_alias"),
    [
        (mh.style.ALICE, "ALICE"),
        (mh.style.ATLAS, "ATLAS"),
        (mh.style.CMS, "CMS"),
        (mh.style.DUNE1, "DUNE1"),
        (mh.style.DUNE, "DUNE"),
        (mh.style.LHCb, "LHCb"),
        (mh.style.LHCb1, "LHCb1"),
        (mh.style.LHCb2, "LHCb2"),
        (mh.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "DUNE1", "DUNE", "LHCb", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style_str_alias(fig_test, fig_ref, mplhep_style, str_alias):
    mh.rcParams.clear()
    plt.style.use(mplhep_style)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(str_alias)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    ("mplhep_style", "str_alias"),
    [
        (mh.style.ALICE, "ALICE"),
        (mh.style.ATLAS, "ATLAS"),
        (mh.style.CMS, "CMS"),
        (mh.style.DUNE1, "DUNE1"),
        (mh.style.DUNE, "DUNE"),
        (mh.style.LHCb, "LHCb"),
        (mh.style.LHCb1, "LHCb1"),
        (mh.style.LHCb2, "LHCb2"),
        (mh.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "DUNE1", "DUNE", "LHCb", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style_self_consistent(fig_test, fig_ref, mplhep_style, str_alias):
    mh.rcParams.clear()
    mh.style.use(mplhep_style)
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use(str_alias)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    ("mplhep_style", "str_alias"),
    [
        (mh.style.ALICE, "ALICE"),
        (mh.style.ATLAS, "ATLAS"),
        (mh.style.CMS, "CMS"),
        (mh.style.DUNE1, "DUNE1"),
        (mh.style.DUNE, "DUNE"),
        (mh.style.LHCb, "LHCb"),
        (mh.style.LHCb1, "LHCb1"),
        (mh.style.LHCb2, "LHCb2"),
        (mh.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "DUNE1", "DUNE", "LHCb", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style_style_list(fig_test, fig_ref, mplhep_style, str_alias):
    mh.rcParams.clear()
    plt.style.use([mplhep_style, {"font.sans-serif": "Comic Sans MS"}])
    fig_ref.subplots()

    mh.rcParams.clear()
    mh.style.use([str_alias, {"font.sans-serif": "Comic Sans MS"}])
    fig_test.subplots()


@pytest.mark.mpl_image_compare(style="default")
def test_labeltext_loc():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for i, ax in enumerate(axs.flatten()):
        mh.cms.text("Test", loc=i, ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_label_loc():
    fig, axs = plt.subplots(1, 5, figsize=(20, 4))
    for i, ax in enumerate(axs.flatten()):
        mh.cms.label("Preliminary", loc=i, ax=ax, lumi=50, data=True)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_pub_loc():
    fig, axs = plt.subplots(2, 5, figsize=(20, 8))
    for i, ax in enumerate(axs.flatten()):
        mh.cms.label(loc=i % 5, ax=ax, lumi=50, supp="arXiv:aaaa.bbbbb", data=(i >= 5))
    return fig


@check_figures_equal(extensions=["pdf"])
def test_label_config(fig_test, fig_ref):
    mh.rcParams.label.data = True
    mh.rcParams.label.lumi = 30
    mh.rcParams.label.text = "Internal"

    test_ax = fig_test.subplots()
    mh.cms.label(data=False, ax=test_ax)

    ref_ax = fig_ref.subplots()
    mh.rcParams.clear()
    mh.cms.label(data=False, lumi=30, text="Internal", ax=ref_ax)
