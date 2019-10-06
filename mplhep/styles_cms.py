# PRL figsize / Elsevier figsize, Nature is somewhere in between
# single column width -  86 mm (3.386in) /  90 mm (3.543in)
# double column width - 172 mm (6.772in) / 180 mm (7.087in)
# For now size to 10

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

    "axes.linewidth": 2,

    "savefig.transparent": False,

    }

ROOTtex = {
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{siunitx},\sisetup{detect-all}, \
                              \usepackage{helvet},\usepackage{sansmath}, \
                              \sansmath"
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
