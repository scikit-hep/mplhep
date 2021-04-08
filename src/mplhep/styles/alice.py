from __future__ import annotations

import matplotlib as mpl

ALICE = {
    "lines.linewidth": 1,
    "font.family": "sans-serif",
    "font.sans-serif": ["TeX Gyre Heros", "Helvetica", "Arial"],
    "font.size": 14,
    "mathtext.fontset": "stixsans",
    "mathtext.default": "rm",
    # figure layout
    "figure.figsize": (12.0, 9.0),
    "figure.facecolor": "white",
    "figure.subplot.bottom": 0.16,
    "figure.subplot.top": 0.93,
    "figure.subplot.left": 0.16,
    "figure.subplot.right": 0.95,
    # axes
    "axes.labelsize": 32,
    "axes.labelpad": 24,
    "xtick.top": True,
    "xtick.labelsize": 25,
    "xtick.major.size": 10,
    "xtick.minor.size": 5,
    "xtick.direction": "in",
    "xtick.minor.visible": True,
    "ytick.right": True,
    "ytick.labelsize": 25,
    "ytick.major.size": 14,
    "ytick.minor.size": 7,
    "ytick.direction": "in",
    "ytick.minor.visible": True,
    "lines.markersize": 8,
    # legend
    "legend.loc": "best",
    "legend.numpoints": 1,
    "legend.fontsize": 28,
    "legend.labelspacing": 0.3,
    "legend.frameon": False,
    "xaxis.labellocation": "right",
    "yaxis.labellocation": "top",
}

# Filter extra (labellocation) items if needed
ALICE = {k: v for k, v in ALICE.items() if k in mpl.rcParams}
