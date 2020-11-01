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


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_inputs_basic():
    np.random.seed(0)
    H = np.histogram(np.random.normal(5, 2, 1000), bins=np.arange(0, 10, 1))
    h, bins = H

    fig, ax = plt.subplots()
    hep.histplot(H, label="tuple", ls="--")
    H = (h * 2, bins)
    hep.histplot(H, label="unwrap", ls=":")
    hep.histplot(h * 3, bins, label="split")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_inputs_uproot():
    import uproot4
    from skhep_testdata import data_path

    fname = data_path("uproot-hepdata-example.root")
    f = uproot4.open(fname)

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    TH1, TH2 = f["hpx"], f["hpxpy"]
    hep.histplot(TH1, ax=axs[0])
    hep.hist2dplot(TH2, ax=axs[1], cbar=False)

    return fig


@check_figures_equal()
def test_uproot_versions(fig_test, fig_ref):
    import uproot
    import uproot4
    from skhep_testdata import data_path

    fname = data_path("uproot-hepdata-example.root")
    f4 = uproot4.open(fname)
    f3 = uproot.open(fname)

    fig_test.set_size_inches(14, 5)
    fig_ref.set_size_inches(14, 5)

    test_axs = fig_test.subplots(1, 2)
    TH1u4, TH2u4 = f4["hpx"], f4["hpxpy"]
    hep.histplot(TH1u4, ax=test_axs[0])
    hep.hist2dplot(TH2u4, ax=test_axs[1], cbar=False)

    ref_axs = fig_ref.subplots(1, 2)
    TH1u3, TH2u3 = f3["hpx"], f3["hpxpy"]
    hep.histplot(TH1u3, ax=ref_axs[0])
    hep.hist2dplot(TH2u3, ax=ref_axs[1], cbar=False)


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_inputs_bh():
    import boost_histogram as bh

    hist2d = bh.Histogram(bh.axis.Regular(10, 0.0, 1.0), bh.axis.Regular(10, 0, 1))
    hist2d.fill(np.random.normal(0.5, 0.2, 1000), np.random.normal(0.5, 0.2, 1000))

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    hep.histplot(hist2d.project(0), ax=axs[0])
    hep.hist2dplot(hist2d, labels=True, cbar=False, ax=axs[1])

    return fig
