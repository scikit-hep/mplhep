from cycler import cycler
from ._deprecate import deprecated_dict
import matplotlib as mpl

colors = [
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
markers = ["o", "s", "D", "^", "v", "<", ">", "P", "X", "*"]

LHCb = {
    # Plot properties
    "axes.labelsize": 32,
    "axes.linewidth": 2,
    "axes.facecolor": "white",
    # Custom colors
    "axes.prop_cycle": cycler("color", colors) + cycler("marker", markers),
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
LHCb = {k: v for k, v in LHCb.items() if k in mpl.rcParams}

ROOT = deprecated_dict(
    LHCb, message="'ROOT' style dict is deprecated, please use 'LHCb' instead"
)

LHCbTex = {
    **LHCb,
    # Use LaTeX rendering by default
    # (overrides default font)
    "text.usetex": True,
    # Use the LaTeX version of Times New Roman
    "text.latex.preamble": r"\usepackage{mathptmx}",
    "pgf.rcfonts": False,
}

ROOTTex = deprecated_dict(
    LHCbTex, message="'ROOT' style dict is deprecated, please use 'LHCb' instead"
)
