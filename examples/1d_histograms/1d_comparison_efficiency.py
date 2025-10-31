"""
Efficiency
==========

Compare the ratio between two histograms h1 and h2 when the entries of h1 are a subset of the entries of h2.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
import hist
import numpy as np

import mplhep as mh

np.random.seed(42)
# --8<-- [end:imports]

# --8<-- [start:setup]
# Generate dummy data - sample is subset of total
x_total = np.random.normal(0.4, 0.1, 10000)
x_sample = x_total[:7500]  # 75% subset

# Create and fill histograms
h_sample = hist.new.Regular(50, 0, 1).Weight().fill(x_sample)
h_total = hist.new.Regular(50, 0, 1).Weight().fill(x_total)
# --8<-- [end:setup]

# --8<-- [start:plot_body]
fig, ax_main, ax_comparison = mh.comp.hists(
    h_sample,
    h_total,
    xlabel="Variable",
    ylabel="Entries",
    h1_label=r"$h_{Sample}$",
    h2_label=r"$h_{Total}$",
    comparison="efficiency",  # <--
)

# --8<-- [end:plot_body]
# --8<-- [end:full_code]
fig.savefig("1d_comparison_efficiency.png", bbox_inches="tight")
