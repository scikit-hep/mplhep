from __future__ import annotations

import sys

from matplotlib.pyplot import style as plt_style

import mplhep._deprecate as deprecate

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
    "use",
    "fira",
    "firamath",
    "fabiola",
)


@deprecate.deprecate(
    "Naming convention is changing to match mpl. Use ``mplhep.style.use()``."
)
def set_style(styles=None):
    use(styles)


def use(styles=None):
    """
    Set the experiment specific plotting style

    Example:

        >>> import mplhep as hep
        >>> hep.style.use("ATLAS")
        >>> hep.style.use(hep.style.CMS)

    Parameters
    ----------
        styles: `str` or `mplhep.style` or `dict` None
            The experiment style. Will understand a dictionary
            of rcParams, a mplhep style or its string alias.
            Pass ``None`` to reset to mpl defaults.
    """

    if styles is None:
        return plt_style.use("default")
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
