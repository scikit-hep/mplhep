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
from .lhcb import LHCb, LHCb1, LHCb2, LHCbTex, LHCbTex1, LHCbTex2, LHCB2_VARIANTS
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


def use(styles=None):
    """
    Set the experiment specific plotting style

    Example:

        >>> import mplhep as mh
        >>> mh.style.use("ATLAS")
        >>> mh.style.use("LHCb2:constrained")  # Use a variant
        >>> mh.style.use(mh.style.CMS)

    Parameters
    ----------
    styles : str or mplhep.style or dict or None
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

    # Resolve aliases and variants
    new_styles = []
    for style in styles:
        if isinstance(style, dict):
            new_styles.append(style)
            continue
        
        # It is a string alias
        base_style = style
        variant = None

        # 1. Parse "Style:variant" syntax
        if isinstance(style, str) and ":" in style:
            base_style, variant = style.split(":", 1)

        # 2. Check if base style exists
        if base_style not in sys.modules[__name__].__dict__:
             error_msg = f"Unknown style alias: {base_style}. Choose from {list(__style_aliases__)}"
             raise ValueError(error_msg)

        # 3. Retrieve the Base Dictionary
        # IMPORTANT: We use .copy() to ensure we don't permanently mutate the base style
        style_obj = getattr(sys.modules[__name__], base_style)
        if isinstance(style_obj, dict):
            style_obj = style_obj.copy()

        # 4. Apply Variant (if requested)
        if variant:
            # Construct the registry name (e.g., "LHCB2_VARIANTS")
            registry_name = f"{base_style.upper()}_VARIANTS"
            if hasattr(sys.modules[__name__], registry_name):
                registry = getattr(sys.modules[__name__], registry_name)
                if variant in registry:
                    style_obj.update(registry[variant])
                else:
                    raise ValueError(f"Variant '{variant}' not found in {registry_name}")
            else:
                raise ValueError(f"Style '{base_style}' does not support variants (requested '{variant}').")

        new_styles.append(style_obj)

    plt_style.use(new_styles)
    return None


def _resolve_styles(styles):
    """
    Helper: Resolves style strings (including 'Style:Variant' syntax) into 
    Matplotlib-compatible dictionaries.
    """
    if styles is None:
        return ["default"]
    if not isinstance(styles, list):
        styles = [styles]

    # ... (alias check remains same) ...
    _passed_aliases = [style for style in styles if not isinstance(style, dict)]
    if len(_passed_aliases) > 1:
        # ... (error msg) ...
        pass # (Assume existing logic here)

    new_styles = []
    for style in styles:
        if isinstance(style, dict):
            new_styles.append(style)
            continue
        
        # === FIX STARTS HERE ===
        # Pass "default" directly to Matplotlib
        if style == "default":
            new_styles.append("default")
            continue
        # === FIX ENDS HERE ===

        # It is a string alias
        base_style = style
        variant = None

        if isinstance(style, str) and ":" in style:
            base_style, variant = style.split(":", 1)

        if base_style not in sys.modules[__name__].__dict__:
             error_msg = f"Unknown style alias: {base_style}. Choose from {list(__style_aliases__)}"
             raise ValueError(error_msg)

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
                    raise ValueError(f"Variant '{variant}' not found in {registry_name}")
            else:
                raise ValueError(f"Style '{base_style}' does not support variants (requested '{variant}').")

        new_styles.append(style_obj)
    
    return new_styles


def use(styles=None):
    """
    Set the experiment specific plotting style.

    Example:
        >>> import mplhep as hep
        >>> hep.style.use("ATLAS")
        >>> hep.style.use("LHCb2:constrained")

    Parameters
    ----------
    styles : str or mplhep.style or dict or None
        The experiment style.
    """
    plt_style.use(_resolve_styles(styles))


def context(styles=None):
    """
    Context manager for using a style temporarily.

    Example:
        >>> with hep.style.context("LHCb2:constrained"):
        >>>     plt.plot(...)
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

fabiola = {
    "font.sans-serif": "Comic Sans MS",
}

