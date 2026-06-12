"""Tests for mplhep label functionality.

To run tests:
    pytest --mpl

When adding new tests:
    pytest --mpl-generate-path=tests/baseline
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

# Set environment before importing mplhep
os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh
from mplhep.label import (
    ExpLabel,
    ExpText,
    _descent_from_layout,
    _parse_com,
    _safe_get_renderer,
    exp_label,
    exp_text,
    save_variations,
)

plt.switch_backend("Agg")

# Test constants
COLORS = ["red", "blue", "green", "orange"]
POSITIONS = ["right", "left", "below", "above"]
LOCATIONS = [
    "upper left",
    "upper right",
    "lower left",
    "lower right",
    "over left",
    "over right",
]


def _setup_test_plot(ax, xlim=(0, 1), ylim=(0, 1)):
    """Common setup for test plots."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def _draw_text_boundary_lines(txt_obj, ax=None, color="gray", alpha=0.5):
    """Draw boundary lines around text object to visualize its extents.

    Parameters
    ----------
    txt_obj : matplotlib.text.Text
        Text object to draw boundaries around
    ax : matplotlib.axes.Axes, optional
        Axes to draw on, by default None (uses current axes)
    color : str, optional
        Color of boundary lines, by default "gray"
    alpha : float, optional
        Transparency of boundary lines, by default 0.5
    """
    ax = plt.gca() if ax is None else ax
    _layout = txt_obj._get_layout(_safe_get_renderer(ax.figure))
    bbox = _layout[0]
    descent = _descent_from_layout(_layout)
    ax_width = ax.get_position().width * ax.figure.get_size_inches()[0]
    ax_height = ax.get_position().height * ax.figure.get_size_inches()[1]
    dpi = ax.figure.dpi

    text_width = bbox.width / ax_width / dpi
    text_height = bbox.height / ax_height / dpi
    yoffset = descent / ax_height / dpi

    # Get reference position accounting for horizontal alignment
    ref_ha = txt_obj.get_horizontalalignment()
    ref_x = txt_obj.get_position()[0]
    ref_y = txt_obj.get_position()[1]

    if ref_ha == "center":
        left = ref_x - text_width / 2
        right = ref_x + text_width / 2
    elif ref_ha == "right":
        left = ref_x - text_width
        right = ref_x
    else:  # "left" or default
        left = ref_x
        right = ref_x + text_width

    # Calculate vertical boundaries based on vertical alignment
    va = txt_obj.get_verticalalignment()
    if va == "bottom":
        bottom = ref_y + yoffset
        top = ref_y + yoffset + text_height
    elif va == "top":
        bottom = ref_y + yoffset - text_height
        top = ref_y + yoffset
    else:  # baseline or other
        bottom = ref_y + yoffset
        top = ref_y + yoffset + text_height

    # Draw boundary lines
    ax.axvline(x=left, color=color, alpha=alpha, linestyle="--", linewidth=1)
    ax.axvline(x=right, color=color, alpha=alpha, linestyle="--", linewidth=1)
    ax.axhline(y=bottom, color=color, alpha=alpha, linestyle="--", linewidth=1)
    ax.axhline(y=top, color=color, alpha=alpha, linestyle="--", linewidth=1)


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_add_text_placement():
    fig, ax = plt.subplots(figsize=(5, 5))
    for loc in LOCATIONS:
        mh.add_text("XYZ", ax=ax, loc=loc)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_add_text_placement_asym():
    fig, ax = plt.subplots(figsize=(15, 5))
    for loc in LOCATIONS:
        mh.add_text("XYZ", ax=ax, loc=loc)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_add_text_placement_any():
    fig, ax = plt.subplots(figsize=(15, 5))
    mh.add_text("XYZ", ax=ax, loc="upper left", pad=10)
    mh.add_text("XYZ", ax=ax, loc="upper right", xpad=5, ypad=20)
    mh.add_text("XYZ", ax=ax, x=0.5, y=0.5, ha="center", va="center")
    return fig


@pytest.mark.parametrize(
    "fontname", [None, "Tex Gyre Heros"], ids=["default", "tex_gyre_heros"]
)
@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_append_text_placement(fontname):
    fig, ax = plt.subplots()

    # Common kwargs for reference texts
    text_kwargs = {
        "ax": ax,
        "ha": "center",
        "fontsize": "xx-large",
        "fontname": fontname,
    }

    # Create reference texts with different horizontal alignments
    ref_specs = [
        ("XyzZ1", 0.25, 0.7, "red"),
        ("XyzZ2", 0.75, 0.7, "blue"),
        ("1XyZ2", 0.25, 0.3, "red"),
        ("1XyZ1", 0.75, 0.3, "blue"),
    ]

    texts = []
    for text, x, y, color in ref_specs:
        t = mh.add_text(text, x=x, y=y, **text_kwargs)
        _draw_text_boundary_lines(t, color=color, alpha=0.3)
        texts.append(t)

    # Test all append positions
    append_base_kwargs = {"ax": ax, "fontname": fontname}
    font_sizes = ["xx-large", "small", "xx-large", "small"]

    for i, app_pos in enumerate(POSITIONS):
        append_kwargs = {**append_base_kwargs, "loc": app_pos, "color": COLORS[i]}
        # Use original labeling pattern to match baseline images
        labels = ["1", "2", "2", "1"]  # Original pattern from t1, t2, t3, t4
        for _, (text_obj, font_size, label_prefix) in enumerate(
            zip(texts, font_sizes, labels, strict=True)
        ):
            label = f"{label_prefix}-{app_pos}"
            mh.append_text(label, text_obj, fontsize=font_size, **append_kwargs)

    _setup_test_plot(ax)
    ax.set_title(f"Test append_text - {fontname}")
    return fig


