"""
Difference
==========

Compare two 1D histograms using the difference [h1-h2].
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()  # noqa: PD901

name = "variable_1"

x1 = df[name][df["category"] == 2]
x2 = df[name][df["category"] == 3]

x_range = (min(*x1, *x2), max(*x1, *x2))

import hist  # noqa: E402
from hist import Hist  # noqa: E402

h1 = Hist(hist.axis.Regular(50, x_range[0], x_range[1]))
h2 = Hist(hist.axis.Regular(50, x_range[0], x_range[1]))

h1.fill(x1)
h2.fill(x2)

###
from mplhep import add_text, plot_two_hist_comparison  # noqa: E402

fig, ax_main, ax_comparison = plot_two_hist_comparison(
    h1,
    h2,
    xlabel=name,
    ylabel="Entries",
    h1_label=r"$\mathcal{H}_{1}$",
    h2_label=r"$\mathcal{H}_{2}$",
    comparison="difference",  # <--
)

add_text("Comparison of two hist with difference plot", ax=ax_main)
add_text("Difference ax", x="right", ax=ax_comparison)

fig.savefig("1d_comparison_difference.svg", bbox_inches="tight")
