from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as hep  # noqa: E402

"""
To test run:
python pytest -r sa --mpl --mpl-results-path=pytest_results

When adding new tests, run:
python pytest -r sa --mpl --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_square_cbar():
    fig, ax = plt.subplots()
    ax = hep.make_square_add_cbar(ax=ax)
    return fig
