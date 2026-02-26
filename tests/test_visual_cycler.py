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
