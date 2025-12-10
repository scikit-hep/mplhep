"""
Test case that exactly reproduces the original issue.

From the issue: "I want to arrange two axes with no space between."
This test verifies that the fix works for the exact use case described.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep

plt.switch_backend("Agg")


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_original_issue_reproduction():
    """
    Exact reproduction of the original issue code.
    This should now work with LHCb style.
    """
    mplhep.style.use("LHCb")  # Using the default LHCb alias
    fig, axs = plt.subplots(2, 2)
    plt.subplots_adjust(hspace=0)
    return fig
