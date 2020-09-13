import inspect
from matplotlib import docstring

# Log styles
from . import styles_lhcb as style
from . import label as label_base
from .label import lumitext
import mplhep

__all__ = [style, lumitext]


# Experiment wrappers:
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
