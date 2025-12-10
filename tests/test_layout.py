import matplotlib.pyplot as plt

import mplhep as hep
from mplhep.layout import join_axes


def test_join_axes_manual():
    """Test that join_axes works on standard Manual layout."""
    hep.style.use("LHCb2")
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    join_axes([ax1, ax2])
    fig.canvas.draw()
    gap = ax1.get_position().y0 - ax2.get_position().y1
    plt.close(fig)
    assert abs(gap) < 0.001


def test_join_axes_constrained():
    """Test that join_axes works on Constrained layout."""
    hep.style.use("LHCb2:constrained")
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    join_axes([ax1, ax2])
    fig.canvas.draw()
    gap = ax1.get_position().y0 - ax2.get_position().y1
    plt.close(fig)
    assert abs(gap) < 0.001
