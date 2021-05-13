from __future__ import annotations

import inspect

from matplotlib import docstring

import mplhep

from . import label as label_base
from .label import lumitext

# Log styles
from .styles import alice as style

__all__ = ("style", "lumitext")


@docstring.copy(label_base.exp_text)
def text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    return label_base.exp_text("ALICE", text=text, fontsize=28, loc=1, **kwargs)


@docstring.copy(label_base.exp_label)
def label(label=None, **kwargs):
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base.exp_label).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    if label is not None:
        kwargs["label"] = label
    return label_base.exp_label(exp="ALICE", fontsize=28, loc=1, rlabel="", **kwargs)
