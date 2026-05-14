from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.testing.decorators import check_figures_equal

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh


def _make_color_wheel_hists(n=10):
    """Create n Gaussian-like histograms to visualize color cycle in a stacked plot."""
    bins = np.arange(9)  # 8 bins: 0-1, 1-2, ..., 7-8
    # Hardcoded Gaussian-like values peaking around 10 in the middle
    h = np.array([1, 2, 5, 8, 10, 8, 5, 2])
    hists = [h] * n
    return hists, bins


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
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.atlas.label(text="Preliminary")
    mh.mpl_magic()

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_cms():
    plt.style.use(mh.style.CMS)
    fig, ax = plt.subplots()
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.cms.label("Preliminary")
    mh.mpl_magic()

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_alice():
    plt.style.use(mh.style.ALICE)
    fig, ax = plt.subplots()
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.alice.label("Preliminary")
    mh.mpl_magic()

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcb():
    plt.style.use([mh.style.LHCb1, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.lhcb.label("Preliminary")
    mh.mpl_magic()
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcb2():
    plt.style.use([mh.style.LHCb2, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.lhcb.label("Preliminary")
    mh.mpl_magic()
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dune():
    plt.style.use(mh.style.DUNE)
    fig, ax = plt.subplots()
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.dune.label(text="Preliminary")
    mh.mpl_magic()

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dune1():
    plt.style.use(mh.style.DUNE1)
    fig, ax = plt.subplots()
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.dune.label(text="Preliminary")
    mh.mpl_magic()

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_plothist():
    plt.style.use(mh.style.plothist)
    fig, ax = plt.subplots()
    hists, bins = _make_color_wheel_hists()
    mh.histplot(hists, bins, ax=ax, stack=True, histtype="fill")
    mh.mpl_magic()
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
def test_use_style_LHCb_default(fig_test, fig_ref):
    mh.rcParams.clear()
    mh.style.use(mh.style.LHCb2)
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
        (mh.style.LHCb1, "LHCb1"),
        (mh.style.LHCb2, "LHCb2"),
        (mh.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "DUNE1", "DUNE", "LHCb1", "LHCb2", "ROOT"],
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
        (mh.style.LHCb1, "LHCb1"),
        (mh.style.LHCb2, "LHCb2"),
        (mh.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "DUNE1", "DUNE", "LHCb1", "LHCb2", "ROOT"],
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
        (mh.style.LHCb1, "LHCb1"),
        (mh.style.LHCb2, "LHCb2"),
        (mh.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "DUNE1", "DUNE", "LHCb1", "LHCb2", "ROOT"],
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


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_cms_label_dpi_invariance():
    """Render `cms.label` on a non-square figure at elevated DPI.

    Regression guard for the dpi-vs-points fix: with the old (dimensionally
    wrong) formula the CMS<->Preliminary gap was pinned to a constant pixel
    count regardless of DPI, so at dpi=200 the gap shrinks to a sliver next
    to the (correctly-DPI-scaled) text. The corrected math keeps the gap a
    constant fraction of an inch.
    """
    fig, axs = plt.subplots(2, 1, figsize=(12, 5), dpi=200)
    axs[0].set_title("loc=0")
    mh.cms.label("Preliminary", ax=axs[0], lumi=50, data=True, loc=0)
    axs[1].set_title("loc=2")
    mh.cms.label("Preliminary", ax=axs[1], lumi=50, data=True, loc=2)
    return fig


def test_cms_label_gap_is_dpi_invariant():
    """The horizontal gap between 'CMS' and the appended experiment-status
    text must be a constant physical size (constant inches), not a constant
    pixel size, so that high-DPI saves don't shrink the gap to a sliver.

    Under the old `fontsize / ax_width / dpi` formula, the gap was instead
    pinned to a constant pixel count regardless of DPI -- correct at dpi=100
    but visibly wrong on a 300 DPI print.
    """
    gaps_in_inches = []
    for dpi in (50, 100, 200, 300):
        with plt.style.context(mh.style.CMS):
            fig = plt.figure(figsize=(12, 5), dpi=dpi)
            ax = fig.add_subplot(111)
            mh.cms.label("Preliminary", ax=ax, lumi=50, data=True, loc=0)
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]

            cms_bb = pre_bb = None
            for t in ax.texts:
                if getattr(t, "_text", None) == "CMS":
                    cms_bb = t.get_window_extent(renderer)
                elif getattr(t, "_text", None) == "Preliminary":
                    pre_bb = t.get_window_extent(renderer)

            assert cms_bb is not None, "expected a 'CMS' text artist"
            assert pre_bb is not None, "expected a 'Preliminary' text artist"

            gaps_in_inches.append((pre_bb.x0 - cms_bb.x1) / dpi)
            plt.close(fig)

    # All measured gaps should be identical in inches (constant physical
    # size). Half a hundredth-of-an-inch tolerance for sub-pixel rounding.
    ref = gaps_in_inches[0]
    for dpi, gap in zip((50, 100, 200, 300), gaps_in_inches, strict=True):
        assert abs(gap - ref) < 5e-3, (
            f"Gap at dpi={dpi} is {gap:.4f}in but at dpi=50 is {ref:.4f}in -- "
            f"label positioning is not DPI-invariant. All gaps: {gaps_in_inches}"
        )
