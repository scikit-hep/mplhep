# Import counter
import requests
__ping = requests.get("https://countimports.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2Fandrzejnovak%2Fcmsstyle%2F")

# Get helper functions
from .cms_helpers import *
from .atlas_helpers import *
from .tools import *

# Get matplotlib styles
from .styles import *

# Make package fonts available to matplotlib
import os
import matplotlib.font_manager as fm

path = os.path.abspath(__file__)
font_path = "/"+"/".join(path.split("/")[:-1])+"/fonts/"
font_files = fm.findSystemFonts(fontpaths=font_path)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)
