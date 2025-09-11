"""
Data/model comparisons, no model uncertainty
============================================

All supported comparisons between data and model, without model uncertainty.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

import seaborn as sns

# Define the histograms

key = "variable_1"
x_range = (-9, 12)
category = "category"

# Define masks
signal_mask = df[category] == 7
data_mask = df[category] == 8

background_categories = [0, 1, 2]
background_categories_labels = [f"c{i}" for i in background_categories]
background_categories_colors = sns.color_palette(
    "cubehelix", len(background_categories)
)

background_masks = [df[category] == p for p in background_categories]

# Make histograms
import hist
from hist import Hist

axis = hist.axis.Regular(50, x_range[0], x_range[1])

data_hist = Hist(axis, storage=hist.storage.Weight())
signal_hist = Hist(axis, storage=hist.storage.Weight())
background_hists = []

data_hist.fill(df[key][data_mask])
signal_hist.fill(df[key][signal_mask])

for mask in background_masks:
    h_bkg = Hist(axis, storage=hist.storage.Weight())
    h_bkg.fill(df[key][mask])
    background_hists.append(h_bkg)

# Optional: scale to data
background_scaling_factor = data_hist.sum().value / sum(background_hists).sum().value
background_hists = [background_scaling_factor * h for h in background_hists]

###
import matplotlib.pyplot as plt
import numpy as np

from mplhep import (
    add_text,
    plot_comparison,
    plot_data_model_comparison,
    set_fitting_ylabel_fontsize,
)

fig, axes = plt.subplots(
    nrows=6,
    figsize=(6, 13),
    gridspec_kw={"height_ratios": [3, 1, 1, 1, 1, 1]},
)
fig.subplots_adjust(hspace=0.3)
for ax in axes[:-1]:
    ax.xaxis.set_ticklabels([])
    ax.set_xlabel(" ")
background_sum = sum(background_hists)

plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=background_categories_labels,
    stacked_colors=background_categories_colors,
    xlabel="",
    ylabel="Entries",
    model_uncertainty=False,  # <--
    comparison="ratio",
    fig=fig,
    ax_main=axes[0],
    ax_comparison=axes[1],
)

add_text(
    r"Multiple data-model comparisons, $\mathbf{without}$ model uncertainty",
    ax=axes[0],
    loc="over left",
    fontsize="small",
)
add_text(
    r'  $\mathbf{→}$ comparison = "ratio"', ax=axes[1], loc="over left", fontsize=13
)

for k_comp, comparison in enumerate(
    ["split_ratio", "pull", "relative_difference", "difference"], start=2
):
    ax_comparison = axes[k_comp]

    # Copy the original histogram and set the uncertainties of the copy to 0.
    background_sum_copy = background_sum.copy()
    background_sum_copy[:] = np.c_[
        background_sum_copy.values(), np.zeros_like(background_sum_copy.values())
    ]

    plot_comparison(
        data_hist,
        background_sum_copy,
        ax=ax_comparison,
        comparison=comparison,
        xlabel="",
        h1_label="Data",
        h2_label="Pred.",
        h1_w2method="poisson",
    )
    if comparison == "pull":
        # Since the uncertainties of the model are neglected, the pull label is "(Data - Pred.)/sigma_Data"
        ax_comparison.set_ylabel(r"$\frac{Data-Pred.}{\sigma_{Data}}$")
    add_text(
        rf'  $\mathbf{{→}}$ comparison = "{comparison}"',
        ax=ax_comparison,
        loc="over left",
        fontsize=13,
    )
    set_fitting_ylabel_fontsize(ax_comparison)

axes[-1].set_xlabel(key)

fig.savefig("model_all_comparisons_no_model_unc.svg", bbox_inches="tight")
