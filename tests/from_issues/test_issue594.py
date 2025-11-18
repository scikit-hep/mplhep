import hist
import numpy as np
import pytest

import mplhep as hep


@pytest.mark.mpl_image_compare(remove_text=False)
def test_issue_594():
    np.random.seed(42)  # Set seed for reproducible results
    h1 = hist.Hist(hist.axis.Regular(10, 0, 10, underflow=True, overflow=True))
    h1.fill(np.random.normal(5, 2, 1000))
    h2 = hist.Hist(hist.axis.Regular(10, 0, 10, underflow=True, overflow=True))
    h2.fill(np.random.normal(5, 2, 1000))

    fig, ax, rax = hep.comparison_plotters.data_model(
        h1, unstacked_components=[h2], flow="show"
    )
    return fig
