"""
Comparison plotting module with shortened function names.

This module provides convenient aliases for comparison plotting functions
with shorter, more ergonomic names.
"""

from .comparison_plotters import (
    plot_comparison as ratio,
)
from .comparison_plotters import (
    plot_data_model_comparison as data_model,
)
from .comparison_plotters import (
    plot_model as model,
)
from .comparison_plotters import (
    plot_two_hist_comparison as hists,
)

# Alias the module name itself for discoverability
compare = __import__(__name__)

__all__ = [
    "hists",
    "ratio",
    "data_model",
    "model",
    "compare",
]
