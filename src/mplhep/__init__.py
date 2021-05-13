from __future__ import annotations

import os

import matplotlib.font_manager as fm
import mplhep_data

# Get styles directly, also available within experiment helpers.
# Get helper functions
from . import alice, atlas, cms, label, lhcb, plot
from . import styles as style
from ._tools import Config
from .label import savelabels
from .plot import (
    append_axes,
    box_aspect,
    hist2dplot,
    histplot,
    make_square_add_cbar,
    mpl_magic,
    rescale_to_axessize,
    save_variations,
    sort_legend,
    ylow,
    yscale_legend,
)
from .styles import set_style

## Configs
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

# Make __version__ available
_base_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_base_dir, ".VERSION")) as version_file:
    __version__ = version_file.read().strip()

path = os.path.abspath(__file__)
font_path = os.path.join(os.path.dirname(mplhep_data.__file__), "fonts")
font_files = fm.findSystemFonts(fontpaths=font_path)
for font in font_files:
    fm.fontManager.addfont(font)


# Log submodules
__all__ = [
    "cms",
    "atlas",
    "lhcb",
    "alice",
    "plot",
    "style",
    "label",
    "savelabels",
    # Log plot functions
    "histplot",
    "hist2dplot",
    "mpl_magic",
    "r_align",
    "yscale_legend",
    "ylow",
    "rescale_to_axessize",
    "box_aspect",
    "make_square_add_cbar",
    "append_axes",
    "sort_legend",
    "save_variations",
    "set_style",
]
