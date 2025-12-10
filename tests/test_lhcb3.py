import matplotlib.pyplot as plt
import mplhep as hep
import pytest

@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_lhcb3_simple():
    """Test that LHCb3 loads and renders without error."""
    hep.style.use("LHCb3")
    fig, ax = plt.subplots()
    hep.cms.text("LHCb3 Test", loc=0)
    ax.plot([1, 2, 3], [1, 2, 3])
    return fig

def test_lhcb3_no_autolayout():
    """Verify that autolayout is FALSE in LHCb3."""
    hep.style.use("LHCb3")
    # Check rcParams directly
    assert plt.rcParams.get("figure.autolayout") is False