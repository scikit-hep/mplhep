from __future__ import annotations

import inspect

from matplotlib import rcParams

import mplhep

from . import label as label_base
from ._compat import docstring
from ._deprecate import deprecate_parameter

# Log styles
from .styles import cms as style

# import mplhep._deprecate as deprecate

__all__ = ("label", "style", "text")


@docstring.copy(label_base.exp_text)
def text(text=None, **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs
            and key in inspect.getfullargspec(label_base.exp_text).kwonlyargs
        ):
            kwargs.setdefault(key, value)
    kwargs.setdefault("fontstyle", ("normal", "italic", "normal", "normal"))
    kwargs.setdefault("exp", "CMS")
    if text is not None:
        kwargs["text"] = text
    return label_base.exp_text(**kwargs)


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
            rcParams["font.size"],
            rcParams["font.size"] / 1.1,
            rcParams["font.size"] / 1.3,
        ),
    )
    kwargs.setdefault("fontstyle", ("normal", "italic", "normal", "normal"))
    kwargs.setdefault("exp", "CMS")
    if text is not None:
        kwargs["text"] = text
    return label_base.exp_label(**kwargs)


# Deprecation example
# @deprecate.deprecate("Naming convention is changing. Use ``mplhep.cms.label``.")
# def cmslabel(*args, **kwargs):
#     return _cms_label(*args, **kwargs)
