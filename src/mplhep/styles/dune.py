from __future__ import annotations

import copy

import matplotlib as mpl
from cycler import cycler

# DUNE style based on dune_plot_style package
DUNE1 = {
    # Font configuration
    "font.sans-serif": [
        "TeX Gyre Heros",  # Better, free Helvetica-like font with math support
        "Helvetica",
        "Helvetica Neue",
        "Nimbus Sans L",
        "Liberation Sans",
        "Arial",
        "FreeSans",
    ],
    "font.family": "sans-serif",
    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Heros",
    "mathtext.bf": "TeX Gyre Heros:bold",
    "mathtext.sf": "TeX Gyre Heros",
    "mathtext.it": "TeX Gyre Heros:italic",
    "mathtext.tt": "TeX Gyre Heros",
    "mathtext.cal": "TeX Gyre Heros",
    "mathtext.default": "regular",
    # Figure configuration
    "figure.figsize": (10, 10),
    "figure.facecolor": "white",
    "figure.dpi": 100,
    "figure.autolayout": True,
    # Text properties
    "text.hinting_factor": 8,
    "font.size": 22,
    # Axes properties
    "axes.facecolor": "white",
    "axes.edgecolor": "black",
    "axes.grid": False,
    "axes.linewidth": 1.5,
    "axes.labelsize": "medium",
    "axes.titlesize": 36,
    # "axes.labelpad": 8,  # Better spacing between labels and axes
    # "axes.formatter.limits": "-3, 4",  # Better scientific notation limits
    "axes.formatter.use_mathtext": True,
    "axes.unicode_minus": False,  # Use ASCII minus for better compatibility
    "axes.xmargin": 0.0,  # Small margin for better plot bounds
    "axes.ymargin": 0.0,
    # Enhanced color cycle - DUNE logo colors first, then accessibility-optimized sequence
    "axes.prop_cycle": cycler(
        "color",
        [
            "#000000",  # Black
            "#D55E00",  # DUNE Orange (primary)
            "#56B4E9",  # DUNE Sky Blue (primary)
            "#E69F00",  # DUNE Yellow/Gold (primary)
            "#009E73",  # Green (accessible)
            "#CC79A7",  # Pink (accessible)
            "#0072B2",  # Blue (accessible)
            "#F0E442",  # Bright Yellow (accessible)
        ],
    ),
    # Line properties
    "lines.linewidth": 2.0,
    "lines.markersize": 8,
    # Patch properties (histograms)
    "patch.linewidth": 1.5,
    "patch.facecolor": "blue",
    "patch.edgecolor": "black",
    "patch.antialiased": True,
    # Image properties - Color Vision Deficiency friendly
    "image.cmap": "cividis",
    "image.aspect": "auto",
    # Grid properties - Improved styling when enabled
    "grid.color": "#b2b2b2",
    "grid.linestyle": ":",  # Dotted style for less visual interference
    "grid.linewidth": 0.5,
    "grid.alpha": 0.8,
    # Legend properties
    "legend.fontsize": 12,
    "legend.title_fontsize": "large",
    "legend.frameon": False,
    "legend.handlelength": 2.0,
    "legend.borderpad": 0.8,
    "legend.columnspacing": 1.0,
    "legend.labelspacing": 0.5,
    # Automatically choose the best location
    "legend.loc": "best",
    # Enhanced tick properties
    "xtick.color": "black",
    "xtick.direction": "in",
    "xtick.labelsize": "small",
    "xtick.major.size": 10,
    "xtick.minor.size": 5,
    "xtick.major.pad": 6,
    "xtick.minor.visible": True,
    "xtick.top": True,
    "xtick.bottom": True,
    "xtick.major.top": True,
    "xtick.major.bottom": True,
    "xtick.minor.top": True,
    "xtick.minor.bottom": True,
    "ytick.color": "black",
    "ytick.direction": "in",
    "ytick.labelsize": "small",
    "ytick.major.size": 10,
    "ytick.minor.size": 5,
    "ytick.major.pad": 6,
    "ytick.minor.visible": True,
    "ytick.right": True,
    "ytick.left": True,
    "ytick.major.left": True,
    "ytick.major.right": True,
    "ytick.minor.left": True,
    "ytick.minor.right": True,
    # Enhanced axis label positioning (like other HEP experiments)
    "xaxis.labellocation": "right",
    "yaxis.labellocation": "top",
    # Save figure properties
    "savefig.transparent": False,
    "savefig.bbox": "tight",
    # "savefig.pad_inches": 0.1,
}

# Filter extra items if needed
DUNE1 = {k: v for k, v in DUNE1.items() if k in mpl.rcParams}

# Add a tex variant
DUNETex1 = {
    **DUNE1,
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{siunitx}\sisetup{detect-all}\usepackage{tgheros}\renewcommand{\familydefault}{\sfdefault}\usepackage{sansmath}\sansmath\usepackage{amsmath}\usepackage{physics}",
}

# moving targets
DUNE = copy.deepcopy(DUNE1)
DUNETex = copy.deepcopy(DUNETex1)
