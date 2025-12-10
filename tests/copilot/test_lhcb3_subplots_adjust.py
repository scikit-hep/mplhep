"""
Test that LHCb3 style works with plt.subplots_adjust(hspace=0).

This test ensures that the LHCb3 style does not have figure.autolayout
enabled, which would conflict with manual layout adjustments.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

plt.switch_backend("Agg")


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
@pytest.mark.mpl_image_compare(style="default", remove_text=False)
def test_lhcb3_with_hspace_zero():
    """Test that LHCb3 style works with subplots_adjust(hspace=0)."""
    mh.style.use("LHCb3")
    fig, axs = plt.subplots(2, 2)
    plt.subplots_adjust(hspace=0)
    return fig


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_lhcb3_no_autolayout():
    """Test that LHCb3 does not have figure.autolayout enabled."""
    mh.style.use("LHCb3")
    assert plt.rcParams["figure.autolayout"] is False


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_lhcb2_has_autolayout():
    """Test that LHCb2 has figure.autolayout enabled (for backward compatibility)."""
    mh.style.use("LHCb2")
    assert plt.rcParams["figure.autolayout"] is True


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_lhcb_alias_uses_lhcb3():
    """Test that LHCb alias points to LHCb3 (without autolayout)."""
    mh.style.use("LHCb")
    assert plt.rcParams["figure.autolayout"] is False
