"""
Model with stacked and unstacked functional components
======================================================

Plot a model with stacked and unstacked functional components.
"""

key = "variable_1"
range = (-9, 12)

background_categories = [0, 1, 2]
background_categories_labels = [f"c{i}" for i in background_categories]


# Define some random functions that will be used as model components with functions
from scipy.stats import norm


def f_signal(x):
    return 1000 * norm.pdf(x, loc=0.5, scale=3)


def f_background1(x):
    return 1000 * norm.pdf(x, loc=-1.5, scale=4)


def f_background2(x):
    return 3000 * norm.pdf(x, loc=-1.8, scale=1.8)


###
from mplhep import add_text, plot_model

fig, ax = plot_model(
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

fig.savefig(
    "model_with_stacked_and_unstacked_function_components.svg", bbox_inches="tight"
)
