"""
Comparison
==========

Plot the comparison between two 1D histograms.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

name = "variable_1"

x_total = df[name][df["category"] == 2]
x_sample = x_total[: int(len(x_total) * 0.75)]

x_range = (min(x_total), max(x_total))

import hist
from hist import Hist

h_sample = Hist(hist.axis.Regular(50, x_range[0], x_range[1]))
h_total = Hist(hist.axis.Regular(50, x_range[0], x_range[1]))

h_sample.fill(x_sample)
h_total.fill(x_total)

###
import matplotlib.pyplot as plt

from mplhep import plot_comparison

fig, ax = plt.subplots()

plot_comparison(h_sample, h_total, ax=ax, xlabel=name, comparison="efficiency")

fig.savefig("1d_comparison_only_efficiency.svg", bbox_inches="tight")
