import inspect
import matplotlib as mpl

# Log styles
from .styles import atlas as style
from . import label as label_base
from .label import lumitext
import mplhep

__all__ = [style, lumitext]


# Experiment wrappers, full names made private
def _atlas_text(text="", **kwargs):
    for key, value in dict(mplhep.rcParams.text._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base._exp_text).args
        ):
            kwargs[key] = value
    return label_base._exp_text("ATLAS", text=text, italic=(True, False), **kwargs)


def _atlas_label(**kwargs):
    for key, value in dict(mplhep.rcParams.label._get_kwargs()).items():
        if (
            value is not None
            and key not in kwargs.keys()
            and key in inspect.getfullargspec(label_base._exp_label).args
        ):
            kwargs[key] = value
    return label_base._exp_label(exp="ATLAS", italic=(True, False), **kwargs)


@mpl.docstring.copy(label_base._exp_text)
def text(*args, **kwargs):
    return _atlas_text(*args, **kwargs)


@mpl.docstring.copy(label_base._exp_label)
def label(**kwargs):
    return _atlas_label(**kwargs)


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
