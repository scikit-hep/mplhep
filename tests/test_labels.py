"""Tests for mplhep label functionality.

To run tests:
    pytest --mpl

When adding new tests:
    pytest --mpl-generate-path=tests/baseline
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pytest

# Set environment before importing mplhep
os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

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
    bbox, _, descent = txt_obj._get_layout(ax.figure.canvas.get_renderer())
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
            zip(texts, font_sizes, labels)
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
