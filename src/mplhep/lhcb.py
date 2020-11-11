"""LHCb-like plot styles

All of this styles resemble the LHCb plotting style; however it is an approximation and
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
import inspect

import mplhep
from matplotlib import docstring
from mplhep import label as label_base

from .label import lumitext
from .styles import lhcb as style

__all__ = [style, lumitext, "label", "text"]


def _lhcb_text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base._exp_text).args
        ):
            kwargs[key] = value
    return label_base._exp_text(
        "LHCb",
        text=text,
        italic=(False, False),
        fontsize=28,
        fontname="Times New Roman",
        loc=1,
        **kwargs
    )


def _lhcb_label(**kwargs):
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base._exp_label).args
        ):
            kwargs[key] = value
    return label_base._exp_label(
        exp="LHCb",
        italic=(False, False),
        fontsize=28,
        fontname="Times New Roman",
        loc=1,
        **kwargs
    )


@docstring.copy(label_base._exp_text)
def text(*args, **kwargs):
    return _lhcb_text(*args, **kwargs)


@docstring.copy(label_base._exp_label)
def label(**kwargs):
    return _lhcb_label(**kwargs)
