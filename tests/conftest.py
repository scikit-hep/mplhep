import matplotlib.pyplot as plt
import pytest


def pytest_configure(config):
    """Configure pytest to handle pytest-xdist + pytest-asyncio compatibility."""
    # Disable pytest-asyncio when running with pytest-xdist to avoid warnings
    # This is the recommended fix from pytest-xdist documentation
    if hasattr(config.option, "numprocesses") and config.option.numprocesses:
        # Running with xdist, disable pytest-asyncio
        config.pluginmanager.set_blocked("pytest_asyncio")


@pytest.fixture(autouse=True)
def clear_mplhep_rcparams():
    """Clear matplotlib rcParams before and after each test."""

    plt.rcParams.update(plt.rcParamsDefault)
    yield
    plt.rcParams.update(plt.rcParamsDefault)
