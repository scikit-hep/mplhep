# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

# -- Path setup --------------------------------------------------------------
import importlib
import inspect

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import subprocess
import sys
from functools import reduce

# Add mplhep to path for sphinx-automodapi
sys.path.insert(0, os.path.abspath("../../src"))

import mplhep  # noqa: E402

print("sys.path:", sys.path)
print("mplhep version:", mplhep.__version__)


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
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",  # Google and NumPy format docstrings
    # 'sphinx.ext.automodapi',
    "sphinx_rtd_theme",
]

numpydoc_show_class_members = False
nbsphinx_execute = "never"


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    mod = importlib.import_module(info["module"])
    modpath = [p for p in sys.path if mod.__file__.startswith(p)]
    if len(modpath) < 1:
        raise RuntimeError("Cannot deduce module path")
    modpath = modpath[0]
    obj = reduce(getattr, [mod] + info["fullname"].split("."))
    try:
        path = inspect.getsourcefile(obj)
        relpath = path[len(modpath) + 1 :]
        _, lineno = inspect.getsourcelines(obj)
    except TypeError:
        # skip property or other type that inspect doesn't like
        return None
    return "http://github.com/scikit-hep/mplhep/blob/{}/{}#L{}".format(
        githash, relpath, lineno
    )


intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
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
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

html_logo = "_static/mplhep.png"

html_theme_options = {
    "canonical_url": "",
    "analytics_id": "UA-XXXXXXX-1",  # Provided by Google in your dashboard
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "style_nav_header_background": "white",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
