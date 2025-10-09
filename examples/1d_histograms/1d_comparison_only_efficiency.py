"""
Comparison
==========

Plot the comparison between two 1D histograms.
"""

import hist
import matplotlib.pyplot as plt
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
fig, ax = plt.subplots()

mh.comp.ratio(h_sample, h_total, ax=ax, xlabel="Variable", comparison="efficiency")

fig.savefig("1d_comparison_only_efficiency.svg", bbox_inches="tight")
