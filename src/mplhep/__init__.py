import os
from packaging import version
import matplotlib as mpl
import matplotlib.font_manager as fm

import mplhep_data

# Get helper functions
from . import cms
from . import atlas
from . import lhcb
from . import alice
from . import plot
from . import label

from ._tools import Config

# Get styles directly, also available within experiment helpers.
from . import styles as style
from .styles import set_style

from .plot import (
    histplot,
    hist2dplot,
    mpl_magic,
    yscale_legend,
    ylow,
    rescale_to_axessize,
    box_aspect,
    make_square_add_cbar,
    append_axes,
    sort_legend,
    save_variations,
)

## Configs
rcParams = Config(
    label=Config(
        data=None,
        paper=None,
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
]
