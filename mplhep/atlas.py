# Log styles
from . import styles_atlas as style
from . import label as label_base
from . label import lumitext
__all__ = [style, lumitext]


# Experiment wrappers:
def atlastext(text="", **kwargs):
    return label_base._exptext("ATLAS", text=text, italic=(True, False), **kwargs)


def atlaslabel(**kwargs):
    return label_base._explabel(exp="ATLAS", italic=(True, False), **kwargs)


def text(*args, **kwargs):
    return atlastext(*args, **kwargs)


def label(**kwargs):
    return atlaslabel(**kwargs)
