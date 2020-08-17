def get_histogram_axes_title(axis):
    # type: (object) -> str

    if hasattr(axis, "label"):
        return axis.label
    # Classic support for older hist, deprecated
    elif hasattr(axis, "title"):
        return axis.title
    elif hasattr(axis, "name"):
        return axis.name

    # No axis title found
    return ""
