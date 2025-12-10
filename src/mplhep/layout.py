import matplotlib.pyplot as plt

def join_axes(axes, orientation="vertical"):
    """
    Force axes to physically touch (gap = 0), manually overriding any layout engine.
    """
    if not axes:
        return

    ax1, ax2 = axes[:2]
    fig = ax1.get_figure()

    # 1. Hide bottom labels of the upper subplot
    if orientation == "vertical":
        ax1.tick_params(labelbottom=False)

    # 2. Let the layout engine (if any) run first to establish baselines
    fig.canvas.draw()

    # 3. === HARD OVERRIDE (PADDING-KILLER) ===
    # We manually edit bbox positions post-solver to force exact touching.
    pos1 = ax1.get_position()
    pos2 = ax2.get_position()

    if orientation == "vertical":
        # Pin ax2 (bottom) to its current location
        ax2.set_position([pos2.x0, pos2.y0, pos2.width, pos2.height])

        # Pin ax1 (top) so its bottom (y0) touches ax2's top (y0 + height)
        new_y0 = pos2.y0 + pos2.height
        ax1.set_position([pos1.x0, new_y0, pos1.width, pos1.height])

    else:
        # Horizontal case: Pin ax2, move ax1 to touch it
        ax2.set_position([pos2.x0, pos2.y0, pos2.width, pos2.height])
        ax1.set_position([pos2.x0 + pos2.width, pos1.y0, pos1.width, pos1.height])

    # 4. Final draw to render the changes
    fig.canvas.draw()
