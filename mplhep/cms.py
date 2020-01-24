# Log styles
from . import styles_cms as style
from . import label
from . label import lumitext
__all__ = [style, lumitext]


# Experiment wrappers:
def cmstext(text="", loc=0, ax=None,
            fontname=None, fontsize=None, pad=0):
    return label._exptext("CMS", text=text, loc=loc, ax=ax,
                          fontname=None, fontsize=None, italic=(False, True),
                          pad=pad)


def cmslabel(ax=None, loc=0, data=False, paper=False, supplementary=False,
             year=2017, lumi=None, llabel=None, rlabel=None, fontname=None,
             fontsize=None, pad=0):
    return label._explabel(ax=ax, loc=loc, data=data, paper=paper,
                           supplementary=supplementary, year=year, lumi=lumi,
                           llabel=llabel, rlabel=rlabel,
                           fontname=fontname, fontsize=fontsize, pad=pad,
                           exp="CMS", italic=(False, True))