@pytest.mark.parametrize("fontsize", ["large", "x-small"])
@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_append_text_alignment(fontsize):
    fig, ax = plt.subplots()

    # Common kwargs for reference texts
    ref_kwargs = {"ax": ax, "fontsize": "large"}

    # Create reference texts with different alignments
    alignment_specs = [
        # (text, x, y, ha, va, group)
        ("yha-left", 0.15, 0.7, "left", "bottom", "top"),
        ("yha-center", 0.5, 0.7, "center", "bottom", "top"),
        ("yha-right", 0.85, 0.7, "right", "bottom", "top"),
        ("yva-top", 0.15, 0.3, "center", "top", "bottom"),
        ("yva-base", 0.5, 0.3, "center", "baseline", "bottom"),
        ("yva-bot", 0.85, 0.3, "center", "bottom", "bottom"),
    ]

    texts = {"top": [], "bottom": []}
    for text, x, y, ha, va, group in alignment_specs:
        t = mh.add_text(text, x=x, y=y, ha=ha, va=va, **ref_kwargs)
        _draw_text_boundary_lines(t, color="gray", alpha=0.25)
        texts[group].append(t)

    # Test all append positions
    append_kwargs = {"ax": ax, "fontsize": fontsize}

    # Use original labeling pattern to match baseline images
    for group_name, text_list in texts.items():
        group_label = "1" if group_name == "top" else "2"
        for t in text_list:
            for i, app_pos in enumerate(POSITIONS):
                label = f"{group_label}-{app_pos}"
                mh.append_text(label, t, loc=app_pos, color=COLORS[i], **append_kwargs)
    _setup_test_plot(ax)
    title = "Test append_text va/ha"
    if fontsize is not None:
        title += f", fontsize={fontsize}"
    ax.set_title(title)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_append_text_multiline():
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create one reference text in the center
    ref_text = mh.add_text(
        "Reference", ax=ax, x=0.5, y=0.5, ha="center", va="baseline", fontsize="x-large"
    )

    # Draw boundary lines for reference text
    _draw_text_boundary_lines(ref_text, color="gray", alpha=0.3)

    # Test multiline appended text in all four directions
    multiline_text = "Line1\nLine2\nLine3"
    append_kwargs = {"ax": ax, "fontsize": "medium"}

    for i, direction in enumerate(POSITIONS):
        mh.append_text(
            multiline_text, ref_text, loc=direction, color=COLORS[i], **append_kwargs
        )

    _setup_test_plot(ax)
    ax.set_title("Test append_text with multiline text")
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_exp_text_scilocator_adjust():
    """Test scilocator_adjust parameter with scientific notation on y-axis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Create plots with scientific notation on y-axis
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * 1e6 + 5e6

    ax1.plot(x, y)
    exp_text(exp="TEST", text="Simulation", loc=0, ax=ax1, scilocator_adjust=True)
    mh.add_text("scilocator_adjust=True", loc="lower right", ax=ax1, fontsize=10)

    ax2.plot(x, y)
    exp_text(exp="TEST", text="Simulation", loc=0, ax=ax2, scilocator_adjust=False)
    mh.add_text("scilocator_adjust=False", loc="lower right", ax=ax2, fontsize=10)

    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_exp_label_scilocator_adjust():
    """Test scilocator_adjust parameter in exp_label with scientific notation on y-axis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Create plots with scientific notation on y-axis
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * 1e6 + 5e6

    ax1.plot(x, y)
    exp_label(
        exp="TEST",
        data=False,
        lumi=138,
        year=2018,
        loc=0,
        ax=ax1,
        scilocator_adjust=True,
    )
    mh.add_text("scilocator_adjust=True", loc="lower right", ax=ax1, fontsize=10)

    ax2.plot(x, y)
    exp_label(
        exp="TEST",
        data=False,
        lumi=138,
        year=2018,
        loc=0,
        ax=ax2,
        scilocator_adjust=False,
    )
    mh.add_text("scilocator_adjust=False", loc="lower right", ax=ax2, fontsize=10)

    return fig


@pytest.mark.parametrize(
    ("com", "expected"),
    [
        (None, (None, None)),
        (13, ("13", "TeV")),
        (13.6, ("13.6", "TeV")),
        ("13.6", ("13.6", "TeV")),
        ("500 GeV", ("500", "GeV")),
        ("500GeV", ("500", "GeV")),
        ("900 MeV", ("900", "MeV")),
        (".5 GeV", (".5", "GeV")),
    ],
)
def test_parse_com(com, expected):
    assert _parse_com(com) == expected


