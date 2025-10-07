from __future__ import annotations

import inspect

import matplotlib as mpl
from matplotlib import rcParams

import mplhep

from . import label as label_base
from ._compat import docstring
from ._deprecate import deprecate, deprecate_parameter

# Log styles
from .styles import atlas as style

__all__ = ("label", "set_xlabel", "set_ylabel", "style", "text")


@docstring.copy(label_base.exp_text)
def text(text="", **kwargs):
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
            rcParams["font.size"] * 1.2,
            rcParams["font.size"],
            rcParams["font.size"] / 1.3,
        ),
    )
    kwargs.setdefault("fontstyle", ("italic", "normal", "italic", "normal"))
    kwargs.setdefault("loc", 4)
    kwargs.setdefault("exp", "ATLAS")
    return label_base.exp_text(text=text, **kwargs)


@deprecate_parameter("label", reason='Use `text="..."` instead.', warn_once=False)
@docstring.copy(label_base.exp_label)
def label(text=None, **kwargs):
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
            rcParams["font.size"] * 1.2,
            rcParams["font.size"],
            rcParams["font.size"] / 1.3,
        ),
    )
    kwargs.setdefault("fontstyle", ("italic", "normal", "italic", "normal"))
    kwargs.setdefault("loc", 4)
    kwargs.setdefault("exp", "ATLAS")
    if text is not None:
        kwargs["text"] = text
    return label_base.exp_label(**kwargs)


@deprecate(reason="Use `ax.set_xlabel(...)` directly instead.", warn_once=False)
def set_xlabel(label, ax=None, *args, **kwargs):
    """
    Set x label in ATLAS style (right aligned).

    Additional parameters are passed through to `ax.set_xlabel`.

    Parameters
    ----------
    label : str
        Label (LaTeX permitted)
    ax : mpl.axes.Axes, optional
        Axes to set x label on
    """
    ax = ax or mpl.pyplot.gca()
    # update settings
    kwargs.update({"ha": "right", "va": "top", "x": 1.0})
    ax.set_xlabel(label, *args, **kwargs)


@deprecate(reason="Use `ax.set_xlabel(...)` directly instead.", warn_once=False)
def set_ylabel(label, ax=None, *args, **kwargs):
    """
    Set y label in ATLAS style (top aligned).

    Additional parameters are passed through to ``ax.set_ylabel``.

    Parameters
    ----------
    label : str
        Label (LaTeX permitted)
    ax : mpl.axes.Axes, optional
        Axes to set y label on
    """
    ax = ax or mpl.pyplot.gca()
    kwargs.update({"ha": "right", "va": "bottom", "y": 1.0})
    ax.set_ylabel(label, *args, **kwargs)
