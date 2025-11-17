"""
Data vs model with stacked components
=====================================

Plot data and a model with stacked components.
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
# Create data histogram
data_hist = hist.new.Regular(50, -8, 8).Weight()
data_hist.fill(
    np.concatenate(
        [
            np.random.normal(0, 2, 3000),
            np.random.normal(-3, 0.8, 1500),
            np.random.normal(-2, 1.5, 1200),
            np.random.normal(0, 0.5, 500),
        ]
    )
)

# Create background histograms
background_hists = [
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(0, 2, 3500)),
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(-3, 0.8, 1800)),
    hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(-2, 1.5, 1400)),
]

# Scale backgrounds to match data
scale = data_hist.sum().value / sum(background_hists).sum().value
background_hists = [scale * h for h in background_hists]

# Create signal histogram (not part of the model)
signal_hist = hist.new.Regular(50, -8, 8).Weight().fill(np.random.normal(-1, 0.5, 400))
# --8<-- [end:setup]

# --8<-- [start:plot_body]
fig, ax_main, ax_comparison = mh.comp.data_model(
    data_hist=data_hist,
    stacked_components=background_hists,
    stacked_labels=["c0", "c1", "c2"],
    stacked_colors=sns.color_palette("cubehelix", 3),
    xlabel="Observable",
    ylabel="Entries",
)

# Signal histogram not part of the model and therefore not included in the comparison
mh.histplot(signal_hist, ax=ax_main, color="red", label="Signal", histtype="step")
ax_main.legend()
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig("model_examples_stacked.svg", bbox_inches="tight")
