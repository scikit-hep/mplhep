"""
Difference
==========

Compare two 1D histograms using the difference [h1-h2].
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
from mplhep import add_text, plot_two_hist_comparison

fig, ax_main, ax_comparison = plot_two_hist_comparison(
    h1,
    h2,
    xlabel=name,
    ylabel="Entries",
    h1_label=r"$\mathcal{H}_{1}$",
    h2_label=r"$\mathcal{H}_{2}$",
    comparison="difference",  # <--
)

add_text(
    "Comparison of two hist with difference plot",
    ax=ax_main,
    fontsize="small",
    loc="over left",
)
add_text("Difference ax", ax=ax_comparison, loc="over right", fontsize="small")

fig.savefig("1d_comparison_difference.svg", bbox_inches="tight")
