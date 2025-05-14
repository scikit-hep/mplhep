from __future__ import annotations

import matplotlib as mpl
from cycler import cycler

from .._deprecate import deprecated_dict

colors1 = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]
markers1 = ["o", "s", "D", "^", "v", "<", ">", "P", "X", "*"]

LHCb1 = {
    # Plot properties
    "axes.labelsize": 32,
    "axes.linewidth": 2,
    "axes.facecolor": "white",
    # Custom colors
    "axes.prop_cycle": cycler("color", colors1) + cycler("marker", markers1),
    "axes.formatter.min_exponent": 3,
    "axes.unicode_minus": False,
    # Figure properties
    "figure.figsize": (12, 9),
    "figure.dpi": 100,
    # Outer frame color
    "figure.facecolor": "white",
    "figure.autolayout": True,
    # Set default font to Times New Roman
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 14,
    "font.weight": 400,
    # Draw the legend on a solid background
    "legend.frameon": True,
    "legend.fancybox": False,
    # Inherit the background color from the plot
    "legend.facecolor": "inherit",
    "legend.numpoints": 1,
    "legend.labelspacing": 0.2,
    "legend.fontsize": 28,
    "legend.title_fontsize": 28,
    # Automatically choose the best location
    "legend.loc": "best",
    # Space between the handles and their labels
    "legend.handletextpad": 0.75,
    # Space between the borders of the plot and the legend
    "legend.borderaxespad": 1.0,
    "legend.edgecolor": "white",
    # Lines settings
    "lines.linewidth": 4,
    "lines.markeredgewidth": 0,
    "lines.markersize": 8,
    # Saved figure settings
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
    "savefig.format": "pdf",
    # Ticks settings
    "xtick.major.size": 14,
    "xtick.minor.size": 7,
    "xtick.major.width": 2,
    "xtick.minor.width": 2,
    "xtick.major.pad": 10,
    "xtick.minor.pad": 10,
    "xtick.direction": "in",
    "xtick.labelsize": 30,
    "ytick.major.size": 14,
    "ytick.minor.size": 7,
    "ytick.major.width": 2,
    "ytick.minor.width": 2,
    "ytick.major.pad": 10,
    "ytick.minor.pad": 10,
    "ytick.direction": "in",
    "ytick.labelsize": 30,
    # Legend frame border size
    # WARNING: this affects every patch object
    # (i.e. histograms and so on)
    "patch.linewidth": 2,
    "xaxis.labellocation": "right",
    "yaxis.labellocation": "top",
}

# Filter extra (labellocation) items if needed
LHCb1 = {k: v for k, v in LHCb1.items() if k in mpl.rcParams}

ROOT = deprecated_dict(
    LHCb1, message="'ROOT' style dict is deprecated, please use 'LHCb' instead"
)

LHCbTex1 = {
    **LHCb1,
    # Use LaTeX rendering by default
    # (overrides default font)
    "text.usetex": True,
    # Use the LaTeX version of Times New Roman
    "text.latex.preamble": r"\usepackage{mathptmx}",
    "pgf.rcfonts": False,
}

ROOTTex = deprecated_dict(
    LHCbTex1, message="'ROOT' style dict is deprecated, please use 'LHCb' instead"
)

colors2 = [
    "#0078FF",
    "#FF6600",
    "#0AAFB6",
    "#FF3333",
    "#0000FF",
    "#00CC00",
    "#BF8040",
    "#FF33CC",
    "#FF7733",
    "#BFD1D4",
]

LHCb2 = {
    # Plot properties
    "axes.labelsize": 32,
    "axes.linewidth": 2,
    "axes.facecolor": "white",
    # Custom colors
    "axes.prop_cycle": cycler("color", colors2),
    "axes.formatter.min_exponent": 3,
    "axes.titlesize": 28,
    # Errorbar properties
    "errorbar.capsize": 2.5,
    # Figure properties
    "figure.figsize": (12, 9),
    "figure.dpi": 100,
    # Outer frame color
    "figure.facecolor": "white",
    "figure.autolayout": True,
    # Set default font to Times New Roman
    "font.family": "serif",
    "font.serif": ["Tex Gyre Termes"],
    "font.cursive": ["Tex Gyre Termes"],
    "mathtext.fontset": "custom",
    "mathtext.rm": "Tex Gyre Termes",
    "mathtext.bf": "Tex Gyre Termes:bold",
    "mathtext.sf": "Tex Gyre Termes",
    "mathtext.it": "Tex Gyre Termes:italic",
    "mathtext.tt": "Tex Gyre Termes",
    "mathtext.cal": "Tex Gyre Termes",
    "font.size": 14,
    "font.weight": 400,
    # Draw the legend on a solid background
    "legend.frameon": False,
    "legend.fancybox": True,
    # Inherit the background color from the plot
    "legend.facecolor": "inherit",
    "legend.numpoints": 1,
    "legend.labelspacing": 0.2,
    "legend.fontsize": 28,
    "legend.title_fontsize": 28,
    # Automatically choose the best location
    "legend.loc": "best",
    # Space between the handles and their labels
    "legend.handletextpad": 0.75,
    # Space between the borders of the plot and the legend
    "legend.borderaxespad": 1.0,
    # Lines settings
    "lines.linewidth": 3.3,
    "lines.markeredgewidth": 1.5,
    "lines.markersize": 16,
    "lines.elinewidth": 1.5,
    # Saved figure settings
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
    "savefig.format": "pdf",
    # Ticks settings
    # xticks
    "xtick.minor.visible": True,
    "xtick.top": True,
    "xtick.major.size": 14,
    "xtick.minor.size": 7,
    "xtick.major.width": 2,
    "xtick.minor.width": 2,
    "xtick.major.pad": 10,
    "xtick.minor.pad": 10,
    "xtick.labelsize": 30,
    "xtick.direction": "in",
    # yticks
    "ytick.minor.visible": True,
    "ytick.right": True,
    "ytick.major.size": 14,
    "ytick.minor.size": 7,
    "ytick.major.width": 2,
    "ytick.minor.width": 2,
    "ytick.major.pad": 10,
    "ytick.minor.pad": 10,
    "ytick.labelsize": 30,
    "ytick.direction": "in",
    # Legend frame border size
    # WARNING: this affects every patch object
    # (i.e. histograms and so on)
    "patch.linewidth": 2,
    "xaxis.labellocation": "right",
    "yaxis.labellocation": "top",
}

# Filter extra (labellocation) items if needed
LHCb2 = {k: v for k, v in LHCb2.items() if k in mpl.rcParams}

LHCbTex2 = {
    **LHCb2,
    # Use LaTeX rendering by default
    # (overrides default font)
    "text.usetex": True,
    # Use the LaTeX version of Times New Roman
    "text.latex.preamble": r"\usepackage{txfonts}",
    "pgf.rcfonts": False,
}

# alias LHCb Style

lhcb_depr_msg = (
    "'LHCb' style is deprecated as it may change in the future. Please use 'LHCb1' (which is"
    " the same as currently 'LHCb') or 'LHCb2'."
)
LHCb = deprecated_dict(LHCb1, message=lhcb_depr_msg, warning=FutureWarning)
LHCbTex = deprecated_dict(LHCbTex1, message=lhcb_depr_msg, warning=FutureWarning)
