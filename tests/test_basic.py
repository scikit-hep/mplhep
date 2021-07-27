from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as hep  # noqa: E402

"""
To test run:
pytest --mpl

When adding new tests, run:
pytest --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_simple():
    fig, ax = plt.subplots(figsize=(10, 10))
    h = [1, 3, 2]
    bins = [0, 1, 2, 3]
    hep.histplot(h, bins, yerr=True, label="X")
    ax.legend()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_simple_xerr():
    fig, ax = plt.subplots(figsize=(10, 10))
    h = np.array([1, 3, 2])
    bins = [0, 1, 2, 4]
    hep.histplot(h, bins, yerr=True, histtype="errorbar")
    hep.histplot(h * 2, bins, yerr=True, histtype="errorbar", xerr=0.1)
    hep.histplot(h * 3, bins, yerr=True, histtype="errorbar", xerr=True)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_simple2d():
    fig, ax = plt.subplots()
    h = [[1, 3, 2], [1, 3, 2]]
    hep.hist2dplot(h)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_log():
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for ax in axs[0]:
        hep.histplot([1, 2, 3, 2], range(5), ax=ax)
    ax.semilogy()
    for ax in axs[1]:
        hep.histplot([1, 2, 3, 2], range(5), ax=ax, edges=False)
    ax.semilogy()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot(h, bins, ax=axs[0])

    axs[1].set_title("Plot No Edges", fontsize=18)
    hep.histplot(h, bins, edges=False, ax=axs[1])

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(h, bins, yerr=np.sqrt(h), ax=axs[2])

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot(h, bins, histtype="fill", ax=axs[3])

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_density():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot(h, bins, ax=axs[0], density=True)

    axs[1].set_title("Plot No Edges", fontsize=18)
    hep.histplot(h, bins, edges=False, ax=axs[1], density=True)

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(h, bins, yerr=np.sqrt(h), ax=axs[2], density=True)

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot(h, bins, histtype="fill", ax=axs[3], density=True)

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
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
    axs[3].legend(fontsize=16, prop={"family": "Tex Gyre Heros"})

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_stack():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 400), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    axs[0].set_title("Default", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, stack=True, ax=axs[0])

    axs[1].set_title("Plot No Edges", fontsize=18)
    hep.histplot([h, 1.5 * h], bins, edges=False, stack=True, ax=axs[1])

    axs[2].set_title("Plot Errorbars", fontsize=18)
    hep.histplot(
        [h, 1.5 * h], bins, yerr=[np.sqrt(h), np.sqrt(h)], stack=True, ax=axs[2]
    )

    axs[3].set_title("Filled Histogram", fontsize=18)
    hep.histplot([1.5 * h, h], bins, histtype="fill", stack=True, ax=axs[3])

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot():
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots()
    hep.hist2dplot(H, xedges, yedges, labels=True)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_inputs_nobin():
    np.random.seed(0)
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()
    hep.hist2dplot([[1, 2, 3]], ax=axs[0])
    hep.hist2dplot(np.array([[1, 2, 3]]), ax=axs[1])
    hep.hist2dplot([[1, 2, 3], [3, 4, 1]], ax=axs[2])
    hep.hist2dplot(np.array([[1, 2, 3], [3, 4, 1]]), ax=axs[3])
    return fig


@pytest.mark.parametrize("cbarextend", [False, True])
@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_cbar(cbarextend):
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots()
    hep.hist2dplot(H, xedges, yedges, labels=True, cbar=True, cbarextend=cbarextend)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_cbar_subplots():
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    hep.hist2dplot(H, xedges, yedges, labels=True, cbar=True, ax=ax1)
    hep.hist2dplot(H * 2, xedges, yedges, labels=True, cbar=True, ax=ax2)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_hist2dplot_custom_labels():
    np.random.seed(0)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    fig, ax = plt.subplots()

    @np.vectorize
    def _fmt(x):
        return f"${x:.2f}$"

    hep.hist2dplot(H, xedges, yedges, labels=_fmt(H))
    return fig


def test_hist2dplot_labels_option():
    """
    Test the functionality of hist2dplot's label options.
    """
    np.random.seed(0)

    x = np.random.normal(5, 1.5, 100)
    y = np.random.normal(4, 1, 100)
    xedges = np.arange(0, 11.5, 1.5)
    yedges = [0, 2, 3, 4, 6, 7]
    H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))

    assert hep.hist2dplot(H, xedges, yedges, labels=True)

    assert hep.hist2dplot(H, xedges, yedges, labels=False)

    label_array = np.chararray(H.shape, itemsize=2)
    label_array[:] = "hi"
    assert hep.hist2dplot(H, xedges, yedges, labels=label_array)

    label_array = np.chararray(H.shape[0], itemsize=2)
    label_array[:] = "hi"
    # Label array shape invalid
    with pytest.raises(ValueError):
        hep.hist2dplot(H, xedges, yedges, labels=label_array)

    # Invalid label type
    with pytest.raises(ValueError):
        hep.hist2dplot(H, xedges, yedges, labels=5)


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_kwargs():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 1000), bins=10)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
    axs = axs.flatten()

    hep.histplot(
        [h * 2, h * 1, h * 0.5],
        bins,
        label=["1", "2", "3"],
        stack=True,
        histtype="step",
        linestyle="--",
        color=["green", "black", (1, 0, 0, 0.4)],
        ax=axs[0],
    )
    axs[0].legend()

    hep.histplot(
        [h, h, h],
        bins,
        label=["1", "2", "3"],
        stack=True,
        histtype="step",
        linestyle=["--", ":"],
        color=(1, 0, 0, 0.8),
        ax=axs[1],
    )
    axs[1].legend()

    hep.histplot(
        [h, h, h],
        bins,
        label=["1", "2", "3"],
        histtype="step",
        binwnorm=[0.5, 3, 6],
        linestyle=["--", ":"],
        color=(1, 0, 0, 0.8),
        ax=axs[2],
    )
    axs[2].legend()

    hep.histplot(
        [h, h, h],
        bins,
        label=["1", "2", "3"],
        histtype="fill",
        binwnorm=[0.5, 3, 6],
        linestyle=["--", ":"],
        color=["green", "darkorange", "red"],
        alpha=[0.4, 0.7, 0.2],
        ax=axs[3],
    )
    axs[3].legend()

    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_real():
    np.random.seed(0)
    h, bins = np.histogram(np.random.normal(10, 3, 1000), bins=10)

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()
    a, b, c = h, h * 2, np.random.poisson(h * 3)

    hep.histplot(
        [a, b, c], bins=bins, ax=axs[0], yerr=True, label=["MC1", "MC2", "Data"]
    )
    hep.histplot([a, b], bins=bins, ax=axs[1], stack=True, label=["MC1", "MC2"])
    hep.histplot(
        [c], bins=bins, ax=axs[1], yerr=True, histtype="errorbar", label="Data"
    )

    hep.histplot(
        [a, b], bins=bins, ax=axs[2], stack=True, label=["MC1", "MC2"], binwnorm=[2, 1]
    )
    hep.histplot(
        c,
        bins=bins,
        ax=axs[2],
        yerr=True,
        histtype="errorbar",
        label="Data",
        binwnorm=1,
    )
    hep.histplot(
        [a, b], bins=bins, ax=axs[3], stack=True, label=["MC1", "MC2"], density=True
    )
    hep.histplot(
        c,
        bins=bins,
        ax=axs[3],
        yerr=True,
        histtype="errorbar",
        label="Data",
        density=True,
    )
    for ax in axs:
        ax.legend()
    axs[0].set_title("Raw")
    axs[1].set_title("Data/MC")
    axs[2].set_title("Data/MC binwnorm")
    axs[3].set_title("Data/MC Density")

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_w2():
    fig, ax = plt.subplots()
    hep.histplot([0, 3, 0], range(4), w2=np.array([0, 3, 0]))
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_types():
    hs, bins = [[2, 3, 4], [5, 4, 3]], [0, 1, 2, 3]
    fig, axs = plt.subplots(3, 2, figsize=(8, 12))
    axs = axs.flatten()

    for i, htype in enumerate(["step", "fill", "errorbar"]):
        hep.histplot(hs[0], bins, yerr=True, histtype=htype, ax=axs[i * 2], alpha=0.7)
        hep.histplot(hs, bins, yerr=True, histtype=htype, ax=axs[i * 2 + 1], alpha=0.7)

    return fig


h = np.geomspace(1, 10, 10)


@pytest.mark.parametrize("h", [h, [h, h], [h]])
@pytest.mark.parametrize("yerr", [h / 4, [h / 4, h / 4], 4])
@pytest.mark.parametrize("htype", ["step", "fill", "errorbar"])
def test_histplot_inputs_pass(h, yerr, htype):
    bins = np.linspace(1, 10, 11)

    fig, ax = plt.subplots()
    hep.histplot(h, bins, yerr=yerr, histtype=htype)
    plt.close(fig)
