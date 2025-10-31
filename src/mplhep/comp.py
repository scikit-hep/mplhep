"""
Comparison/compound plotting module.

This module provides functions to create comparison plots, such as ratio plots,
data vs. model comparisons, and more.
"""

from .comparison_plotters import (
    comparison,
    data_model,
    hists,
)

# Alias functions for plothist consistency
plot_comparison = comparison
plot_data_model_comparison = data_model
plot_two_hist_comparison = hists

from .comparison_functions import (
    get_asymmetry,
    get_comparison,
    get_difference,
    get_efficiency,
    get_pull,
    get_ratio,
)

# Alias the module name itself for discoverability
compare = __import__(__name__)

__all__ = [
    "hists",
    "plot_two_hist_comparison",
    "comparison",
    "plot_comparison",
    "data_model",
    "plot_data_model_comparison",
    "compare",
    "get_ratio",
    "get_difference",
    "get_efficiency",
    "get_pull",
    "get_comparison",
    "get_asymmetry",
]
