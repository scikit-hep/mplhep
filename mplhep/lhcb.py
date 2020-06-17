# Log styles
from . import styles_lhcb as style
from . import label as label_base
from .label import lumitext
import mplhep._deprecate as deprecate
from matplotlib import docstring

__all__ = [style, lumitext]


# Experiment wrappers:
def _lhcb_text(text="", **kwargs):
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
    return label_base._exp_label(
        exp="LHCb",
        italic=(False, False),
        fontsize=28,
        fontname="Times New Roman",
        loc=1,
        **kwargs
    )


# Change to snake_case
@deprecate.deprecate("Naming convention is changing. Use ``mplhep.lhcb.label``.")
def lhcblabel(*args, **kwargs):
    return _lhcb_label(*args, **kwargs)


@deprecate.deprecate("Naming convention is changing. Use ``mplhep.lhcb.text``.")
def lhcbtext(**kwargs):
    return _lhcb_text(**kwargs)


@docstring.copy(label_base._exp_text)
def text(*args, **kwargs):
    return _lhcb_text(*args, **kwargs)


@docstring.copy(label_base._exp_label)
def label(**kwargs):
    return _lhcb_label(**kwargs)
