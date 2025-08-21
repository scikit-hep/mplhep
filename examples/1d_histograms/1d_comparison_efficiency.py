"""
Efficiency
==========

Compare the ratio between two histograms h1 and h2 when the entries of h1 are a subset of the entries of h2.
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
from mplhep import plot_two_hist_comparison

fig, ax_main, ax_comparison = plot_two_hist_comparison(
    h_sample,
    h_total,
    xlabel=name,
    ylabel="Entries",
    h1_label=r"$\mathit{H}_{Sample}$",
    h2_label=r"$\mathit{H}_{Total}$",
    comparison="efficiency",  # <--
)

fig.savefig("1d_comparison_efficiency.svg", bbox_inches="tight")
