from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.decorators import check_figures_equal

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as hep  # noqa: E402

plt.switch_backend("Agg")


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dune():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(hep.style.DUNE)
    fig, ax = plt.subplots()
    hep.dune.label(label="Preliminary")

    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_style_dune_logo():
    plt.rcParams.update(plt.rcParamsDefault)

    plt.style.use(hep.style.DUNE_LOGO)
    fig, ax = plt.subplots()
    hep.dune.label(label="Preliminary")

    plt.rcParams.update(plt.rcParamsDefault)
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize("mplhep_style", [hep.style.DUNE, hep.style.DUNE_LOGO])
def test_dune_style_variants(fig_test, fig_ref, mplhep_style):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use(mplhep_style)
    fig_ref.subplots()

    hep.rcParams.clear()
    hep.style.use(mplhep_style)
    fig_test.subplots()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    "mplhep_style, str_alias",
    [
        (hep.style.DUNE, "DUNE"),
        (hep.style.DUNE_LOGO, "DUNE_LOGO"),
    ],
    ids=["DUNE", "DUNE_LOGO"],
)
def test_dune_style_str_alias(fig_test, fig_ref, mplhep_style, str_alias):
    plt.rcParams.update(plt.rcParamsDefault)

    hep.rcParams.clear()
    plt.style.use(mplhep_style)
    fig_ref.subplots()

    hep.rcParams.clear()
    hep.style.use(str_alias)
    fig_test.subplots()


@pytest.mark.mpl_image_compare(style="default")
def test_dune_label_variants():
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))
    axs = axs.flatten()
    
    # Test each type of label
    hep.dune.preliminary(ax=axs[0])
    axs[0].set_title("preliminary")
    
    hep.dune.wip(ax=axs[1])
    axs[1].set_title("wip")
    
    hep.dune.simulation(ax=axs[2])
    axs[2].set_title("simulation")
    
    hep.dune.official(ax=axs[3])
    axs[3].set_title("official")
    
    hep.dune.simulation_side(ax=axs[4])
    axs[4].set_title("simulation_side")
    
    hep.dune.corner_label("Test Corner Label", ax=axs[5])
    axs[5].set_title("corner_label")
    
    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_dune_label_loc():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for i, ax in enumerate(axs.flatten()):
        hep.dune.label(label="Preliminary", loc=i, ax=ax, lumi=50, data=True)
        ax.set_title(f"loc={i}")
    return fig