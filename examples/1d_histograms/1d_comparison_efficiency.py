"""
Efficiency
==========

Compare the ratio between two histograms h1 and h2 when the entries of h1 are a subset of the entries of h2.
"""

import hist
import numpy as np
from hist import Hist

import mplhep as mh

np.random.seed(42)

# Generate dummy data - sample is subset of total
x_total = np.random.normal(0.4, 0.1, 10000)
x_sample = x_total[:7500]  # 75% subset

# Create and fill histograms
h_sample = Hist(
    hist.axis.Regular(50, 0, 1), storage=hist.storage.Weight()
)  # Long interface
h_total = hist.new.Regular(50, 0, 1).Weight()  # Shorthand interface
h_sample.fill(x_sample)
h_total.fill(x_total)

###
fig, ax_main, ax_comparison = mh.comp.hists(
    h_sample,
    h_total,
    xlabel="Variable",
    ylabel="Entries",
    h1_label=r"$h_{Sample}$",
    h2_label=r"$h_{Total}$",
    comparison="efficiency",  # <--
)

fig.savefig("1d_comparison_efficiency.svg", bbox_inches="tight")
