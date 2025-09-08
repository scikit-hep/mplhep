"""LHCb-like plot styles

All of these styles resemble the LHCb plotting style; however it is an approximation and
not an official style. The style `LHCb` should improve over time by inputs and may be changed in the future in favor of
 a style that resembles morethe actual LHCb style.

To use a specific style, use `LHCb1`, `LHCb2` etc. as they won't change in the future.

Notes on LHCb2 style:

An updated version of `LHCb` that includes minor ticks by default on and on all axes as well as improved legends and
larger minus sign (by using unicode).

Contributed and adjusted by Jonas Eschle <Jonas.Eschle@cern.ch>
based on the works of Kevin Dungs, Tim Head, Thomas Schietinger,
                      Andrew Powell, Chris Parkes, Elena Graverini
                      and Niels Tuning
"""

from __future__ import annotations

import inspect

import mplhep
from mplhep import label as label_base

from ._compat import docstring
from .label import lumitext as _base_lumitext
from .styles import lhcb as style

__all__ = ("label", "_base_lumitext", "style", "text")


@docstring.copy(label_base.exp_text)
def text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("italic", (False, False, False))
    kwargs.setdefault("fontsize", 28)
    kwargs.setdefault("fontname", "Times New Roman")
    kwargs.setdefault("loc", 1)
    kwargs.setdefault("exp_weight", "normal")
    return label_base.exp_text("LHCb", text=text, **kwargs)


@docstring.copy(label_base.exp_label)
def label(label=None, **kwargs):
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_label).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("italic", (False, False, False))
    kwargs.setdefault("fontsize", 28)
    kwargs.setdefault("fontname", "Times New Roman")
    kwargs.setdefault("exp_weight", "normal")
    kwargs.setdefault("loc", 1)
    kwargs.setdefault("exp_weight", "normal")
    if label is not None:
        kwargs["label"] = label
    return label_base.exp_label("LHCb", **kwargs)


@docstring.copy(label_base.lumitext)
def lumitext(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.lumitext).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    # kwargs.setdefault("italic", (False, False, False))
    # kwargs.setdefault("fontsize", 28)
    kwargs.setdefault("fontname", "Times New Roman")
    # kwargs.setdefault("loc", 1)
    # kwargs.setdefault("exp_weight", "normal")
    return label_base.lumitext("LHCb", text=text, **kwargs)
