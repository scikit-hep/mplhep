# Log styles
from . import styles_cms as style
from . import label as label_base
from . label import lumitext
__all__ = [style, lumitext]


# Experiment wrappers:
def cmstext(text="", **kwargs):
    return label_base._exptext("CMS", text=text, **kwargs, italic=(False, True))


def cmslabel(**kwargs):
    return label_base._explabel(**kwargs, exp="CMS", italic=(False, True))


def text(**kwargs):
    return cmstext(**kwargs)


def label(**kwargs):
    return cmslabel(**kwargs)
