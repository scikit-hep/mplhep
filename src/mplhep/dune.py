# Taken with a lot of inspiration from https://github.com/DUNE/dune_plot_style
# Many thanks to the authors for their work!

from __future__ import annotations

import inspect

import mplhep

from . import label as label_base
from ._compat import docstring
from .label import lumitext

# Import styles
from .styles import dune as style

__all__ = ("lumitext", "style")


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
    kwargs.setdefault("italic", (False, False, False))
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
    kwargs.setdefault("italic", (False, False, False))
    if label is not None:
        kwargs["label"] = label
    kwargs.setdefault("exp", "DUNE")
    kwargs.setdefault("loc", 0)
    return label_base.exp_label(**kwargs)
