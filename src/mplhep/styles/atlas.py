import matplotlib as mpl

ATLAS = {
    # From https://github.com/kratsg/ATLASstylempl
    "lines.linewidth": 1,
    "font.family": "sans-serif",
    "font.sans-serif": [
        "helvetica",
        "Helvetica",
        "Nimbus Sans L",
        "Mukti Narrow",
        "FreeSans",
    ],
    "font.size": 22,
    "mathtext.fontset": "stixsans",
    "mathtext.default": "rm",
    # figure layout
    "figure.figsize": (8.75, 5.92),
    "figure.facecolor": "white",
    "figure.subplot.bottom": 0.16,
    "figure.subplot.top": 0.93,
    "figure.subplot.left": 0.16,
    "figure.subplot.right": 0.95,
    # axes
    "axes.labelsize": 24,
    "axes.labelpad": 24,
    "xtick.top": True,
    "xtick.labelsize": 14,
    "xtick.major.size": 10,
    "xtick.minor.size": 5,
    "xtick.direction": "in",
    "xtick.minor.visible": True,
    "ytick.right": True,
    "ytick.labelsize": 14,
    "ytick.major.size": 14,
    "ytick.minor.size": 7,
    "ytick.direction": "in",
    "ytick.minor.visible": True,
    "lines.markersize": 8,
    # legend
    "legend.numpoints": 1,
    "legend.fontsize": 18,
    "legend.labelspacing": 0.3,
    "legend.frameon": False,
    "xaxis.labellocation": "right",
    "yaxis.labellocation": "top",
}

# Filter extra (labellocation) items if needed
ATLAS = {k: v for k, v in ATLAS.items() if k in mpl.rcParams}
