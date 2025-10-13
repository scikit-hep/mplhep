import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.offsetbox import AnchoredText

import mplhep as mh

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
