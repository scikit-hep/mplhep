"""
Comparison
==========

Plot the comparison between two 1D histograms.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
import hist
import matplotlib.pyplot as plt
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
fig, ax = plt.subplots()
mh.comp.comparison(h_sample, h_total, ax=ax, xlabel="Variable", comparison="efficiency")

# --8<-- [end:plot_body]
# --8<-- [end:full_code]
fig.savefig("1d_comparison_only_efficiency.svg", bbox_inches="tight")
