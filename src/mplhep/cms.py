from __future__ import annotations

import inspect

import mplhep

from . import label as label_base
from ._compat import docstring
from .label import lumitext

# Log styles
from .styles import cms as style

# import mplhep._deprecate as deprecate

__all__ = ("lumitext", "style")


@docstring.copy(label_base.exp_text)
def text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("italic", (False, True, False))
    kwargs.setdefault("exp", "CMS")
    return label_base.exp_text(text=text, **kwargs)


@docstring.copy(label_base.exp_label)
def label(label=None, **kwargs):
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
    kwargs.setdefault("exp", "CMS")
    return label_base.exp_label(**kwargs)


# Deprecation example
# @deprecate.deprecate("Naming convention is changing. Use ``mplhep.cms.label``.")
# def cmslabel(*args, **kwargs):
#     return _cms_label(*args, **kwargs)
