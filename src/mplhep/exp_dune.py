# Taken with a lot of inspiration from https://github.com/DUNE/dune_plot_style
# Many thanks to the authors for their work!

from __future__ import annotations

import inspect

from matplotlib import rcParams

import mplhep

from . import label as label_base
from ._compat import docstring
from ._deprecate import deprecate_parameter

# Import styles
from .styles import dune as style

__all__ = ("label", "style", "text")


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
    kwargs.setdefault(
        "fontsize",
        (
            rcParams["font.size"] * 1.3,
            rcParams["font.size"],
            rcParams["font.size"] * 0.95,
            rcParams["font.size"] / 1.3,
        ),
    )
    kwargs.setdefault("fontstyle", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("exp", "DUNE")
    return label_base.exp_text(text=text, **kwargs)


@deprecate_parameter("label", reason='Use `text="..."` instead.', warn_once=False)
@docstring.copy(label_base.exp_label)
def label(text=None, label=None, **kwargs):
    """Add DUNE experiment label to a plot."""
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_label).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault(
        "fontsize",
        (
            rcParams["font.size"] * 1.3,
            rcParams["font.size"],
            rcParams["font.size"] * 0.95,
            rcParams["font.size"] / 1.3,
        ),
    )
    kwargs.setdefault("fontstyle", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("exp", "DUNE")
    kwargs.setdefault("loc", 0)
    if text is not None:
        kwargs["text"] = text
    if label is not None:
        kwargs["text"] = label
    return label_base.exp_label(**kwargs)
