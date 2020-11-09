"""LHCb-like plot style 2

This style resembles the LHCb plotting style; however it is an approximation and
not an official style.

In order to optimally use the style, the
the following lines should be used in your python script:
  plt.xlabel(..., ha='center', y=1)
  plt.ylabel(..., ha='right', x=1, y=1)
  plt.legend(loc='best')
  plt.minorticks_on()

Contributed by Jonas Eschle <Jonas.Eschle@cern.ch>
based on the works of Kevin Dungs, Tim Head, Thomas Schietinger,
                      Andrew Powell, Chris Parkes, Elena Graverini
                      and Niels Tuning
"""

import matplotlib as mpl
from cycler import cycler

colors = [
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
markers = ["o", "s", "D", "^", "v", "<", ">", "P", "X", "*"]

LHCb2 = {
    # Plot properties
    "axes.labelsize": 32,
    "axes.linewidth": 2,
    "axes.facecolor": "white",
    # Custom colors
    "axes.prop_cycle": cycler("color", colors),
    # + cycler("marker", markers)  # TODO: markers?
    "axes.formatter.min_exponent": 3,
    # Figure properties
    "figure.figsize": (8, 8),
    "figure.dpi": 2500,
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
    # Inherit the background color from the plot
    "legend.facecolor": "inherit",
    "legend.numpoints": 1,
    "legend.labelspacing": 0.2,
    "legend.fontsize": 28,
    # "legend.title_fontsize": 28,  # TODO: needed?
    # Automatically choose the best location
    "legend.loc": "best",
    # Space between the handles and their labels
    "legend.handletextpad": 0.75,
    # Space between the borders of the plot and the legend
    "legend.borderaxespad": 1.0,
    # "legend.edgecolor": "white",  # TODO: needed?
    # Lines settings
    "lines.linewidth": 3,
    "lines.markeredgewidth": 0,
    "lines.markersize": 8,
    # Saved figure settings
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
    "savefig.format": "pdf",
    # Ticks settings
    "xtick.major.size": 14,
    "xtick.minor.size": 7,
    "xtick.major.width": 2,
    "xtick.minor.width": 2,
    "xtick.major.pad": 10,
    "xtick.minor.pad": 10,
    "xtick.labelsize": 30,
    "xtick.direction": "in",
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
    "yaxis.labellocation": "top",  # TODO: 'center'?
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
