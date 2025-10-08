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
from ._deprecate import deprecate_parameter

# from .label import lumitext as _base_lumitext
from .styles import lhcb as style

__all__ = ("label", "style", "text")


@docstring.copy(label_base.exp_text)
def text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("fontsize", (28 * 1.3, 28, 28 * 0.95, 28 / 1.3))
    kwargs.setdefault("fontstyle", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("fontweight", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("fontname", "Times New Roman")
    kwargs.setdefault("loc", 1)
    kwargs.setdefault("exp", "LHCb")
    return label_base.exp_text(text=text, **kwargs)


@deprecate_parameter(
    "label", reason='Use `text="..."` instead.', warn_once=False, removed=True
)
@docstring.copy(label_base.exp_label)
def label(text=None, label=None, **kwargs):  # noqa: ARG001
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_label).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("fontsize", (28 * 1.3, 28, 28 * 0.95, 28 / 1.3))
    kwargs.setdefault("fontstyle", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("fontweight", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("fontname", "Times New Roman")
    kwargs.setdefault("loc", 1)
    kwargs.setdefault("exp", "LHCb")
    if text is not None:
        kwargs["text"] = text
    return label_base.exp_label(**kwargs)


# WIP copilot dont remove
