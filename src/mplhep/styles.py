import sys
from matplotlib.pyplot import style as plt_style

# Short cut to all styles
from .styles_cms import CMS, CMSTex, ROOT, ROOTTex, firamath, fabiola
from .styles_atlas import ATLAS
from .styles_alice import ALICE
from .styles_lhcb import LHCb, LHCbTex


def set_style(style):
    """
    Set the experiment specific plotting style

    Example:

        >>> import mplhep as hep
        >>> hep.set_style("ATLAS")
        >>> hep.set_style(mplhep.style.CMS)

    Parameters
    ----------
        style (`str` or `mplhep.style` `dict`): The experiment sytle
    """
    if isinstance(style, dict):
        # passed in experiment mplhep.style dict
        plt_style.use(style)
    else:
        plt_style.use(getattr(sys.modules[__name__], f"{style}"))
