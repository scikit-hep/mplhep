import re


def resize_svg_to_percentage(svg_content, width_percentage=50):
    """
    Resize SVG to a percentage of its container width, maintaining aspect ratio.

    Args:
        svg_content (str): The SVG content as a string
        width_percentage (float): The desired width as a percentage (default 50)

    Returns:
        str: The resized SVG content
    """
    width_match = re.search(r'width="([^"]*)"', svg_content)
    height_match = re.search(r'height="([^"]*)"', svg_content)
    if width_match and height_match:
        w_str = width_match.group(1)
        h_str = height_match.group(1)
        # Extract numeric values
        w_val = float(re.match(r"([\d.]+)", w_str).group(1))
        h_val = float(re.match(r"([\d.]+)", h_str).group(1))
        # Calculate aspect ratio
        ratio = h_val / w_val
        # Set width to percentage and height proportionally
        new_w = f"{width_percentage}%"
        new_h = f"{width_percentage * ratio}%"
        svg_content = svg_content.replace(f'width="{w_str}"', f'width="{new_w}"')
        svg_content = svg_content.replace(f'height="{h_str}"', f'height="{new_h}"')
    return svg_content