@pytest.mark.parametrize(
    ("com", "expected_in", "expected_not_in"),
    [
        ("13", "(13 TeV)", None),
        (None, None, "TeV"),
        ("500 GeV", "(500 GeV)", "TeV"),
        ("900 MeV", "(900 MeV)", "TeV"),
    ],
)
def test_exp_label_com(com, expected_in, expected_not_in):
    """com units are respected and com=None omits the energy entirely."""
    fig, ax = plt.subplots()
    _, _, lumi_text, _ = exp_label(exp="TEST", lumi=100, com=com, ax=ax)
    label = lumi_text.get_text()
    if expected_in is not None:
        assert expected_in in label
    if expected_not_in is not None:
        assert expected_not_in not in label
    assert "100" in label
    plt.close(fig)


@pytest.mark.parametrize(
    ("com", "expected_in", "expected_not_in"),
    [
        ("13", r"\mathrm{13\ TeV}", None),
        (None, None, r"\sqrt{s}"),
        ("500 GeV", r"\mathrm{500\ GeV}", "TeV"),
    ],
)
def test_exp_label_com_atlas_style(com, expected_in, expected_not_in):
    """ATLAS-style (loc=4) sqrt(s) line respects units and com=None."""
    fig, ax = plt.subplots()
    _, _, lumi_text, _ = exp_label(exp="TEST", lumi=139, com=com, loc=4, ax=ax)
    label = lumi_text.get_text()
    if expected_in is not None:
        assert expected_in in label
    if expected_not_in is not None:
        assert expected_not_in not in label
    assert "139" in label
    plt.close(fig)


@pytest.mark.parametrize("loc", [0, 4])
def test_exp_label_com_none_no_lumi(loc):
    """com=None with no lumi/year creates no luminosity text at all."""
    fig, ax = plt.subplots()
    _, _, lumi_text, _ = exp_label(exp="TEST", com=None, loc=loc, ax=ax)
    assert lumi_text is None
    plt.close(fig)


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_exp_label_com_variants():
    """Visual test for com=None and com with explicit units."""
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    exp_label(exp="TEST", lumi=100, ax=axs[0, 0])
    exp_label(exp="TEST", lumi=100, com=None, ax=axs[0, 1])
    exp_label(exp="TEST", lumi=100, com="500 GeV", ax=axs[1, 0])
    exp_label(exp="TEST", lumi=100, com="500 GeV", loc=4, ax=axs[1, 1])
    return fig


# --- Regression tests for Bug D: deprecated label= kwarg ---


def test_exp_label_deprecated_label_kwarg():
    """Regression: exp_label(label='Preliminary') must use the value, not silently drop it."""
    fig, ax = plt.subplots()
    with pytest.warns(FutureWarning):
        exp_obj, text_obj, _, _ = exp_label(exp="TEST", label="Preliminary", ax=ax)
    # The text should appear in the secondary text object
    assert text_obj is not None
    assert "Preliminary" in text_obj.get_text()
    plt.close(fig)


def test_exp_cms_deprecated_label_kwarg():
    """Regression: mh.cms.label(label='Preliminary') must forward the value."""
    fig, ax = plt.subplots()
    with pytest.warns(FutureWarning):
        _, text_obj, _, _ = mh.cms.label(label="Preliminary", ax=ax)
    assert text_obj is not None
    assert "Preliminary" in text_obj.get_text()
    plt.close(fig)


def test_exp_label_no_duplicate_deprecation_pub():
    """Regression: duplicate @deprecate_parameter('pub') must not raise on call."""
    fig, ax = plt.subplots()
    # This should not raise TypeError about duplicate decorator application
    with pytest.warns(FutureWarning):
        exp_label(exp="TEST", pub="Note", ax=ax)
    plt.close(fig)


# --- Regression tests for Bug B: save_variations artist lookup ---


def test_save_variations_exp_targets_explabel(tmp_path):
    """Regression: save_variations(exp=...) must update ExpLabel, not ExpText."""
    fig, ax = plt.subplots()
    exp_label(exp="CMS", text="Preliminary", ax=ax)

    original_exp_texts = [
        t.get_text() for t in ax.get_children() if isinstance(t, ExpLabel)
    ]
    assert original_exp_texts, "No ExpLabel found — test setup broken"

    save_file = str(tmp_path / "test.png")
    save_variations(fig, save_file, text_list=[""], exp="ATLAS")
    plt.close(fig)

    # After save_variations runs, ExpLabel objects should have been set to "ATLAS"
    # and ExpText objects should have been set to the suffix text (empty string here)
    exp_label_texts = [
        t.get_text() for t in ax.get_children() if isinstance(t, ExpLabel)
    ]
    suffix_texts = [t.get_text() for t in ax.get_children() if isinstance(t, ExpText)]
    assert all(t == "ATLAS" for t in exp_label_texts), (
        f"ExpLabel texts should be 'ATLAS', got {exp_label_texts}"
    )
    assert all(t == "" for t in suffix_texts), (
        f"ExpText suffix texts should be '', got {suffix_texts}"
    )
