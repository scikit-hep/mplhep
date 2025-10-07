# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

# -- Path setup --------------------------------------------------------------
import importlib
import inspect
import logging
import os
import subprocess
import sys
from functools import reduce
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

import mplhep

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# Add mplhep to path for sphinx-automodapi
sys.path.insert(0, os.path.abspath("../../src"))


# -- Project information -----------------------------------------------------

project = "mplhep"
copyright = "2020, Andrzej Novak"
author = "Andrzej Novak"

# The full version, including alpha/beta/rc tags
version = mplhep.__version__.rsplit(".", 1)[0]
release = mplhep.__version__
githash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("ascii")

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "jupyter_sphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",  # Google and NumPy format docstrings
    # 'sphinx.ext.automodapi',
]

numpydoc_show_class_members = False
nb_execution_mode = "cache"
nb_execution_raise_on_error = True
nb_execution_show_tb = True


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None

    # Handle module aliasing for experiment modules
    module_name = info["module"]
    if module_name.startswith("mplhep.") and module_name.split(".")[-1] in [
        "cms",
        "atlas",
        "lhcb",
        "alice",
        "dune",
    ]:
        # Map aliased modules to their actual module names
        alias_map = {
            "mplhep.cms": "mplhep.exp_cms",
            "mplhep.atlas": "mplhep.exp_atlas",
            "mplhep.lhcb": "mplhep.exp_lhcb",
            "mplhep.alice": "mplhep.exp_alice",
            "mplhep.dune": "mplhep.exp_dune",
        }
        module_name = alias_map.get(module_name, module_name)

    try:
        mod = importlib.import_module(module_name)
    except ImportError:
        return None

    modpath = [p for p in sys.path if mod.__file__.startswith(p)]
    if len(modpath) < 1:
        msg = "Cannot deduce module path"
        raise RuntimeError(msg)
    modpath = modpath[0]

    try:
        obj = reduce(getattr, [mod, *info["fullname"].split(".")])
    except AttributeError:
        return None

    try:
        path = inspect.getsourcefile(obj)
        relpath = path[len(modpath) + 1 :]
        _, lineno = inspect.getsourcelines(obj)
    except (TypeError, OSError):
        # skip property or other type that inspect doesn't like
        return None
    return f"http://github.com/scikit-hep/mplhep/blob/{githash}/{relpath}#L{lineno}"


intersphinx_mapping = {
    # "python": ("https://docs.python.org/3", None),
    # "matplotlib": ("https://matplotlib.org/stable/", None),
    # "pandas": ("https://pandas.pydata.org/docs/", None),
    # "numpy": ("https://numpy.org/doc/stable/", None),  # stuck, takes forever
}

# The master toctree document.
master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "pydata_sphinx_theme"
here = Path(__file__).parent
staticfolder = here / "_static"

html_theme_options = {
    "logo": {
        "image_light": str(staticfolder / "mplhep.png"),
        "image_dark": str(staticfolder / "mplhep.png"),
    },
    "use_edit_page_button": True,
    # "analytics_id": "UA-XXXXXXX-1",  # Provided by Google in your dashboard
    # Toc options
    "collapse_navigation": False,
    "navigation_depth": 4,
}

html_context = {
    "github_user": "scikit-hep",
    "github_repo": "mplhep",
    "github_version": "master",
    "doc_path": "docs",
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_static_path = ["_static"]

# generate plots, moved here from index.rst


x = np.linspace(0, 10, 100)
y = np.sin(x)

allstyle = ["ATLAS1", "ATLAS2", "CMS", "LHCb1", "LHCb2", "ALICE", "DUNE1"]
allstyle = sorted(allstyle, key=lambda s: s.lower())
# allstyle = sorted(allstyle, key=lambda s: s.lower().endswith("tex"))
allstyle = sorted(allstyle, key=lambda s: s.lower().endswith("alt"))
here = Path("__file__").parent.resolve()  # jupyter workaround, use string


with Path(here / "_static/bkg_sig_plot.yaml").resolve().open() as f:
    plotdata = yaml.load(f, Loader=yaml.FullLoader)
logging.info("Creating gallery plots on the fly... (this takes a minute or two)")
for style in allstyle:
    plt.style.use("default")  # make sure it's reset
    plt.style.use(getattr(mplhep.style, style))

    plot = plotdata.copy()
    x = np.asarray(plot.pop("x"))
    data = tuple(plot.pop("Data"))
    for histtype in ["fill", "step", "errorbar", "band"]:
        for position in range(5):
            plt.figure()
            ax = plt.gca()
            title = f"{style} {histtype}"
            ax.set_title(title, y=1.03)
            mplhep.histplot(data, histtype=histtype, label="Data", ax=ax)
            for label, y in plot.items():
                ax.plot(x, np.asarray(y), label=label)

            kwargs = {
                "text": "Preliminary",
                "data": True,
                "ax": ax,
                "year": 2016,
                "loc": position,
                "lumi": 9,
            }
            if "atlas" in style.lower():
                mplhep.atlas.label(**kwargs)
            elif "cms" in style.lower():
                mplhep.cms.label(**kwargs)
            elif "lhcb" in style.lower():
                mplhep.lhcb.label(**kwargs)
            elif "dune" in style.lower():
                mplhep.dune.label(**kwargs)
            ax.legend()
            ax.set_xlabel(r"$m_{\mu\mu}$ [GeV]")
            ax.set_ylabel("Events")
            path = Path(
                here / f"_static/_generated/{style}/{histtype}/pos{position}.png"
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(path)
            plt.close()
