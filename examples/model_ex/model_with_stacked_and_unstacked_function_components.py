"""
Model with stacked and unstacked functional components
======================================================

Plot a model with stacked and unstacked functional components.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
from scipy.stats import norm

import mplhep as mh

# --8<-- [end:imports]


# --8<-- [start:setup]
# Define model function components
def f_signal(x):
    return 600 * norm.pdf(x, loc=0.2, scale=3)


def f_background1(x):
    return 1000 * norm.pdf(x, loc=-1.5, scale=4)


def f_background2(x):
    return 3000 * norm.pdf(x, loc=-3.2, scale=1.2)


# --8<-- [end:setup]

# --8<-- [start:plot_body]
fig, ax = mh.model(
    stacked_components=[f_background1, f_background2],
    stacked_labels=["c0", "c1"],
    unstacked_components=[f_signal],
    unstacked_labels=["Signal"],
    unstacked_colors=["black"],
    xlabel="Observable",
    ylabel="f(Observable)",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    function_range=(-9, 12),
)

mh.add_text("Model made of functions", ax=ax, loc="over left", fontsize="small")
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig(
    "model_with_stacked_and_unstacked_function_components.svg", bbox_inches="tight"
)
