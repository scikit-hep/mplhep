import sys
from matplotlib.pyplot import style as plt_style

# Short cut to all styles
from .styles_cms import CMS, CMSTex, ROOT, ROOTTex, firamath, fabiola
from .styles_atlas import ATLAS
from .styles_alice import ALICE
from .styles_lhcb import LHCb, LHCbTex


def set_style(styles):
    """
    Set the experiment specific plotting style

    Example:

        >>> import mplhep as hep
        >>> hep.set_style("ATLAS")
        >>> hep.set_style(mplhep.style.CMS)

    Parameters
    ----------
        styles (`str` or `mplhep.style` `dict`): The experiment style
    """
    if not isinstance(styles, list):
        styles = [styles]

    # passed in experiment mplhep.style dict or str alias
    styles = [
        style if isinstance(style, dict) else getattr(sys.modules[__name__], f"{style}")
        for style in styles
    ]

    plt_style.use(styles)
