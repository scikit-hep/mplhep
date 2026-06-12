import sys

sys.path.append(".")  # Ensure resize_svg can be imported from the same directory
from io import StringIO

import resize_svg


def save_figure_as_resized_svg(fig, width_percentage=50):
    """
    Save a matplotlib figure as SVG, resize it to a percentage width, and return the result.

    Args:
        fig: The matplotlib Figure object
        width_percentage (float): The desired width as a percentage (default 50)

    Returns:
        str: The resized SVG content
    """
    buffer = StringIO()
    fig.savefig(buffer, format="svg", dpi=300, bbox_inches="tight", pad_inches=0.2)
    return resize_svg.resize_svg_to_percentage(buffer.getvalue(), width_percentage)
