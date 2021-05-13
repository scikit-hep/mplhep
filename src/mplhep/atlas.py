from __future__ import annotations

import inspect

import matplotlib as mpl

import mplhep

from . import label as label_base
from .label import lumitext

# Log styles
from .styles import atlas as style

__all__ = ("style", "lumitext")


@mpl.docstring.copy(label_base.exp_text)
def text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("italic", (True, False))
    kwargs.setdefault("loc", 4)
    return label_base.exp_text("ATLAS", text=text, **kwargs)


@mpl.docstring.copy(label_base.exp_label)
def label(label=None, **kwargs):
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base.exp_label).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("italic", (True, False))
    kwargs.setdefault("loc", 4)
    if label is not None:
        kwargs["label"] = label
    return label_base.exp_label(exp="ATLAS", **kwargs)


# set_xlabel / set_ylabel copied from atlas-mpl
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
