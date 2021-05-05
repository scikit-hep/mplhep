from __future__ import annotations

from typing import Any

import matplotlib as mpl

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

ATLAS: dict[str, Any] = {
    **_base,
    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Heros",
    "mathtext.bf": "TeX Gyre Heros:bold",
    "mathtext.sf": "TeX Gyre Heros",
    "mathtext.it": "TeX Gyre Heros:italic",
    "mathtext.tt": "TeX Gyre Heros",
    "mathtext.cal": "TeX Gyre Heros",
    "mathtext.default": "it",
    "mathtext.fontset": "custom",
}

# use dejavusans (default math fontset)
ATLASAlt: dict[str, Any] = {
    **_base,
    "mathtext.default": "it",
}

# use LaTeX
ATLASTex: dict[str, Any] = {
    **_base,
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
ATLAS = {k: v for k, v in ATLAS.items() if k in mpl.rcParams}
ATLASAlt = {k: v for k, v in ATLASAlt.items() if k in mpl.rcParams}
ATLASTex = {k: v for k, v in ATLASTex.items() if k in mpl.rcParams}
