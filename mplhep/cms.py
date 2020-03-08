# Log styles
from . import styles_cms as style
from . import label as label_base
from . label import lumitext
__all__ = [style, lumitext]


# Experiment wrappers:
def cmstext(text="", **kwargs):
    return label_base._exptext("CMS", text=text, italic=(False, True), **kwargs)


def cmslabel(**kwargs):
    return label_base._explabel(exp="CMS", italic=(False, True), **kwargs)


def text(*args, **kwargs):
    return cmstext(*args, **kwargs)


def label(**kwargs):
    return cmslabel(**kwargs)
