import os
from packaging import version
import matplotlib as mpl
import matplotlib.font_manager as fm

# Get helper functions
from . import cms
from . import atlas
from . import lhcb
from . import alice
from . import plot
from . import label

from ._tools import Config, FontLoader

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


# Make package fonts available to matplotlib
if version.parse(mpl.__version__) >= version.parse("3.2"):
    # mpl 3.2 and up
    html_font_path = "https://github.com/scikit-hep/mplhep/raw/master/src/mplhep/fonts/"
    FontLoader(
        html_font_path + "texgyreheros/texgyreheros-bolditalic.otf", persist=True
    ).prop
    FontLoader(
        html_font_path + "texgyreheros/texgyreheros-italic.otf", persist=True
    ).prop
    FontLoader(
        html_font_path + "texgyreheros/texgyreheros-regular.otf", persist=True
    ).prop
    FontLoader(
        html_font_path + "texgyreheros/texgyreheroscn-bold.otf", persist=True
    ).prop
    FontLoader(
        html_font_path + "texgyreheros/texgyreheroscn-bolditalic.otf", persist=True
    ).prop
    FontLoader(
        html_font_path + "texgyreheros/texgyreheroscn-italic.otf", persist=True
    ).prop
    FontLoader(html_font_path + "firasans/FiraMono-Bold.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraMono-Medium.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraMono-Regular.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-Black.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-BlackItalic.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-Bold.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-BoldItalic.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-ExtraBold.ttf", persist=True).prop
    FontLoader(
        html_font_path + "firasans/FiraSans-ExtraBoldItalic.ttf", persist=True
    ).prop
    FontLoader(html_font_path + "firasans/FiraSans-ExtraLight.ttf", persist=True).prop
    FontLoader(
        html_font_path + "firasans/FiraSans-ExtraLightItalic.ttf", persist=True
    ).prop
    FontLoader(html_font_path + "firasans/FiraSans-Italic.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-Light.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-LightItalic.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-Medium.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-MediumItalic.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-Regular.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-SemiBold.ttf", persist=True).prop
    FontLoader(
        html_font_path + "firasans/FiraSans-SemiBoldItalic.ttf", persist=True
    ).prop
    FontLoader(html_font_path + "firasans/FiraSans-Thin.ttf", persist=True).prop
    FontLoader(html_font_path + "firasans/FiraSans-ThinItalic.ttf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Bold.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Book.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-ExtraBold.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-ExtraLight.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Heavy.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Light.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Medium.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Regular.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-SemiBold.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Thin.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-Ultra.otf", persist=True).prop
    FontLoader(html_font_path + "firamath/FiraMath-UltraLight.otf", persist=True).prop
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
