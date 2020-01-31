# Log styles
from . import styles_atlas as style
from . import label as label_base
from label_base import lumitext
__all__ = [style, lumitext]


# Experiment wrappers:
def atlastext(text="", **kwargs):
    return label_base._exptext("ATLAS", text=text, **kwargs, italic=(True, False))


def atlaslabel(**kwargs):
    return label_base._explabel(**kwargs, exp="ATLAS", italic=(True, False))


def text(**kwargs):
    return atlastext(**kwargs)


def label(**kwargs):
    return atlaslabel(**kwargs)
