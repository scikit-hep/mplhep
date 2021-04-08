from __future__ import annotations

import sys

from matplotlib.pyplot import style as plt_style

# Short cut to all styles
from .alice import ALICE
from .atlas import ATLAS, ATLASAlt, ATLASTex
from .cms import CMS, ROOT, CMSTex, ROOTTex
from .lhcb import LHCb, LHCb1, LHCb2, LHCbTex, LHCbTex1, LHCbTex2

__all__ = (
    "ALICE",
    "ATLAS",
    "ATLASAlt",
    "ATLASTex",
    "CMS",
    "ROOT",
    "CMSTex",
    "ROOTTex",
    "LHCb",
    "LHCb1",
    "LHCb2",
    "LHCbTex",
    "LHCbTex1",
    "LHCbTex2",
    "set_style",
    "fira",
    "firamath",
    "fabiola",
)


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
