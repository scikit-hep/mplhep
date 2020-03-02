# Log styles
from . import styles_lhcb as style
from . import label as label_base
from . label import lumitext
__all__ = [style, lumitext]


# Experiment wrappers:
def lhcbtext(text="", **kwargs):
    return label_base._exptext("LHCb", text=text, italic=(False, False),
                               fontsize=28, fontname="Times New Roman",
                               loc=1, **kwargs)


def lhcblabel(**kwargs):
    return label_base._explabel(exp="LHCb", italic=(False, False),
                                fontsize=28, fontname="Times New Roman",
                                loc=1, **kwargs)


def text(*args, **kwargs):
    return lhcbtext(*args, **kwargs)


def label(**kwargs):
    return lhcblabel(**kwargs)
