from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

"""
To test run:
pytest --mpl

When adding new tests, run:
pytest --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


def _draw_text_boundary_lines(txt_obj, ax=None, color="gray", alpha=0.5):
    # Get text bounding box in axes coordinates
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
    for loc in [
        "upper left",
        "upper right",
        "lower left",
        "lower right",
        "over left",
        "over right",
    ]:
        mh.add_text("XYZ", ax=ax, loc=loc)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_add_text_placement_asym():
    fig, ax = plt.subplots(figsize=(15, 5))
    for loc in [
        "upper left",
        "upper right",
        "lower left",
        "lower right",
        "over left",
        "over right",
    ]:
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

    # Create reference texts with different horizontal alignments
    t1 = mh.add_text(
        "XyzZ1",
        ax=ax,
        x=0.25,
        y=0.7,
        ha="center",
        fontsize="xx-large",
        fontname=fontname,
    )
    t2 = mh.add_text(
        "XyzZ2",
        ax=ax,
        x=0.75,
        y=0.7,
        ha="center",
        fontsize="xx-large",
        fontname=fontname,
    )
    t3 = mh.add_text(
        "1XyZ2",
        ax=ax,
        x=0.25,
        y=0.3,
        ha="center",
        fontsize="xx-large",
        fontname=fontname,
    )
    t4 = mh.add_text(
        "1XyZ1",
        ax=ax,
        x=0.75,
        y=0.3,
        ha="center",
        fontsize="xx-large",
        fontname=fontname,
    )

    # Draw boundary lines for reference texts
    _draw_text_boundary_lines(t1, color="red", alpha=0.3)
    _draw_text_boundary_lines(t2, color="blue", alpha=0.3)
    _draw_text_boundary_lines(t3, color="red", alpha=0.3)
    _draw_text_boundary_lines(t4, color="blue", alpha=0.3)

    # Test all append positions
    colors = ["red", "blue", "green", "orange"]
    for i, app_pos in enumerate(["right", "left", "below", "above"]):
        mh.append_text(
            f"1-{app_pos}",
            t1,
            loc=app_pos,
            ax=ax,
            fontsize="xx-large",
            color=colors[i],
            fontname=fontname,
        )
        mh.append_text(
            f"2-{app_pos}",
            t2,
            loc=app_pos,
            ax=ax,
            fontsize="small",
            color=colors[i],
            fontname=fontname,
        )
        mh.append_text(
            f"2-{app_pos}",
            t3,
            loc=app_pos,
            ax=ax,
            fontsize="xx-large",
            color=colors[i],
            fontname=fontname,
        )
        mh.append_text(
            f"1-{app_pos}",
            t4,
            loc=app_pos,
            ax=ax,
            fontsize="small",
            color=colors[i],
            fontname=fontname,
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(f"Test append_text - {fontname}")
    return fig


@pytest.mark.parametrize("fontsize", ["large", "x-small"])
@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_append_text_alignment(fontsize):
    fig, ax = plt.subplots()

    # Create reference texts with different horizontal alignments
    _ref_fs = "large"
    t1 = mh.add_text(
        "yha-left",
        ax=ax,
        x=0.15,
        y=0.7,
        ha="left",
        va="bottom",
        fontsize=_ref_fs,
    )
    t2 = mh.add_text(
        "yha-center",
        ax=ax,
        x=0.5,
        y=0.7,
        ha="center",
        va="bottom",
        fontsize=_ref_fs,
    )
    t3 = mh.add_text(
        "yha-right",
        ax=ax,
        x=0.85,
        y=0.7,
        ha="right",
        va="bottom",
        fontsize=_ref_fs,
    )
    t4 = mh.add_text(
        "yva-top",
        ax=ax,
        x=0.15,
        y=0.3,
        ha="center",
        va="top",
        fontsize=_ref_fs,
    )
    t5 = mh.add_text(
        "yva-base",
        ax=ax,
        x=0.5,
        y=0.3,
        ha="center",
        va="baseline",
        fontsize=_ref_fs,
    )
    t6 = mh.add_text(
        "yva-bot",
        ax=ax,
        x=0.85,
        y=0.3,
        ha="center",
        va="bottom",
        fontsize=_ref_fs,
    )

    # Draw lines to visualize the text boundaries

    # Draw boundary lines for reference texts
    for t in [t1, t2, t3]:
        _draw_text_boundary_lines(t, color="gray", alpha=0.25)
    for t in [t4, t5, t6]:
        _draw_text_boundary_lines(t, color="gray", alpha=0.25)

    # Test all append positions
    colors = ["red", "blue", "green", "orange"]
    for t in [t1, t2, t3]:
        for i, app_pos in enumerate(["right", "left", "below", "above"]):
            mh.append_text(
                f"1-{app_pos}",
                t,
                loc=app_pos,
                ax=ax,
                fontsize=fontsize,
                color=colors[i],
            )
    for t in [t4, t5, t6]:
        for i, app_pos in enumerate(["right", "left", "below", "above"]):
            mh.append_text(
                f"2-{app_pos}",
                t,
                loc=app_pos,
                ax=ax,
                fontsize=fontsize,
                color=colors[i],
            )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
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
    colors = ["red", "blue", "green", "orange"]

    for i, direction in enumerate(["right", "left", "below", "above"]):
        mh.append_text(
            multiline_text,
            ref_text,
            loc=direction,
            ax=ax,
            fontsize="medium",
            color=colors[i],
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Test append_text with multiline text")
    return fig
