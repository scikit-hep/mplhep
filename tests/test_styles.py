import os
import sys
import pytest
import matplotlib.pyplot as plt
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


@pytest.mark.mpl_image_compare(style="default")
def test_label_loc():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for i, ax in enumerate(axs.flatten()):
        hep.cms.text("Test", loc=i, ax=ax)
    return fig
