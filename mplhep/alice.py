# Log styles
from . import styles_alice as style
from . import label as label_base
from .label import lumitext
import mplhep._deprecate as deprecate
from matplotlib import docstring


__all__ = [style, lumitext]


# Experiment wrappers, full names made private
def _alice_text(text="", **kwargs):
    return label_base._exp_text(
        "ALICE", text=text, fontsize=28, loc=1, italic=(False, False), **kwargs
    )


def _alice_label(**kwargs):
    return label_base._exp_label(
        exp="ALICE", fontsize=28, loc=1, italic=(False, False), rlabel="", **kwargs
    )


@docstring.copy(label_base._exp_text)
def text(*args, **kwargs):
    return _alice_text(*args, **kwargs)


@docstring.copy(label_base._exp_label)
def label(**kwargs):
    return _alice_label(**kwargs)
