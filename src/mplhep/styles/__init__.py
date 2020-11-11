import sys

from matplotlib.pyplot import style as plt_style

# Short cut to all styles
from .alice import ALICE
from .atlas import ATLAS
from .cms import CMS, CMSTex, ROOT, ROOTTex
from .lhcb import LHCb, LHCbTex, LHCb1, LHCbTex1, LHCb2, LHCbTex2


def set_style(styles):
    """
    Set the experiment specific plotting style

    Example:

        >>> import mplhep as hep
        >>> hep.set_style("ATLAS")
        >>> hep.set_style(mplhep.style.CMS)

    Parameters
    ----------
        styles (`str` or `mplhep.style` `dict`): The experiment style
    """
    if not isinstance(styles, list):
        styles = [styles]

    # passed in experiment mplhep.style dict or str alias
    styles = [
        style if isinstance(style, dict) else getattr(sys.modules[__name__], f"{style}")
        for style in styles
    ]

    plt_style.use(styles)


fira = {"font.sans-serif": "Fira Sans"}

firamath = {
    "mathtext.fontset": "custom",
    "mathtext.rm": "Fira Math:regular",
    "mathtext.bf": "Fira Math:medium",
    "mathtext.sf": "Fira Math",
    "mathtext.it": "Fira Math:regular:italic",
    "mathtext.tt": "Fira Mono",
}

fabiola = {
    "font.sans-serif": "Comic Sans MS",
}
