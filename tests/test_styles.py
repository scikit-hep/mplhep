import os
import sys
import pytest
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal
import numpy as np

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as hep  # noqa

"""
To test run:
py.test --mpl

When adding new tests, run:
py.test --mpl-generate-path=tests/baseline
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
    hep.atlas.text()

    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_cms():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots()
    hep.cms.text()

    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_alice():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(hep.style.ALICE)
    fig, ax = plt.subplots()
    hep.alice.text()

    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_lhcb():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use([hep.style.LHCb, {"figure.autolayout": False}])
    fig, ax = plt.subplots()
    # Doesn't work for now
    # hep.lhcb.text()
    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@check_figures_equal(extensions=["pdf"])
# @pytest.mark.parametrize(
#     "experiment_style",
#     [hep.style.ALICE, hep.style.ATLAS, hep.style.CMS, hep.style.LHCb, hep.style.ROOT,],
#     ids=["ALICE", "ATLAS", "CMS", "LHCb", "ROOT"],
# )
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
# def test_set_style(experiment_style, fig_test, fig_ref):
def test_set_style(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use(hep.style.CMS)
    ref_ax = fig_ref.subplots()

    hep.rcParams.clear()
    hep.set_style(hep.style.CMS)
    test_ax = fig_test.subplots()


@check_figures_equal(extensions=["pdf"])
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_set_style_str_alias(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use(hep.style.ATLAS)
    ref_ax = fig_ref.subplots()

    hep.rcParams.clear()
    hep.set_style("ATLAS")
    test_ax = fig_test.subplots()


@check_figures_equal(extensions=["pdf"])
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_set_style_self_consistent(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    hep.set_style(hep.style.LHCb)
    ref_ax = fig_ref.subplots()

    hep.rcParams.clear()
    hep.set_style("LHCb")
    test_ax = fig_test.subplots()


@check_figures_equal(extensions=["pdf"])
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_set_style_style_list(fig_test, fig_ref):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use([hep.style.CMS, {"font.sans-serif": "Comic Sans MS"}])
    ref_ax = fig_ref.subplots()

    hep.rcParams.clear()
    hep.set_style(["CMS", {"font.sans-serif": "Comic Sans MS"}])
    test_ax = fig_test.subplots()


@pytest.mark.mpl_image_compare(style="default")
def test_label_loc():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for i, ax in enumerate(axs.flatten()):
        hep.cms.text("Test", loc=i, ax=ax)
    return fig


@check_figures_equal(extensions=["pdf"])
def test_label_config(fig_test, fig_ref):
    hep.rcParams.label.data = True
    hep.rcParams.label.lumi = 30
    hep.rcParams.label.paper = True

    test_ax = fig_test.subplots()
    hep.cms.label(data=False, ax=test_ax)

    ref_ax = fig_ref.subplots()
    hep.rcParams.clear()
    hep.cms.label(data=False, lumi=30, paper=True, ax=ref_ax)
