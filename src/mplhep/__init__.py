"""
Primary namespace for mplhep. Holds primary plotting and most common functions.
"""

from __future__ import annotations

import os

import matplotlib.font_manager as fm
import mplhep_data

# Get styles directly, also available within experiment helpers.
# Get helper functions
from . import comp, label, plot
from . import exp_alice as alice
from . import exp_atlas as atlas
from . import exp_cms as cms
from . import exp_dune as dune
from . import exp_lhcb as lhcb
from . import styles as style
from ._tools import Config
from ._utils import (
    EnhancedPlottableHistogram,
    _check_counting_histogram,
)
from ._utils import (
    _get_plottables as get_plottables,
)
from ._utils import (
    _make_plottable_histogram as make_plottable_histogram,
)
from ._version import version as __version__  # noqa: F401
from .label import add_text, append_text, save_variations, savelabels
from .plot import (
    funcplot,
    hist,
    hist2dplot,
    histplot,
    model,
)

plot_model = model

plot_hist = histplot
from .styles import set_style
from .utils import (
    append_axes,
    box_aspect,
    make_square_add_cbar,
    merge_legend_handles_labels,
    mpl_magic,
    rescale_to_axessize,
    set_fitting_ylabel_fontsize,
    set_ylow,
    sort_legend,
    subplots,
    yscale_anchored_text,
    yscale_legend,
)

# Configs
rcParams = Config(
    label=Config(
        text=None,
        data=None,
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
    "add_text",
    "alice",
    "append_axes",
    "append_text",
    "atlas",
    "box_aspect",
    "cms",
    "comp",
    "dune",
    "funcplot",
    "get_plottables",
    "hist",
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
    "model",
    "plot_hist",
    "plot_model",
    "rescale_to_axessize",
    "save_variations",
    "savelabels",
    "set_fitting_ylabel_fontsize",
    "set_style",
    "set_ylow",
    "sort_legend",
    "style",
    "yscale_anchored_text",
    "yscale_legend",
    "subplots",
]
