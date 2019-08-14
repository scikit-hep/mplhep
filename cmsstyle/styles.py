ROOT = {
    "font.sans-serif": ["TeX Gyre Heros", "Helvetica", "Arial"],
    "font.family": "sans-serif",

    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Heros",
    "mathtext.bf": "TeX Gyre Heros:bold",
    "mathtext.sf": "TeX Gyre Heros",
    "mathtext.it": "TeX Gyre Heros:italic",
    "mathtext.tt": "TeX Gyre Heros",

    "figure.figsize": (10.0, 10.0),

    "font.size": 26,
    "axes.labelsize": "medium",
    "xtick.labelsize": "small",
    "ytick.labelsize": "small",

    "legend.fontsize": "small",
    "legend.handlelength": 1.5,
    "legend.borderpad": 0.5,
    "legend.frameon": False,

    "xtick.direction": "in",
    "xtick.major.size": 12,
    "xtick.minor.size": 6,
    "xtick.major.pad": 6,

    "xtick.top": True,
    "xtick.major.top": True,
    "xtick.major.bottom": True,
    "xtick.minor.top": True,
    "xtick.minor.bottom": True,
    "xtick.minor.visible": True,

    "ytick.direction": "in",
    "ytick.major.size": 12,
    "ytick.minor.size": 6.0,

    "ytick.right": True,
    "ytick.major.left": True,
    "ytick.major.right": True,
    "ytick.minor.left": True,
    "ytick.minor.right": True,
    "ytick.minor.visible": True,

    "grid.alpha": 0.8,
    "grid.linestyle": ":",

    "axes.autolimit_mode": "round_numbers",
    "axes.linewidth": 2,

    "savefig.transparent": False,

    }

ROOTtex = {
    "text.usetex": True,
    "text.latex.preamble" : r"\usepackage{siunitx},\sisetup{detect-all},\usepackage{helvet},\usepackage{sansmath},\sansmath"
}

fira = {
    "font.sans-serif": "Fira Sans"
}

firamath = {
    "mathtext.fontset": "custom",
    "mathtext.rm": "Fira Math:regular",
    "mathtext.bf": "Fira Math:medium",
    "mathtext.sf": "Fira Math",
    "mathtext.it": "Fira Math:regular:italic",
    "mathtext.tt": "Fira Mono",
}

fabiola = {
    "font.sans-serif": "Comic Sans MS",
}


ATLAS = {
    # From https://github.com/kratsg/ATLASstylempl
    "lines.linewidth": 1,

    "font.family": "sans-serif",
    "font.sans-serif": ["helvetica", "Helvetica", "Nimbus Sans L", "Mukti Narrow", "FreeSans"],
    "font.size": 18,
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
    "axes.labelsize": 30,
    "axes.labelpad": 30,
    "xtick.top": True,
    "xtick.labelsize": 19,
    "xtick.major.size": 10,
    "xtick.minor.size": 5,
    "xtick.direction": "in",
    "xtick.minor.visible": True,
    "ytick.right": True,
    "ytick.labelsize": 19,
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
}
