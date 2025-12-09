import matplotlib.pyplot as plt
import mplhep as hep
import pytest
import warnings

def test_lhcb2_default_is_manual():
    """Verify default LHCb2 does NOT have constrained_layout."""
    hep.style.use("LHCb2")
    # Should be False (Manual Engine)
    assert plt.rcParams.get("figure.autolayout") is False
    assert plt.rcParams.get("figure.constrained_layout.use") is False

def test_lhcb2_variant_is_constrained():
    """Verify LHCb2:constrained ENABLES constrained_layout."""
    hep.style.use("LHCb2:constrained")
    # Should be True (Constrained Engine)
    val = plt.rcParams.get("figure.constrained_layout.use")
    assert val is True

def test_variant_application():
    """Integration Test: Check the gap behavior."""
    # Case 1: Default (Manual) -> Gap should be 0
    hep.style.use("LHCb2")
    fig1, (ax1a, ax1b) = plt.subplots(2, 1, sharex=True)
    plt.subplots_adjust(hspace=0)
    fig1.canvas.draw()
    gap1 = ax1a.get_position().y0 - ax1b.get_position().y1
    plt.close(fig1)
    
    # Case 2: Variant (Constrained) -> Gap should be > 0 (Solver inserts padding)
    hep.style.use("LHCb2:constrained")
    fig2, (ax2a, ax2b) = plt.subplots(2, 1, sharex=True)
    
    # We expect a warning here because we are mixing engines. 
    # We ignore it because we WANT to verify that the solver ignored our command.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.subplots_adjust(hspace=0) 
        
    fig2.canvas.draw()
    gap2 = ax2a.get_position().y0 - ax2b.get_position().y1
    plt.close(fig2)

    assert gap1 < 0.001, "Default style should allow zero gap"
    assert gap2 > 0.001, "Constrained variant should enforce padding (when join_axes is NOT used)"