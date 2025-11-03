"""
Model with stacked and unstacked components
===========================================

Plot a model with stacked and unstacked components.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
import hist
import numpy as np
import seaborn as sns

import mplhep as mh

np.random.seed(42)
# --8<-- [end:imports]

# --8<-- [start:setup]
# Create background histograms
background_hists = [
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(0, 2, 3500)),
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(-3, 0.8, 1800)),
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(-2, 1.5, 1400)),
]

# Create signal histogram
signal_hist = hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(0, 0.5, 500))
# --8<-- [end:setup]

# --8<-- [start:plot_body]
fig, ax = mh.model(
    stacked_components=background_hists,
    stacked_labels=["c0", "c1", "c2"],
    stacked_colors=sns.color_palette("cubehelix", 3),
    unstacked_components=[signal_hist],
    unstacked_labels=["Signal"],
    unstacked_colors=["black"],
    unstacked_kwargs_list=[{"linestyle": "dotted"}],
    xlabel="Observable",
    ylabel="Entries",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    model_uncertainty_label="Stat. unc.",
)

mh.add_text("Model made of histograms", ax=ax, loc="over left")
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig(
    "model_with_stacked_and_unstacked_histograms_components.svg",
    bbox_inches="tight",
)
