from __future__ import annotations

import copy

import matplotlib as mpl

SNOplus1 = {
    # Set font, use liberation serif as a fallback if times new roman is not
    # installed
    "font.size": 12,
    "font.serif": ["Times New Roman", "Liberation Serif"],
    "font.family": "serif",
    "mathtext.fontset": "stix",
    "mathtext.fallback": "stix",
    # axis settings
    "axes.titlesize": 20,
    "axes.labelsize": 22,
    "axes.linewidth": 1.6,
    "axes.unicode_minus": False,
    "axes.titlepad": 12,
    "xaxis.labellocation": "right",
    "yaxis.labellocation": "top",
    # legend settings
    "legend.fontsize": 15,
    "legend.frameon": False,
    "legend.numpoints": 1,
    # xtick settings
    "xtick.labelsize": 22,
    "xtick.major.size": 6,
    "xtick.major.width": 1.6,
    "xtick.minor.size": 3,
    "xtick.minor.width": 1.6,
    "xtick.major.pad": 6,
    "xtick.direction": "in",
    "xtick.top": True,
    "ytick.top": True,
    # ytick settings
    "ytick.labelsize": 22,
    "ytick.major.size": 6,
    "ytick.major.width": 1.6,
    "ytick.minor.size": 3,
    "ytick.minor.width": 1.6,
    "ytick.major.pad": 6,
    "ytick.direction": "in",
    "ytick.left": True,
    "ytick.right": True,
    # general plot settings
    "figure.facecolor": "white",
    "figure.figsize": (8.5, 6.5),
    # line style
    "lines.linewidth": 2.5,
    "errorbar.capsize": 1.5,
    "patch.linewidth": 2,
}

# Filter extra (labellocation) items if needed
SNOplus1 = {k: v for k, v in SNOplus1.items() if k in mpl.rcParams}

SNOplus = copy.deepcopy(SNOplus1)
