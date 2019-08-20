# Import counter
import requests as req

# Get helper functions
from . cms import cms
from . atlas import atlas

from . import tools

# Get styles directly, also available within experiment helpers.
from . import styles as sty

# Make package fonts available to matplotlib
import os
import matplotlib.font_manager as fm

path = os.path.abspath(__file__)
font_path = "/"+"/".join(path.split("/")[:-1])+"/fonts/"
font_files = fm.findSystemFonts(fontpaths=font_path)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)

# Log submodules
__all__ = [cms, atlas, sty, tools]

# Ping import counter for stats
#__ping__ = req.get("https://countimports.pythonanywhere.com/count/" +
#                   "tag.svg?url=https%3A%2F%2Fgithub.com%2Fandrzej" +
#                   "novak%2Fcmsstyle%2F")
__ping__ = req.get("https://countimports.pythonanywhere.com/count/" +
                   "tag.svg?url=count_hepstyle_imports")
