from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import mplhep as mh

plt.switch_backend("Agg")


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_cycler():
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = ["#e42536", "#5790fc", "#964a8b"]
    lines = ["solid", "dashed", "dotted"]
    custom_cycler = mpl.cycler(color=colors) + mpl.cycler(linestyle=lines)
    ax.set_prop_cycle(custom_cycler)

    h1 = [1, 3, 2]
    h2 = [2, 1, 3]
    h3 = [3, 2, 1]
    bins = [0, 1, 2, 3]

    mh.histplot(h1, bins, ax=ax, label="h1")
    mh.histplot(h2, bins, ax=ax, label="h2")
    mh.histplot(h3, bins, ax=ax, label="h3")

    ax.legend()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_stack_cycler():
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = ["#e42536", "#5790fc"]
    lines = ["solid", "dashed"]
    custom_cycler = mpl.cycler(color=colors) + mpl.cycler(linestyle=lines)
    ax.set_prop_cycle(custom_cycler)

    h1 = [1, 3, 2]
    h2 = [2, 1, 3]
    bins = [0, 1, 2, 3]

    mh.histplot([h1, h2], bins, stack=True, ax=ax, label=["h1", "h2"])

    ax.legend()
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_histplot_linestyle_tuple_viz():
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    h1 = [1, 3, 2]
    h2 = [2, 1, 3]
    bins = [0, 1, 2, 3]

    # 1. Single histogram with linestyle tuple
    axs[0].set_title("Single hist w/ tuple")
    mh.histplot(h1, bins, ax=axs[0], linestyle=(0, (3, 5, 1, 5)), label="tuple")

    # 2. Multiple histograms with broadcasting
    axs[1].set_title("Multiple hists w/ broadcast tuple")
    mh.histplot([h1, h2], bins, ax=axs[1], linestyle=(5, (10, 3)), label=["h1", "h2"])

    # 3. Multiple histograms with distribution (list of tuples)
    axs[2].set_title("Multiple hists w/ list of tuples")
    ls_list = [(0, (3, 5)), (0, (1, 1))]
    mh.histplot(
        [h1, h2], bins, ax=axs[2], linestyle=ls_list, label=["tuple 1", "tuple 2"]
    )

    # 4. Mix of string and tuple
    axs[3].set_title("Mix of string and tuple")
    mh.histplot(
        [h1, h2],
        bins,
        ax=axs[3],
        linestyle=["-", (0, (5, 5))],
        label=["string", "tuple"],
    )

    for ax in axs:
        ax.legend()

    fig.tight_layout()
    return fig
