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
    "compare",
    "comparison",
    "data_model",
    "get_asymmetry",
    "get_comparison",
    "get_difference",
    "get_efficiency",
    "get_pull",
    "get_ratio",
    "hists",
    "plot_comparison",
    "plot_data_model_comparison",
    "plot_two_hist_comparison",
]
