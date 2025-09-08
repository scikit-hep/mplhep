"""
Ratio
=====

Compare two 1D histograms using the ratio [h1/h2].
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

name = "variable_1"

x1 = df[name][df["category"] == 2]
x2 = df[name][df["category"] == 3]

x_range = (min(*x1, *x2), max(*x1, *x2))

import hist
from hist import Hist

h1 = Hist(hist.axis.Regular(50, x_range[0], x_range[1]))
h2 = Hist(hist.axis.Regular(50, x_range[0], x_range[1]))

h1.fill(x1)
h2.fill(x2)

###
from mplhep import plot_two_hist_comparison

# Default comparison is ratio
fig, ax_main, ax_comparison = plot_two_hist_comparison(
    h1,
    h2,
    xlabel=name,
    ylabel="Entries",
    h1_label="h1",
    h2_label="h2",
)

fig.savefig("1d_comparison_ratio.svg", bbox_inches="tight")
