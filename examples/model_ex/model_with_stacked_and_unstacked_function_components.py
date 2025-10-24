"""
Model with stacked and unstacked functional components
======================================================

Plot a model with stacked and unstacked functional components.
"""

# --8<-- [start:full_code]
# --8<-- [start:imports]
key = "variable_1"
range = (-9, 12)

background_categories = [0, 1, 2]
background_categories_labels = [f"c{i}" for i in background_categories]


# Define some random functions that will be used as model components with functions
from scipy.stats import norm

# --8<-- [end:imports]


# --8<-- [start:setup]
def f_signal(x):
    return 1000 * norm.pdf(x, loc=0.5, scale=3)


def f_background1(x):
    return 1000 * norm.pdf(x, loc=-1.5, scale=4)


def f_background2(x):
    return 3000 * norm.pdf(x, loc=-1.8, scale=1.8)


# --8<-- [end:setup]

# --8<-- [start:plot_body]
###
from mplhep import add_text, model

fig, ax = model(
    stacked_components=[f_background1, f_background2],
    stacked_labels=background_categories_labels[:2],
    unstacked_components=[f_signal],
    unstacked_labels=["Signal"],
    unstacked_colors=["black"],
    xlabel=key,
    ylabel=f"f({key})",
    model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
    function_range=range,
)

add_text("Model made of functions", ax=ax, loc="over left", fontsize="small")
# --8<-- [end:plot_body]

# --8<-- [end:full_code]
fig.savefig(
    "model_with_stacked_and_unstacked_function_components.svg", bbox_inches="tight"
)
