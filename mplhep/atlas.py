# Log styles
from . import styles_atlas as style
from . import label as label_base
from .label import lumitext
import mplhep._deprecate as deprecate
from matplotlib import docstring


__all__ = [style, lumitext]


# Experiment wrappers, full names made private
def _atlas_text(text="", **kwargs):
    return label_base._exp_text("ATLAS", text=text, italic=(True, False), **kwargs)


def _atlas_label(**kwargs):
    return label_base._exp_label(exp="ATLAS", italic=(True, False), **kwargs)


# Temporary aliases
@deprecate.deprecate("Naming convention is changing. Use ``mplhep.atlas.label``.")
def atlaslabel(*args, **kwargs):
    return _atlas_label(*args, **kwargs)


@deprecate.deprecate("Naming convention is changing. Use ``mplhep.atlas.text``.")
def atlastext(**kwargs):
    return _atlas_text(**kwargs)


@docstring.copy(label_base._exp_text)
def text(*args, **kwargs):
    return _atlas_text(*args, **kwargs)


@docstring.copy(label_base._exp_label)
def label(**kwargs):
    return _atlas_label(**kwargs)
