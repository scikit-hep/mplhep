"""
Relative difference
===================

Compare two 1D histograms using the relative difference [(h1-h2)/h2].
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
import hist
import numpy as np

import mplhep as mh

np.random.seed(42)
# --8<-- [end:imports]

# --8<-- [start:setup]
# Generate dummy data
x1 = np.r_[np.random.normal(0.4, 0.1, 5000), np.random.normal(0.7, 0.1, 5000)]
x2 = np.r_[np.random.normal(0.4, 0.1, 1000), np.random.normal(0.7, 0.11, 7000)]

# Create and fill histograms
h1 = hist.new.Regular(50, 0, 1).Weight().fill(x1)
h2 = hist.new.Regular(50, 0, 1).Weight().fill(x2)
# --8<-- [end:setup]

# --8<-- [start:plot_body]
fig, ax_main, ax_comparison = mh.comp.hists(
    h1,
    h2,
    xlabel="Variable",
    ylabel="Entries",
    h1_label=r"$h_1$",
    h2_label=r"$h_2$",
    comparison="relative_difference",  # <--
)

# --8<-- [end:plot_body]
# --8<-- [end:full_code]
fig.savefig("1d_comparison_relative_difference.svg", bbox_inches="tight")
