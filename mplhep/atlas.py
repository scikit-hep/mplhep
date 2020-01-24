# Log styles
from . import styles_atlas as style
from . import label
from . label import lumitext
__all__ = [style, lumitext]


def atlastext(text="", loc=0, ax=None,
              fontname=None, fontsize=None, pad=0):
    return label._exptext("ATLAS", text=text, loc=loc, ax=ax,
                          fontname=None, fontsize=None, italic=(True, False),
                          pad=pad)


def atlaslabel(ax=None, loc=0, data=False, paper=False, supplementary=False,
               year=2017, lumi=None, llabel=None, rlabel=None, fontname=None,
               fontsize=None, pad=0):
    return label._explabel(ax=ax, loc=loc, data=data, paper=paper,
                           supplementary=supplementary, year=year, lumi=lumi,
                           llabel=llabel, rlabel=rlabel,
                           fontname=fontname, fontsize=fontsize, pad=pad,
                           exp="ATLAS", italic=(True, False))
