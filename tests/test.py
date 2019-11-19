import pytest
import matplotlib.pyplot as plt
# import numpy as np

import mplhep as hep


@pytest.mark.mpl_image_compare(style='default', remove_text=True)
def test_basic():
    fig, ax = plt.subplots()
    h = [1, 3, 2]
    bins = [0, 1, 2, 3]
    hep.histplot(h, bins, yerr=True, label='X')
    ax.legend()
    return fig
