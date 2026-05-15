import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.offsetbox import AnchoredText
from matplotlib.transforms import Bbox

import mplhep as mh
from mplhep._utils import _calculate_optimal_scaling, _overlap

plt.switch_backend("Agg")


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_yscale_legend():
    """Test yscale_legend function for automatic legend scaling."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create data that will result in a legend that overlaps with plot
    x = np.linspace(0, 10, 50)
    y1 = np.sin(x) + 10
    y2 = np.cos(x) + 10
    y3 = np.sin(x + np.pi / 4) + 10

    ax.plot(x, y1, label="Signal 1")
    ax.plot(x, y2, label="Signal 2")
    ax.plot(x, y3, label="Background")

    # Set y limits to force legend overlap
    ax.set_ylim(8, 12)
    ax.legend(loc="upper right")

    # Apply yscale_legend to automatically scale
    mh.yscale_legend(ax)

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_yscale_legend_comprehensive():
    """Comprehensive test of yscale_legend with different plot types."""
    np.random.seed(42)

    pairs = [
        ("hist", "line"),
        ("stairs", "stairs2"),
        ("scatter", "scatter2"),
        ("fill_between", None),
    ]

    fig, axes = plt.subplots(4, 4, figsize=(24, 12))

    def plot_data(ax, ptype, x, x2, y):
        if ptype == "hist":
            ax.hist(x, bins=30, alpha=0.5, label="Hist1")
            ax.hist(x + 0.5, bins=30, alpha=0.5, label="Hist2")
        elif ptype == "line":
            ax.plot(np.sort(x), np.linspace(-2, 2, len(x)), alpha=0.5, label="Line1")
            ax.plot(
                np.sort(x) + 0.5, np.linspace(-2, 2, len(x)), alpha=0.5, label="Line2"
            )
        elif ptype == "stairs":
            ax.stairs(
                np.histogram(x, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs1",
            )
            ax.stairs(
                np.histogram(x + 0.5, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs2",
            )
        elif ptype == "stairs2":
            ax.stairs(
                np.histogram(x2, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs1",
            )
            ax.stairs(
                np.histogram(x2, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs2",
            )
        elif ptype == "scatter":
            ax.scatter(x[:50], y[:50], alpha=0.5, label="Scatter1")
            ax.scatter(x[50:100], y[50:100], alpha=0.5, label="Scatter2")
        elif ptype == "scatter2":
            ax.scatter([0.8], [0.1], alpha=0.5, label="Scatter1")
            ax.scatter([0.2] * 50, y[50:100], alpha=0.5, label="Scatter2")
        elif ptype == "fill_between":
            ax.fill_between(
                np.linspace(-2, 2, 100),
                1.5 * np.sin(np.linspace(-2, 2, 100)),
                alpha=0.5,
                label="Fill1",
            )
            ax.fill_between(
                np.linspace(-2, 2, 100),
                1.5 * np.cos(np.linspace(-2, 2, 100)),
                alpha=0.5,
                label="Fill2",
            )

    for row, (ptype1, ptype2) in enumerate(pairs):
        x = np.random.uniform(0, 1, 1000)
        x2 = np.random.normal(0, 1, 1000)
        y = np.random.uniform(0, 1, 1000)

        for col_offset, ptype in enumerate([ptype1, ptype2]):
            ax_ref = axes[row, col_offset * 2]
            ax_scaled = axes[row, col_offset * 2 + 1]
            ax_ref.set_xticks([])
            ax_ref.set_yticks([])
            ax_scaled.set_xticks([])
            ax_scaled.set_yticks([])

            if ptype is None:
                continue
            plot_data(ax_ref, ptype, x, x2, y)
            ax_ref.legend(
                title=f"Ref: {ptype.capitalize()}", loc="upper right", fontsize="small"
            )

            plot_data(ax_scaled, ptype, x, x2, y)
            ax_scaled.legend(
                title=f"Scale: {ptype.capitalize()}",
                loc="upper right",
                fontsize="small",
            )

            # Apply scaling to the scaled axes
            mh.yscale_legend(ax_scaled, soft_fail=True)

    plt.subplots_adjust(hspace=0, wspace=0)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_yscale_anchored_text():
    """Test yscale_anchored_text function for automatic anchored text scaling."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create data that will result in anchored text that overlaps with plot
    x = np.linspace(0, 10, 50)
    y1 = np.sin(x) + 10
    y2 = np.cos(x) + 10
    y3 = np.sin(x + np.pi / 4) + 10

    ax.plot(x, y1, label="Signal 1")
    ax.plot(x, y2, label="Signal 2")
    ax.plot(x, y3, label="Background")

    # Set y limits to force text overlap
    ax.set_ylim(8, 12)

    # Add anchored text that will overlap
    anchored_text = AnchoredText(
        "Important\nInformation", loc="upper right", prop={"size": 12}
    )
    ax.add_artist(anchored_text)

    # Apply yscale_anchored_text to automatically scale
    mh.yscale_anchored_text(ax)

    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_yscale_anchored_text_comprehensive():
    """Comprehensive test of yscale_anchored_text with different plot types."""
    np.random.seed(42)

    pairs = [
        ("hist", "line"),
        ("stairs", "stairs2"),
        ("scatter", "scatter2"),
        ("fill_between", None),
    ]

    fig, axes = plt.subplots(4, 4, figsize=(24, 12))

    def plot_data(ax, ptype, x, x2, y):
        if ptype == "hist":
            ax.hist(x, bins=30, alpha=0.5, label="Hist1")
            ax.hist(x + 0.5, bins=30, alpha=0.5, label="Hist2")
        elif ptype == "line":
            ax.plot(np.sort(x), np.linspace(-2, 2, len(x)), alpha=0.5, label="Line1")
            ax.plot(
                np.sort(x) + 0.5, np.linspace(-2, 2, len(x)), alpha=0.5, label="Line2"
            )
        elif ptype == "stairs":
            ax.stairs(
                np.histogram(x, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs1",
            )
            ax.stairs(
                np.histogram(x + 0.5, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs2",
            )
        elif ptype == "stairs2":
            ax.stairs(
                np.histogram(x2, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs1",
            )
            ax.stairs(
                np.histogram(x2, bins=20)[0],
                np.linspace(-2, 2, 21),
                alpha=0.5,
                label="Stairs2",
            )
        elif ptype == "scatter":
            ax.scatter(x[:50], y[:50], alpha=0.5, label="Scatter1")
            ax.scatter(x[50:100], y[50:100], alpha=0.5, label="Scatter2")
        elif ptype == "scatter2":
            ax.scatter([0.8], [0.1], alpha=0.5, label="Scatter1")
            ax.scatter([0.2] * 50, y[50:100], alpha=0.5, label="Scatter2")
        elif ptype == "fill_between":
            ax.fill_between(
                np.linspace(-2, 2, 100),
                1.5 * np.sin(np.linspace(-2, 2, 100)),
                alpha=0.5,
                label="Fill1",
            )
            ax.fill_between(
                np.linspace(-2, 2, 100),
                1.5 * np.cos(np.linspace(-2, 2, 100)),
                alpha=0.5,
                label="Fill2",
            )

    for row, (ptype1, ptype2) in enumerate(pairs):
        x = np.random.uniform(0, 1, 1000)
        x2 = np.random.normal(0, 1, 1000)
        y = np.random.uniform(0, 1, 1000)

        for col_offset, ptype in enumerate([ptype1, ptype2]):
            ax_ref = axes[row, col_offset * 2]
            ax_scaled = axes[row, col_offset * 2 + 1]
            ax_ref.set_xticks([])
            ax_ref.set_yticks([])
            ax_scaled.set_xticks([])
            ax_scaled.set_yticks([])

            if ptype is None:
                continue
            plot_data(ax_ref, ptype, x, x2, y)

            # Add anchored text to reference axes
            anchored_text_ref = AnchoredText(
                f"Ref: {ptype.capitalize()}", loc="upper right", prop={"size": 10}
            )
            ax_ref.add_artist(anchored_text_ref)

            plot_data(ax_scaled, ptype, x, x2, y)

            # Add anchored text to scaled axes
            anchored_text_scaled = AnchoredText(
                f"Scale: {ptype.capitalize()}", loc="upper right", prop={"size": 10}
            )
            ax_scaled.add_artist(anchored_text_scaled)

            # Apply scaling to the scaled axes
            mh.yscale_anchored_text(ax_scaled, soft_fail=True)

    plt.subplots_adjust(hspace=0, wspace=0)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_yscale_mpl_magic_add_text():
    """Test mpl_magic function with both AnchoredText and add_text for automatic scaling."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 2, figsize=(10, 10))
    fig.subplots_adjust(hspace=0)
    # Create data that will result in text that overlaps with plot
    x = np.linspace(0, 8, 50)
    y1 = np.sin(x)
    y2 = np.cos(x) * 2
    y3 = np.sin(x + np.pi / 4) * 3

    for axs in [ax1, ax2, ax3]:
        for ax in axs:
            ax.plot(x, y1, label="Signal 1")
            ax.plot(x, y2, label="Signal 2")
            ax.plot(x, y3, label="Background")

    # Add AnchoredText that will overlap
    for ax in ax1:
        anchored_text = AnchoredText(
            "AnchoredText\nImportant Information", loc="upper right", prop={"size": 12}
        )
        ax.add_artist(anchored_text)
    # Add text using mplhep's add_text function that will overlap
    for ax in ax2:
        mh.add_text("add_text\nImportant Information", loc="upper right", ax=ax)
    # Add legend
    for ax in ax3:
        ax.legend(loc="upper right", fontsize="small")

    # Apply mpl_magic to automatically scale
    for _, axr in [ax1, ax2, ax3]:
        mh.mpl_magic(axr, soft_fail=True)

    return fig


def _make_sci_overlap_axes(style):
    """Build axes that exhibit the xlabel/sci-notation overlap from issue #712."""
    plt.style.use(style)
    fig, ax = plt.subplots()
    np.random.seed(0)
    ax.plot(np.linspace(0, 5e6, 100), np.random.normal(0, 1, 100))
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax.set_xlabel("Energy [GeV]")
    ax.set_ylabel("Events")
    return fig, ax


@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_xlabel_sci_adjust_visual():
    """Visual baseline for the issue-#712 fix: x-label should not overlap the
    matplotlib-supplied ``x10^n`` offset text after ``xlabel_sci_adjust``.
    """
    fig, ax = _make_sci_overlap_axes(mh.style.ATLAS)
    mh.atlas.label(loc=1)
    mh.xlabel_sci_adjust(ax)
    return fig


def _xlabel_offset_overlap(ax):
    """Return True iff the x-label bbox overlaps the offset-text bbox."""
    fig = ax.figure
    fig.canvas.draw()
    canvas = fig.canvas
    renderer = (
        canvas.get_renderer()
        if hasattr(canvas, "get_renderer")
        else fig._get_renderer()
    )
    xaxis = ax.get_xaxis()
    offset = xaxis.offsetText.get_window_extent(renderer)
    label = xaxis.label.get_window_extent(renderer)
    horiz = label.x1 > offset.x0 and offset.x1 > label.x0
    vert = label.y1 > offset.y0 and offset.y1 > label.y0
    return horiz and vert


@pytest.mark.parametrize("style", ["ATLAS", "ATLASAlt", "CMS", "ALICE", "LHCb2"])
def test_xlabel_sci_adjust_resolves_overlap(style):
    """The fix must turn an overlapping (xlabel vs ``x10^n``) layout into a
    non-overlapping one, across the styles where the overlap typically occurs.
    """
    style_obj = getattr(mh.style, style)
    fig, ax = _make_sci_overlap_axes(style_obj)
    assert _xlabel_offset_overlap(ax), (
        f"Expected pre-fix overlap on style={style}; the test scenario no "
        f"longer reproduces and needs updating."
    )
    mh.xlabel_sci_adjust(ax)
    assert not _xlabel_offset_overlap(ax), (
        f"xlabel_sci_adjust did not clear the overlap on style={style}."
    )
    plt.close(fig)


def test_xlabel_sci_adjust_is_idempotent():
    """Repeated invocations must not keep shifting the label further left."""
    fig, ax = _make_sci_overlap_axes(mh.style.ATLAS)
    mh.xlabel_sci_adjust(ax)
    x_after_first = ax.xaxis.label.get_position()[0]
    mh.xlabel_sci_adjust(ax)
    mh.xlabel_sci_adjust(ax)
    assert ax.xaxis.label.get_position()[0] == x_after_first, (
        "Calling xlabel_sci_adjust again after the first run should be a no-op."
    )
    plt.close(fig)


def test_xlabel_sci_adjust_skips_when_no_offset():
    """No sci-notation offset = no label-position change."""
    plt.style.use(mh.style.ATLAS)
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4])
    ax.set_xlabel("x")
    original_x = ax.xaxis.label.get_position()[0]
    mh.xlabel_sci_adjust(ax)
    assert ax.xaxis.label.get_position()[0] == original_x
    plt.close(fig)


def test_xlabel_sci_adjust_skips_when_no_xlabel():
    """No x-label = nothing to shift."""
    plt.style.use(mh.style.ATLAS)
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, 5e6, 10), np.linspace(0, 1, 10))
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    original_x = ax.xaxis.label.get_position()[0]
    mh.xlabel_sci_adjust(ax)
    assert ax.xaxis.label.get_position()[0] == original_x
    plt.close(fig)


