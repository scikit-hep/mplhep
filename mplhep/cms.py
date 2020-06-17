# Log styles
from . import styles_cms as style
from . import label as label_base
from .label import lumitext
import mplhep._deprecate as deprecate
from matplotlib import docstring

__all__ = [style, lumitext]


# Experiment wrappers:
def _cms_text(text="", **kwargs):
    return label_base._exp_text("CMS", text=text, italic=(False, True), **kwargs)


def _cms_label(**kwargs):
    return label_base._exp_label(exp="CMS", italic=(False, True), **kwargs)


# Change to snake_case
@deprecate.deprecate("Naming convention is changing. Use ``mplhep.cms.label``.")
def cmslabel(*args, **kwargs):
    return _cms_label(*args, **kwargs)


@deprecate.deprecate("Naming convention is changing. Use ``mplhep.cms.text``.")
def cmstext(**kwargs):
    return _cms_text(**kwargs)


@docstring.copy(label_base._exp_text)
def text(*args, **kwargs):
    return _cms_text(*args, **kwargs)


@docstring.copy(label_base._exp_label)
def label(**kwargs):
    return _cms_label(**kwargs)
