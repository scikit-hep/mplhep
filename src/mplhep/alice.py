import inspect
from matplotlib import docstring

# Log styles
from .styles import alice as style
from . import label as label_base
from .label import lumitext
import mplhep

__all__ = [style, lumitext]


# Experiment wrappers, full names made private
def _alice_text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base._exp_text).args
        ):
            kwargs[key] = value
    return label_base._exp_text(
        "ALICE", text=text, fontsize=28, loc=1, italic=(False, False), **kwargs
    )


def _alice_label(**kwargs):
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base._exp_label).args
        ):
            kwargs[key] = value
    return label_base._exp_label(
        exp="ALICE", fontsize=28, loc=1, italic=(False, False), rlabel="", **kwargs
    )


@docstring.copy(label_base._exp_text)
def text(*args, **kwargs):
    return _alice_text(*args, **kwargs)


@docstring.copy(label_base._exp_label)
def label(**kwargs):
    return _alice_label(**kwargs)