def test_overlap_per_bbox_flags_multi_bbox():
    """Regression test for #699: when several bboxes are passed but only a
    subset actually overlap data, ``_overlap(return_per_bbox=True)`` must
    flag exactly the contributing ones.

    Without this, ``_calculate_optimal_scaling`` would have to redo the
    contained/occluding check itself against *all* vertices, which was both
    slow and used a filter criterion that could disagree with the count.
    """
    fig, ax = plt.subplots()
    # Diagonal line through the axes.
    ax.plot([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    fig.canvas.draw()

    def disp_bbox(x0, y0, x1, y1):
        (dx0, dy0), (dx1, dy1) = ax.transData.transform([[x0, y0], [x1, y1]])
        return Bbox.from_extents(dx0, dy0, dx1, dy1)

    # bbox A: contains the line at (1.5, 1.5) -> hit.
    bbox_a = disp_bbox(1.0, 1.0, 2.0, 2.0)
    # bbox B: in the top-left corner, ABOVE every line vertex in its x-range
    #         -> not contained, not occluded -> no hit.
    bbox_b = disp_bbox(0.1, 4.5, 0.3, 4.9)
    # bbox C: below the line in column x in [3, 4] -> occluded -> hit.
    bbox_c = disp_bbox(3.0, 0.0, 4.0, 1.0)

    count, _verts, flags = _overlap(ax, [bbox_a, bbox_b, bbox_c], return_per_bbox=True)

    assert count > 0
    assert flags == [True, False, True], (
        f"per-bbox flags should isolate the actually-overlapping bboxes, got {flags}"
    )
    plt.close(fig)


def test_overlap_per_bbox_bbox_bbox():
    """A bbox that doesn't intersect any plot vertex but DOES overlap another
    text bbox on the axes must still be flagged. This is the path that
    earlier filters could drop because they only looked at vertex overlap.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    txt = ax.text(2.5, 2.5, "hello")
    fig.canvas.draw()
    text_bbox = txt.get_window_extent()

    # Overlapping shift in display coords -- guaranteed not to touch any line.
    overlap_bbox = Bbox.from_extents(
        text_bbox.x0 + 1,
        text_bbox.y0 + 1,
        text_bbox.x1 + 1,
        text_bbox.y1 + 1,
    )
    count, _verts, flags = _overlap(ax, [overlap_bbox], return_per_bbox=True)
    assert count > 0
    assert flags == [True]
    plt.close(fig)


def test_calculate_optimal_scaling_with_subset_overlap():
    """End-to-end regression for #699: when only some bboxes overlap data,
    ``_calculate_optimal_scaling`` must compute the scaling from those bboxes
    only -- not let a far-from-overlap bbox influence (or null out) the
    answer because all bboxes get fed in together.
    """
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    fig.canvas.draw()

    def disp_bbox(x0, y0, x1, y1):
        (dx0, dy0), (dx1, dy1) = ax.transData.transform([[x0, y0], [x1, y1]])
        return Bbox.from_extents(dx0, dy0, dx1, dy1)

    overlapping = disp_bbox(0.5, 0.5, 2.0, 2.0)  # contains line vertices
    free = disp_bbox(0.1, 4.5, 0.3, 4.9)  # top-left, above any line vertex

    scale = _calculate_optimal_scaling(ax, [overlapping, free])
    assert scale > 1.0, (
        f"expected scale > 1 because `overlapping` covers plot data; got {scale}"
    )

    # Sanity: with only the non-overlapping bbox, no scaling is needed.
    assert _calculate_optimal_scaling(ax, [free]) == 1.0
    plt.close(fig)
