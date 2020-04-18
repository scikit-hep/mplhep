import os

# Import counter
import requests as req

from packaging import version
import matplotlib as mpl
import matplotlib.font_manager as fm

# Get helper functions
from . import cms
from . import atlas
from . import lhcb
from . import plot
from . import label

from . import tools

# Get styles directly, also available within experiment helpers.
from . import styles as style

from .plot import (
    histplot,
    hist2dplot,
    mpl_magic,
    r_align,
    yscale_legend,
    ylow,
    rescale_to_axessize,
    box_aspect,
    make_square_add_cbar,
    append_axes,
    sort_legend,
)

# Make __version__ available
try:
    _base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _base_dir = None

with open(os.path.join(_base_dir, ".VERSION")) as version_file:
    __version__ = version_file.read().strip()


# Make package fonts available to matplotlib
if version.parse(mpl.__version__) >= version.parse("3.2"):
    # mpl 3.2 and up
    path = os.path.abspath(__file__)
    font_path = "/".join(path.split("/")[:-1]) + "/fonts/"
    font_files = fm.findSystemFonts(fontpaths=font_path)
    for font in font_files:
        fm.fontManager.addfont(font)
else:
    # Back-comp for mpl<3.2
    # Deprecated in 3.2, removed in 3.3
    path = os.path.abspath(__file__)
    font_path = "/" + "/".join(path.split("/")[:-1]) + "/fonts/"
    font_files = fm.findSystemFonts(fontpaths=font_path)
    font_list = fm.createFontList(font_files)
    fm.fontManager.ttflist.extend(font_list)

# Log submodules
__all__ = [
    cms,
    atlas,
    lhcb,
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
