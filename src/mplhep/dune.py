# Taken with a lot of insiration from https://github.com/DUNE/dune_plot_style
# Many thanks to the authors for their work!

from __future__ import annotations

import inspect

import matplotlib.pyplot as plt

import mplhep

from . import label as label_base
from ._compat import docstring
from .label import lumitext

# Import styles
from .styles import dune as style

__all__ = ("lumitext", "set_dune_logo_colors", "style")


@docstring.copy(label_base.exp_text)
def text(text="", **kwargs):
    """Add DUNE experiment text to a plot."""
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("italic", (False, True, False))
    kwargs.setdefault("exp", "DUNE")
    return label_base.exp_text(text=text, **kwargs)


@docstring.copy(label_base.exp_label)
def label(label=None, **kwargs):
    """Add DUNE experiment label to a plot."""
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_label).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("italic", (False, True, False))
    if label is not None:
        kwargs["label"] = label
    kwargs.setdefault("exp", "DUNE")
    return label_base.exp_label(**kwargs)


def set_dune_logo_colors():
    """Set the color cycler to use the DUNE logo colors (orange, blue, and yellow)."""
    from cycler import cycler

    # DUNE logo colors: orange, blue, yellow
    dune_logo_colors = ["#D55E00", "#56B4E9", "#E69F00"]
    cyc = cycler(color=dune_logo_colors)
    plt.rc("axes", prop_cycle=cyc)
