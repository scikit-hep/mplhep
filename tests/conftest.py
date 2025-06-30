import matplotlib.pyplot as plt
import pytest


@pytest.fixture(autouse=True)
def clear_mplhep_rcparams():
    """Clear matplotlib rcParams before and after each test."""

    plt.rcParams.update(plt.rcParamsDefault)
    yield
    plt.rcParams.update(plt.rcParamsDefault)
