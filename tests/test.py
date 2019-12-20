import os
import pytest
import matplotlib.pyplot as plt
import numpy as np

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as hep # noqa

"""
To test run:
py.test --mpl

When adding new tests, run:
py.test --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


@pytest.mark.mpl_image_compare(style='default', remove_text=True)
def test_basic():
    fig, ax = plt.subplots(figsize=(10, 10))
    h = [1, 3, 2]
    bins = [0, 1, 2, 3]
    hep.histplot(h, bins, yerr=True, label='X')
    ax.legend()
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True)
def test_histplot():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot(h, bins, ax=axs[0])

    axs[1].set_title("Plot Edges", fontsize=18)
    hep.histplot(h, bins, edges=True, ax=axs[1])

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(h, bins, yerr=np.sqrt(h), ax=axs[2])

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot(h, bins, histtype='fill', ax=axs[3])

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True)
def test_histplot_density():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot(h, bins, ax=axs[0], density=True)

    axs[1].set_title("Plot Edges", fontsize=18)
    hep.histplot(h, bins, edges=True, ax=axs[1], density=True)

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(h, bins, yerr=np.sqrt(h), ax=axs[2], density=True)

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot(h, bins, histtype='fill', ax=axs[3], density=True)

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True)
def test_histplot_multiple():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default Overlay", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, ax=axs[0])

    axs[1].set_title("Default Overlay w/ Errorbars", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, yerr=[np.sqrt(h), np.sqrt(1.5 * h)], ax=axs[1])

    axs[2].set_title("Automatic Errorbars", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, yerr=True, ax=axs[2])

    axs[3].set_title("With Labels", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, yerr=True, ax=axs[3], label=["First", "Second"])
    axs[3].legend(fontsize=16, prop={'family': 'Tex Gyre Heros'})

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style='default', remove_text=True)
def test_histplot_stack():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, stack=True, ax=axs[0])

    axs[1].set_title("Plot Edges", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, edges=True, stack=True, ax=axs[1])

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, yerr=np.sqrt(h), stack=True, ax=axs[2])

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot([1.5 * h, h], bins, histtype='fill', stack=True, ax=axs[3])

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


# @pytest.mark.mpl_image_compare(style='default', remove_text=True)
def test_hist2dplot():
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))
    H = H.T

    fig, ax = plt.subplots()
    hep.hist2dplot(H, xedges, yedges, labels=True)
    return fig
