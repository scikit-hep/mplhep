"""
Data vs functional model
========================

Compare data and model with stacked and unstacked functional components.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
import hist
import numpy as np
from scipy.stats import norm

import mplhep as mh

np.random.seed(42)
# --8<-- [end:imports]


# --8<-- [start:setup]
# Create data histogram
data_hist = hist.new.Regular(50, -8, 8).Weight()
data_hist.fill(
    np.concatenate(
        [
            np.random.normal(0, 2, 3500),
            np.random.normal(-3, 1, 2000),
            np.random.normal(5, 0.5, 200),
        ]
    )
)
_binwidth = data_hist.axes[0].widths[0]


# Define model function components
def f_signal(x):
    return 200 * _binwidth * norm.pdf(x, loc=5, scale=0.5)


def f_background1(x):
    return 3500 * _binwidth * norm.pdf(x, loc=0, scale=2)


def f_background2(x):
    return 2000 * _binwidth * norm.pdf(x, loc=-3, scale=1)


# --8<-- [end:setup]

# --8<-- [start:plot_body]
fig, ax_main, ax_comparison = mh.comp.data_model(
    data_hist=data_hist,
    stacked_components=[f_background1, f_background2],
    stacked_labels=["c0", "c1"],
    unstacked_components=[f_signal],
    unstacked_labels=["Signal"],
    unstacked_colors=["#8EBA42"],
    xlabel="Observable",
    ylabel="Entries",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    comparison="pull",
)
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig(
    "ratio_data_vs_model_with_stacked_and_unstacked_function_components.svg",
    bbox_inches="tight",
)
