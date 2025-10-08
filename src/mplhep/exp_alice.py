from __future__ import annotations

import inspect

import mplhep

from . import label as label_base
from ._compat import docstring
from ._deprecate import deprecate_parameter

# Log styles
from .styles import alice as style

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
    kwargs.setdefault("fontsize", 28)
    kwargs.setdefault("fontstyle", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("loc", 1)
    kwargs.setdefault("exp", "ALICE")
    return label_base.exp_text(text=text, **kwargs)


@deprecate_parameter("label", reason='Use `text="..."` instead.', warn_once=False)
@docstring.copy(label_base.exp_label)
def label(text=None, label=None, **kwargs):
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_label).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("fontsize", 28)
    kwargs.setdefault("fontstyle", ("normal", "normal", "normal", "normal"))
    kwargs.setdefault("loc", 1)
    kwargs.setdefault("exp", "ALICE")
    kwargs.setdefault("rlabel", "")
    if text is not None:
        kwargs["text"] = text
    if label is not None:
        kwargs["text"] = label
    return label_base.exp_label(**kwargs)
