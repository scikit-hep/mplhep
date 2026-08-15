from __future__ import annotations

import os
import warnings

import matplotlib.pyplot as plt
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

"""
Style-dict tests for the LaTeX ("Tex") style variants.

These assert on rcParams rather than on rendered output, so they need no
texlive installation and run in the main CI on every platform and Python
version. Pixel-level rendering of the same styles lives in
tests/test_styles_latex.py, which only runs in the CI LaTeX workflow.

To test run:
pytest tests/test_styles_tex.py
"""

plt.switch_backend("Agg")

# Each Tex style is derived from a non-Tex sibling, so the two must stay
# identical outside the LaTeX-specific keys below.
STYLE_PAIRS = [
    ("CMS", "CMSTex"),
    ("ROOT", "ROOTTex"),
    ("DUNE", "DUNETex"),
    ("DUNE1", "DUNETex1"),
    ("ATLAS", "ATLASTex"),
    ("LHCb1", "LHCbTex1"),
    ("LHCb2", "LHCbTex2"),
]

TEX_STYLES = [tex for _, tex in STYLE_PAIRS]

LATEX_ONLY_KEYS = {"text.usetex", "text.latex.preamble", "pgf.rcfonts"}

# savefig.bbox each Tex style is expected to set. "tight" makes the saved image
# size depend on rendered text extents, which is why the image tests in
# test_styles_latex.py fail on dimensions when LaTeX metrics shift; pinning the
# value here catches a style gaining or losing that behaviour by accident.
EXPECTED_SAVEFIG_BBOX = {
    "CMSTex": None,
    "ROOTTex": None,
    "DUNETex": "tight",
    "DUNETex1": "tight",
    "ATLASTex": None,
    "LHCbTex1": "tight",
    "LHCbTex2": "tight",
}


def _apply(style):
    """Apply a style from a clean slate and return its rcParams as strings.

    Values are stringified because rcParams holds cyclers and arrays that do
    not compare cleanly with ==.
    """
    plt.rcParams.update(plt.rcParamsDefault)
    with warnings.catch_warnings():
        # ROOT/ROOTTex are deprecated aliases and warn by design.
        warnings.simplefilter("ignore", FutureWarning)
        plt.style.use(style)
    return {k: str(v) for k, v in plt.rcParams.items()}


@pytest.mark.parametrize("tex", TEX_STYLES)
def test_tex_style_enables_latex(tex):
    """Every Tex style must turn usetex on and ship a preamble."""
    rc = _apply(getattr(mh.style, tex))

    assert rc["text.usetex"] == "True"
    assert rc["text.latex.preamble"].strip(), f"{tex} has an empty LaTeX preamble"


@pytest.mark.parametrize(("base", "tex"), STYLE_PAIRS, ids=[t for _, t in STYLE_PAIRS])
def test_tex_style_matches_base_outside_latex_keys(base, tex):
    """A Tex style may differ from its sibling only in the LaTeX keys.

    This guards against a Tex style being rewritten as a standalone dict and
    then drifting from the style it is supposed to mirror.
    """
    base_rc = _apply(getattr(mh.style, base))
    tex_rc = _apply(getattr(mh.style, tex))

    differing = {k for k in base_rc if base_rc[k] != tex_rc[k]}

    assert differing <= LATEX_ONLY_KEYS, (
        f"{tex} differs from {base} outside the LaTeX keys: "
        f"{sorted(differing - LATEX_ONLY_KEYS)}"
    )


@pytest.mark.parametrize("tex", TEX_STYLES)
def test_tex_style_savefig_bbox(tex):
    """Pin savefig.bbox, which the image tests deliberately override."""
    rc = _apply(getattr(mh.style, tex))

    assert rc["savefig.bbox"] == str(EXPECTED_SAVEFIG_BBOX[tex])


@pytest.mark.parametrize("tex", TEX_STYLES)
def test_tex_style_str_alias_matches_dict(tex):
    """mh.style.use("CMSTex") must land on the same rcParams as the dict.

    tests/test_styles_latex.py checks this by rendering; doing it at the
    rcParams level needs no LaTeX, so it runs everywhere.
    """
    mh.rcParams.clear()
    expected = _apply(getattr(mh.style, tex))

    mh.rcParams.clear()
    plt.rcParams.update(plt.rcParamsDefault)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        mh.style.use(tex)
    actual = {k: str(v) for k, v in plt.rcParams.items()}

    assert actual == expected
