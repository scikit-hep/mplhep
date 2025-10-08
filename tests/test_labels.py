from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pytest

os.environ["RUNNING_PYTEST"] = "true"

import mplhep as mh

"""
To test run:
pytest --mpl

When adding new tests, run:
pytest --mpl-generate-path=tests/baseline
"""

plt.switch_backend("Agg")


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_add_text_placement():
    fig, ax = plt.subplots(figsize=(5, 5))
    for loc in [
        "upper left",
        "upper right",
        "lower left",
        "lower right",
        "over left",
        "over right",
    ]:
        mh.add_text("XYZ", ax=ax, loc=loc)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_add_text_placement_asym():
    fig, ax = plt.subplots(figsize=(15, 5))
    for loc in [
        "upper left",
        "upper right",
        "lower left",
        "lower right",
        "over left",
        "over right",
    ]:
        mh.add_text("XYZ", ax=ax, loc=loc)
    return fig


@pytest.mark.mpl_image_compare(style="default", remove_text=True)
def test_add_text_placement_any():
    fig, ax = plt.subplots(figsize=(15, 5))
    mh.add_text("XYZ", ax=ax, loc="upper left", pad=10)
    mh.add_text("XYZ", ax=ax, loc="upper right", xpad=5, ypad=20)
    mh.add_text("XYZ", ax=ax, x=0.5, y=0.5, ha="center", va="center")
    return fig
