"""
Data vs model with stacked components
=====================================

Plot data and a model with stacked components.
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

signal_scaling_factor = data_hist.sum().value / signal_hist.sum().value
signal_hist *= signal_scaling_factor

###
from mplhep import histplot, plot_data_model_comparison

fig, ax_main, ax_comparison = plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=background_categories_labels,
    stacked_colors=background_categories_colors,
    xlabel=key,
    ylabel="Entries",
)

# Signal histogram not part of the model and therefore not included in the comparison
histplot(
    signal_hist,
    ax=ax_main,
    color="red",
    label="Signal",
    histtype="step",
)

ax_main.legend()

fig.savefig("model_examples_stacked.svg", bbox_inches="tight")
