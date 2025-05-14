from __future__ import annotations

import matplotlib as mpl
from cycler import cycler

# DUNE style based on dune_plot_style package
DUNE = {
    # Font configuration
    "font.sans-serif": [
        "Helvetica",
        "Helvetica Neue",
        "Nimbus Sans",
        "Liberation Sans",
        "Arial",
    ],
    "font.family": "sans-serif",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Helvetica",
    "mathtext.bf": "Helvetica:bold",
    "mathtext.sf": "Helvetica",
    "mathtext.it": "Helvetica:italic",
    "mathtext.tt": "Helvetica",
    "mathtext.default": "regular",
    # Figure size
    "figure.figsize": (10.0, 10.0),
    "figure.facecolor": "white",
    # Text properties
    "text.hinting_factor": 8,
    "font.size": 26,
    # Axes properties
    "axes.facecolor": "white",
    "axes.edgecolor": "black",
    "axes.grid": False,
    "axes.linewidth": 1.0,
    "axes.labelsize": "xx-large",
    "axes.titlesize": 36,
    # Use Okabe-Ito colors with ordering that matches DUNE logo colors
    "axes.prop_cycle": cycler(
        "color",
        [
            "#000000",
            "#D55E00",
            "#56B4E9",
            "#E69F00",
            "#009E73",
            "#CC79A7",
            "#0072B2",
            "#F0E442",
        ],
    ),
    # Line properties
    "lines.linewidth": 2.0,
    # Patch properties (used for histograms)
    "patch.linewidth": 1.5,
    "patch.facecolor": "blue",
    "patch.edgecolor": "#eeeeee",
    "patch.antialiased": True,
    # Image properties
    "image.cmap": "cividis",  # Colo(u)r Vision Deficiency friendly
    # Grid properties (off by default)
    "grid.color": "#b2b2b2",
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    # Legend properties
    "legend.fontsize": 12,
    "legend.frameon": False,
    # Tick properties
    "xtick.color": "black",
    "xtick.direction": "in",
    "xtick.labelsize": "x-large",
    "xtick.major.size": 10,
    "xtick.minor.size": 5,
    "xtick.minor.visible": True,
    "xtick.top": True,
    "ytick.color": "black",
    "ytick.direction": "in",
    "ytick.labelsize": "x-large",
    "ytick.major.size": 10,
    "ytick.minor.size": 5,
    "ytick.minor.visible": True,
    "ytick.right": True,
}

# Filter extra items if needed
DUNE = {k: v for k, v in DUNE.items() if k in mpl.rcParams}

# Add a tex variant
DUNETex = {
    **DUNE,
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{siunitx},\sisetup{detect-all}, \
                              \usepackage{helvet},\usepackage{sansmath}, \
                              \sansmath",
}
