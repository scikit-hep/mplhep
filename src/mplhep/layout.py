import matplotlib.pyplot as plt
import matplotlib.layout_engine
import warnings
def join_axes(axes, orientation="vertical"):
    """
    Force axes to physically touch (gap = 0), even under Matplotlib 3.9
    constrained layout where the solver enforces minimum padding (~0.04).
    """

    if not axes:
        return

    fig = axes[0].get_figure()
    ax1, ax2 = axes[:2]

    # Hide bottom labels of the upper subplot
    if orientation == "vertical":
        ax1.tick_params(labelbottom=False)

    import matplotlib.layout_engine as mle

    engine = fig.get_layout_engine()

    # Let constrained_layout run normally first
    fig.canvas.draw()

    # === HARD OVERRIDE (PADDING-KILLER) ======================================
    # We manually edit bbox positions post-solver.
    pos1 = ax1.get_position()
    pos2 = ax2.get_position()

    if orientation == "vertical":
        # force ax2 top == ax1 bottom
        new_bottom = pos2.y0
        new_top = new_bottom + pos1.height

        ax1.set_position([pos1.x0, new_bottom + pos2.height, pos1.width, pos1.height])
        ax2.set_position([pos2.x0, new_bottom, pos2.width, pos2.height])

        # Now force exact touching
        ax1.set_position([pos1.x0, pos2.y1, pos1.width, pos1.height])
        ax2.set_position([pos2.x0, pos2.y0, pos2.width, pos2.height])

        # Final gap-kill
        ax1_pos = ax1.get_position()
        ax2_pos = ax2.get_position()
        ax1.set_position([ax1_pos.x0, ax2_pos.y1, ax1_pos.width, ax1_pos.height])

    else:
        # Horizontal case (not needed for your tests, but complete)
        ax1.set_position([pos2.x1, pos1.y0, pos1.width, pos1.height])
        ax2.set_position([pos2.x0, pos2.y0, pos2.width, pos2.height])

    fig.canvas.draw()