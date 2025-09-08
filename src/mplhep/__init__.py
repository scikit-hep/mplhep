from __future__ import annotations

import os

import matplotlib.font_manager as fm
import mplhep_data

# Get styles directly, also available within experiment helpers.
# Get helper functions
from . import alice, atlas, cms, dune, label, lhcb, plot
from . import styles as style
from ._tools import Config
from ._version import version as __version__  # noqa: F401
from .comparison import (
    get_asymmetry,
    get_comparison,
    get_difference,
    get_efficiency,
    get_pull,
    get_ratio,
)
from .comparison_plotters import (
    create_comparison_figure,
    plot_comparison,
    plot_data_model_comparison,
    plot_model,
    plot_two_hist_comparison,
)
from .label import add_luminosity, add_text, save_variations, savelabels
from .palettes import get_color_palette
from .plot import (
    append_axes,
    box_aspect,
    hist2dplot,
    histplot,
    make_square_add_cbar,
    merge_legend_handles_labels,
    mpl_magic,
    rescale_to_axessize,
    sort_legend,
    ylow,
    yscale_anchored_text,
    yscale_legend,
)
from .styles import set_style
from .utils import (
    EnhancedPlottableHistogram,
    _check_counting_histogram,
    get_plottables,
    make_plottable_histogram,
    set_fitting_ylabel_fontsize,
)

# Configs
rcParams = Config(
    label=Config(
        data=None,
        kind=None,
        supplementary=None,
        year=None,
        lumi=None,
        llabel=None,
        rlabel=None,
    ),
    text=Config(
        text=None,
    ),
)

path = os.path.abspath(__file__)
font_path = os.path.join(os.path.dirname(mplhep_data.__file__), "fonts")
font_files = fm.findSystemFonts(fontpaths=font_path)
for font in font_files:
    fm.fontManager.addfont(font)


# Log submodules
__all__ = [
    "EnhancedPlottableHistogram",
    "_check_counting_histogram",
    "add_text",
    "alice",
    "append_axes",
    "atlas",
    "box_aspect",
    "cms",
    "dune",
    "get_asymmetry",
    "get_comparison",
    "get_difference",
    "get_efficiency",
    "get_color_palette",
    "get_plottables",
    "get_pull",
    "get_ratio",
    "plot_comparison",
    "plot_two_hist_comparison",
    "plot_model",
    "plot_data_model_comparison",
    "hist2dplot",
    # Log plot functions
    "histplot",
    "label",
    "lhcb",
    "make_plottable_histogram",
    "make_square_add_cbar",
    "merge_legend_handles_labels",
    "mpl_magic",
    "plot",
    "rescale_to_axessize",
    "save_variations",
    "savelabels",
    "set_style",
    "sort_legend",
    "style",
    "ylow",
    "yscale_anchored_text",
    "yscale_legend",
    "get_color_palette",
    "add_text",
    "add_luminosity",
    "create_comparison_figure",
    "set_fitting_ylabel_fontsize",
]
