"""
Styling module.
This module provides matplotlib stylesheets for various HEP experiments.
"""

from __future__ import annotations

import sys

from matplotlib.pyplot import style as plt_style

import mplhep._deprecate as deprecate

# Short cut to all styles
from .alice import ALICE
from .atlas import ATLAS, ATLAS1, ATLAS2, ATLASAlt, ATLASTex
from .cms import CMS, ROOT, CMSTex, ROOTTex
from .dune import DUNE, DUNE1, DUNETex, DUNETex1
from .lhcb import LHCB2_VARIANTS, LHCb, LHCb1, LHCb2, LHCbTex, LHCbTex1, LHCbTex2
from .plothist import plothist

__all__ = (
    "ALICE",
    "ATLAS",
    "CMS",
    "plothist",
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
    "LHCB2_VARIANTS",
    "LHCbTex",
    "LHCbTex1",
    "LHCbTex2",
    "ROOTTex",
    "fabiola",
    "fira",
    "firamath",
    "set_style",
    "use",
    "context",
)

__style_aliases__ = (
    "ALICE",
    "ATLAS",
    "CMS",
    "plothist",
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


def _resolve_styles(styles):
    """
    Helper: Resolves style strings into Matplotlib-compatible dictionaries.
    """
    if styles is None:
        return ["default"]
    if not isinstance(styles, list):
        styles = [styles]

    _passed_aliases = [style for style in styles if not isinstance(style, dict)]
    if len(_passed_aliases) > 1:
        msg = (
            "Can only pass in one style alias at a time, but can modify settings "
            f'eg. `use(["CMS", {{"font.size":25}}])`. Got {", ".join(_passed_aliases)}'
        )
        raise ValueError(msg)

    new_styles = []
    for style in styles:
        if isinstance(style, dict):
            new_styles.append(style)
            continue

        # Allow default matplotlib style
        if style == "default":
            new_styles.append("default")
            continue

        base_style = style
        variant = None

        if isinstance(style, str) and ":" in style:
            base_style, variant = style.split(":", 1)

        if base_style not in sys.modules[__name__].__dict__:
            msg = f"Unknown style alias: {base_style}. Choose from {list(__style_aliases__)}"
            raise ValueError(msg)

        style_obj = getattr(sys.modules[__name__], base_style)
        if isinstance(style_obj, dict):
            style_obj = style_obj.copy()

        if variant:
            registry_name = f"{base_style.upper()}_VARIANTS"
            if hasattr(sys.modules[__name__], registry_name):
                registry = getattr(sys.modules[__name__], registry_name)
                if variant in registry:
                    style_obj.update(registry[variant])
                else:
                    msg = f"Variant '{variant}' not found in {registry_name}"
                    raise ValueError(msg)
            else:
                msg = f"Style '{base_style}' does not support variants (requested '{variant}')."
                raise ValueError(msg)

        new_styles.append(style_obj)

    return new_styles


def use(styles=None):
    """
    Set the experiment specific plotting style.
    """
    plt_style.use(_resolve_styles(styles))


def context(styles=None):
    """
    Context manager for using a style temporarily.
    """
    return plt_style.context(_resolve_styles(styles))


fira = {"font.sans-serif": "Fira Sans"}
firamath = {
    "mathtext.fontset": "custom",
    "mathtext.rm": "Fira Math:regular",
    "mathtext.bf": "Fira Math:medium",
    "mathtext.sf": "Fira Math",
    "mathtext.it": "Fira Math:regular:italic",
    "mathtext.tt": "Fira Mono",
}
fabiola = {"font.sans-serif": "Comic Sans MS"}
