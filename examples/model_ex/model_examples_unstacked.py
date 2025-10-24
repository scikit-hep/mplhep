"""
Data vs model with unstacked components
=====================================

Plot data and a model with unstacked components.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
from plothist_utils import get_dummy_data

df = get_dummy_data()

import seaborn as sns

# --8<-- [end:imports]

# --8<-- [start:setup]
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
# --8<-- [end:setup]

# --8<-- [start:plot_body]
###
from mplhep import data_model

fig, ax_main, ax_comparison = data_model(
    data_hist=data_hist,
    unstacked_components=background_hists,
    unstacked_labels=background_categories_labels,
    unstacked_colors=background_categories_colors,
    xlabel=key,
    ylabel="Entries",
    model_sum_kwargs={"label": "Sum(hists)", "color": "navy"},
    comparison_ylim=[0.5, 1.5],
)
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig("model_examples_unstacked.svg", bbox_inches="tight")
