from __future__ import annotations

import sys

from matplotlib.pyplot import style as plt_style

import mplhep._deprecate as deprecate

# Short cut to all styles
from .alice import ALICE
from .atlas import ATLAS, ATLAS1, ATLAS2, ATLASAlt, ATLASTex
from .cms import CMS, ROOT, CMSTex, ROOTTex
from .dune import DUNE, DUNE1, DUNETex, DUNETex1
from .lhcb import LHCb, LHCb1, LHCb2, LHCbTex, LHCbTex1, LHCbTex2
from .plothist import PLOTHIST

__all__ = (
    "ALICE",
    "ATLAS",
    "CMS",
    "PLOTHIST",
    "ROOT",
    "ATLAS1",
    "ATLAS2",
    "ATLASAlt",
    "ATLASTex",
    "CMSTex",
    "DUNE1",
    "DUNETex1",
    "DUNE",
    "DUNETex",
    "LHCb",
    "LHCb1",
    "LHCb2",
    "LHCbTex",
    "LHCbTex1",
    "LHCbTex2",
    "ROOTTex",
    "fabiola",
    "fira",
    "firamath",
    "set_style",
    "use",
)


__style_aliases__ = (
    "ALICE",
    "ATLAS",
    "CMS",
    "PLOTHIST",
    "ROOT",
    "ATLAS1",
    "ATLAS2",
    "ATLASAlt",
    "ATLASTex",
    "CMSTex",
    "DUNE1",
    "DUNETex1",
    "DUNE",
    "DUNETex",
    "LHCb",
    "LHCb1",
    "LHCb2",
    "LHCbTex",
    "LHCbTex1",
    "LHCbTex2",
    "ROOTTex",
    "fabiola",
    "fira",
    "firamath",
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

        >>> import mplhep as mh
        >>> mh.style.use("ATLAS")
        >>> mh.style.use(mh.style.CMS)

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
    _passed_aliases = [style for style in styles if not isinstance(style, dict)]
    if len(_passed_aliases) > 1:
        error_msg = (
            'Can only pass in one style alias at a time, but can modify settings eg. `use(["CMS", {"font.size":25}])`. '
            f"Got {', '.join(_passed_aliases)}"
        )
        raise ValueError(error_msg)
    if (
        len(_passed_aliases) == 1
        and _passed_aliases[0] not in sys.modules[__name__].__dict__
    ):
        error_msg = f"Unknown style alias: {_passed_aliases[0]}. Choose from {list(__style_aliases__)}"
        raise ValueError(error_msg)
    styles = [
        style if isinstance(style, dict) else getattr(sys.modules[__name__], f"{style}")
        for style in styles
    ]

    plt_style.use(styles)
    return None


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
