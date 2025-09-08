"""
Data vs functional model
========================

Compare data and model with stacked and unstacked functional components.
"""

from plothist_utils import get_dummy_data

df = get_dummy_data()

# Define the histograms

key = "variable_1"
range = (-9, 12)
category = "category"

# Define masks
data_mask = df[category] == 8

# Make histograms
import hist
from hist import Hist

axis = hist.axis.Regular(50, range[0], range[1])
data_hist = Hist(axis, storage=hist.storage.Weight())
data_hist.fill(df[key][data_mask])

# Define some random functions that will be used as model components with functions
from scipy.stats import norm


def f_signal(x):
    return 1000 * norm.pdf(x, loc=0.5, scale=3)


def f_background1(x):
    return 1000 * norm.pdf(x, loc=-1.5, scale=4)


def f_background2(x):
    return 3000 * norm.pdf(x, loc=-1.8, scale=1.8)


###
from mplhep import plot_data_model_comparison

fig, ax_main, ax_comparison = plot_data_model_comparison(
    data_hist=data_hist,
    stacked_components=[f_background1, f_background2],
    stacked_labels=["c0", "c1"],
    unstacked_components=[f_signal],
    unstacked_labels=["Signal"],
    unstacked_colors=["#8EBA42"],
    xlabel=key,
    ylabel="Entries",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    comparison="pull",
)

fig.savefig(
    "ratio_data_vs_model_with_stacked_and_unstacked_function_components.svg",
    bbox_inches="tight",
)
