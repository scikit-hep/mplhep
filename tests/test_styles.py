from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.decorators import check_figures_equal

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as hep  # noqa: E402

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
    plt.rcParams.update(plt.rcParamsDefault)

    # Test suite does not have Helvetica
    plt.style.use([hep.style.ATLAS, {"font.sans-serif": ["Tex Gyre Heros"]}])
    fig, ax = plt.subplots()
    hep.atlas.label(label="Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_cms():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots()
    hep.cms.label("Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_alice():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(hep.style.ALICE)
    fig, ax = plt.subplots()
    hep.alice.label("Preliminary")

    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcb():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use([hep.style.LHCb1, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    hep.lhcb.label("Preliminary")
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcb2():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use([hep.style.LHCb2, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    hep.lhcb.label("Preliminary")
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    "mplhep_style",
    [
        hep.style.ALICE,
        hep.style.ATLAS,
        hep.style.CMS,
        hep.style.LHCb1,
        hep.style.LHCb2,
        hep.style.ROOT,
    ],
    ids=["ALICE", "ATLAS", "CMS", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style(fig_test, fig_ref, mplhep_style):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use(mplhep_style)
    fig_ref.subplots()

    hep.rcParams.clear()
    hep.style.use(mplhep_style)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
def test_use_style_LHCb_dep(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    with pytest.warns(FutureWarning):
        plt.style.use(hep.style.LHCb)
    fig_ref.subplots()

    hep.rcParams.clear()
    hep.style.use(hep.style.LHCb)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    "mplhep_style, str_alias",
    [
        (hep.style.ALICE, "ALICE"),
        (hep.style.ATLAS, "ATLAS"),
        (hep.style.CMS, "CMS"),
        (hep.style.LHCb, "LHCb"),
        (hep.style.LHCb1, "LHCb1"),
        (hep.style.LHCb2, "LHCb2"),
        (hep.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "LHCb", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style_str_alias(fig_test, fig_ref, mplhep_style, str_alias):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use(mplhep_style)
    fig_ref.subplots()

    hep.rcParams.clear()
    hep.style.use(str_alias)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    "mplhep_style, str_alias",
    [
        (hep.style.ALICE, "ALICE"),
        (hep.style.ATLAS, "ATLAS"),
        (hep.style.CMS, "CMS"),
        (hep.style.LHCb, "LHCb"),
        (hep.style.LHCb1, "LHCb1"),
        (hep.style.LHCb2, "LHCb2"),
        (hep.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "LHCb", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style_self_consistent(fig_test, fig_ref, mplhep_style, str_alias):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    hep.style.use(mplhep_style)
    fig_ref.subplots()

    hep.rcParams.clear()
    hep.style.use(str_alias)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    "mplhep_style, str_alias",
    [
        (hep.style.ALICE, "ALICE"),
        (hep.style.ATLAS, "ATLAS"),
        (hep.style.CMS, "CMS"),
        (hep.style.LHCb, "LHCb"),
        (hep.style.LHCb1, "LHCb1"),
        (hep.style.LHCb2, "LHCb2"),
        (hep.style.ROOT, "ROOT"),
    ],
    ids=["ALICE", "ATLAS", "CMS", "LHCb", "LHCb1", "LHCb2", "ROOT"],
)
def test_use_style_style_list(fig_test, fig_ref, mplhep_style, str_alias):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use([mplhep_style, {"font.sans-serif": "Comic Sans MS"}])
    fig_ref.subplots()

    hep.rcParams.clear()
    hep.style.use([str_alias, {"font.sans-serif": "Comic Sans MS"}])
    fig_test.subplots()


@pytest.mark.mpl_image_compare(style="default")
def test_labeltext_loc():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for i, ax in enumerate(axs.flatten()):
        hep.cms.text("Test", loc=i, ax=ax)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_label_loc():
    fig, axs = plt.subplots(1, 5, figsize=(20, 4))
    for i, ax in enumerate(axs.flatten()):
        hep.cms.label("Preliminary", loc=i, ax=ax, lumi=50, data=True)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_pub_loc():
    fig, axs = plt.subplots(2, 5, figsize=(20, 8))
    for i, ax in enumerate(axs.flatten()):
        hep.cms.label(loc=i % 5, ax=ax, lumi=50, pub="arXiv:aaaa.bbbbb", data=(i >= 5))
    return fig


@check_figures_equal(extensions=["pdf"])
def test_label_config(fig_test, fig_ref):
    hep.rcParams.label.data = True
    hep.rcParams.label.lumi = 30
    hep.rcParams.label.label = "Internal"

    test_ax = fig_test.subplots()
    hep.cms.label(data=False, ax=test_ax)

    ref_ax = fig_ref.subplots()
    hep.rcParams.clear()
    hep.cms.label(data=False, lumi=30, label="Internal", ax=ref_ax)
