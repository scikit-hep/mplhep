from __future__ import annotations

from typing import Any

import matplotlib as mpl
from cycler import cycler

# Color wheel from https://arxiv.org/pdf/2107.02270 Table 1, 10 color palette
# This is the color wheel recommended for plots that require a large number
# of colors that would not be satisfied by the below palette
color_sequence1 = [
    "#3f90da",
    "#ffa90e",
    "#bd1f01",
    "#94a4a2",
    "#832db6",
    "#a96b59",
    "#e76300",
    "#b9ac70",
    "#717581",
    "#92dadd",
]

# Color wheel based on internal discussions of optimal
# colors for visibility, accounting for color vision deficiency
# The recommendation for signal is the first color (Vermilion)
# For large signals, ROOT.kWhite / '#ffffff' is also an option
color_sequence2 = [
    "#d55e00",
    "#56b4e9",
    "#e69f00",
    "#f0e442",
    "#009e73",
    "#cc79a7",
    "#0072b2",
]

_base = {
    # fonts and text
    # initially from https://github.com/kratsg/ATLASstylempl
    "font.size": 14,
    "font.family": "sans-serif",
    "font.sans-serif": [
        "TeX Gyre Heros",
        "helvetica",
        "Helvetica",
        "Nimbus Sans L",
        "Mukti Narrow",
        "FreeSans",
    ],
    "font.serif": [
        "Tex Gyre Termes",
        "Times",
        "Times Roman",
        "Times New Roman",
        "Nimbus Roman",
    ],
    "font.monospace": ["Tex Gyre Cursor", "Courier", "Courier New", "Nimbus Mono"],
    # figure layout
    "figure.figsize": (8.0, 6.0),
    "figure.dpi": 100,
    "figure.facecolor": "#FFFFFF",
    "figure.subplot.bottom": 0.16,
    "figure.subplot.top": 0.93,
    "figure.subplot.left": 0.16,
    "figure.subplot.right": 0.95,
    # axes
    "axes.titlesize": "xx-large",
    "axes.labelsize": "x-large",
    "axes.linewidth": 1,
    "axes.grid": False,
    "axes.axisbelow": False,
    "axes.labelpad": 10,
    "axes.facecolor": "#FFFFFF",
    "axes.labelcolor": "#000000",
    "axes.formatter.limits": "-2, 4",
    "axes.formatter.use_mathtext": True,
    "axes.autolimit_mode": "round_numbers",
    "axes.unicode_minus": False,
    "axes.xmargin": 0.0,
    # x/y axis label locations
    "xaxis.labellocation": "right",
    "yaxis.labellocation": "top",
    # xticks
    "xtick.direction": "in",
    "xtick.minor.visible": True,
    "xtick.top": True,
    "xtick.bottom": True,
    "xtick.major.top": True,
    "xtick.major.bottom": True,
    "xtick.minor.top": True,
    "xtick.minor.bottom": True,
    "xtick.labelsize": "large",
    "xtick.major.size": 5,
    "xtick.minor.size": 3,
    "xtick.color": "#000000",
    # yticks
    "ytick.direction": "in",
    "ytick.left": True,
    "ytick.right": True,
    "ytick.major.left": True,
    "ytick.major.right": True,
    "ytick.minor.left": True,
    "ytick.minor.right": True,
    "ytick.minor.visible": True,
    "ytick.labelsize": "large",
    "ytick.major.size": 14,
    "ytick.minor.size": 7,
    # lines
    "lines.linewidth": 2,
    "lines.markersize": 8,
    # legend
    "legend.numpoints": 1,
    "legend.fontsize": "medium",
    "legend.title_fontsize": "medium",
    "legend.labelspacing": 0.3,
    "legend.frameon": False,
    "legend.handlelength": 2,
    "legend.borderpad": 1.0,
    # savefig
    "savefig.transparent": False,
}

ATLAS1: dict[str, Any] = {
    **_base,
    "axes.prop_cycle": cycler("color", color_sequence1),
    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Heros",
    "mathtext.bf": "TeX Gyre Heros:bold",
    "mathtext.sf": "TeX Gyre Heros",
    "mathtext.it": "TeX Gyre Heros:italic",
    "mathtext.tt": "TeX Gyre Heros",
    "mathtext.cal": "TeX Gyre Heros",
    "mathtext.default": "it",
}

ATLAS2: dict[str, Any] = {
    **_base,
    "axes.prop_cycle": cycler("color", color_sequence2),
    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Heros",
    "mathtext.bf": "TeX Gyre Heros:bold",
    "mathtext.sf": "TeX Gyre Heros",
    "mathtext.it": "TeX Gyre Heros:italic",
    "mathtext.tt": "TeX Gyre Heros",
    "mathtext.cal": "TeX Gyre Heros",
    "mathtext.default": "it",
}

# use dejavusans (default math fontset)
ATLASAlt: dict[str, Any] = {
    **_base,
    "axes.prop_cycle": cycler("color", color_sequence1),
    "mathtext.default": "it",
}

# use LaTeX
ATLASTex: dict[str, Any] = {
    **ATLAS2,
    "text.usetex": True,
    "text.latex.preamble": "\n".join(
        [
            r"\usepackage[LGR,T1]{fontenc}",
            r"\usepackage{tgheros}",
            r"\renewcommand{\familydefault}{\sfdefault}",
            r"\usepackage{amsmath}",
            r"\usepackage[symbolgreek,symbolmax]{mathastext}",
            r"\usepackage{physics}",
            r"\usepackage{siunitx}",
            r"\setlength{\parindent}{0pt}",
            r"\def\mathdefault{}",
        ]
    ),
}

# Filter extra (labellocation) items if needed
ATLAS1 = {k: v for k, v in ATLAS1.items() if k in mpl.rcParams}
ATLAS2 = {k: v for k, v in ATLAS2.items() if k in mpl.rcParams}
ATLASAlt = {k: v for k, v in ATLASAlt.items() if k in mpl.rcParams}
ATLASTex = {k: v for k, v in ATLASTex.items() if k in mpl.rcParams}

# Alias 'ATLAS' to the one that most folks should use
ATLAS = ATLAS2.copy()
