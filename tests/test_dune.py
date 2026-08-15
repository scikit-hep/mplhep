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


# The DUNETex/DUNETex1 image tests live in tests/test_styles_latex.py, which
# owns the Tex styles. They used to be duplicated here verbatim, writing to the
# same tests/baseline/ files.


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@check_figures_equal(extensions=["pdf"])
@pytest.mark.parametrize(
    ("style", "str_alias"),
    [
        (mh.style.DUNE, "DUNE"),
        (mh.style.DUNE1, "DUNE1"),
    ],
    ids=["DUNE", "DUNE1"],
)
def test_dune_style_string_aliases(fig_test, fig_ref, style, str_alias):
    """Test that string aliases work for the DUNE style variants.

    The DUNETex/DUNETex1 aliases are covered by
    tests/test_styles_latex.py::test_latex_style_str_alias.
    """
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
        mh.dune.label(text="Preliminary", loc=i, ax=ax, lumi=50, data=True)
        ax.set_title(f"loc={i}")
    return fig
