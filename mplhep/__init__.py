# Import counter
import os

import matplotlib.font_manager as fm
import requests as req

from . import atlas
from . import cms
from . import label
from . import plot
from . import styles as style
from . import tools
from .plot import append_axes
from .plot import box_aspect
from .plot import hist2dplot
from .plot import histplot
from .plot import make_square_add_cbar
from .plot import mpl_magic
from .plot import r_align
from .plot import rescale_to_axessize
from .plot import sort_legend
from .plot import ylow
from .plot import yscale_legend
# Get helper functions
# Get styles directly, also available within experiment helpers.
# Make package fonts available to matplotlib

path = os.path.abspath(__file__)
font_path = "/" + "/".join(path.split("/")[:-1]) + "/fonts/"
font_files = fm.findSystemFonts(fontpaths=font_path)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)

# Log submodules
__all__ = [
    cms,
    atlas,
    plot,
    style,
    tools,
    label,
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

# Ping import counter for stats
# Check if CI
istravis = os.environ.get("TRAVIS") == "true"
isactions = os.environ.get("GITHUB_ACTIONS") == "true"
istests = os.environ.get("RUNNING_PYTEST") == "true"
if not (istravis | isactions | istests):
    try:
        # This exists solely to justify my work on the package
        # to my boss. If you have concerns, feel free to open
        # an issue
        __ping__ = req.get(
            "https://countimports.pythonanywhere.com/"
            "count/tag.svg?url=count_mplhep_imports",
            timeout=1,
        )
    except Exception:
        pass
