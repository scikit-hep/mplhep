import shutil
import subprocess

import matplotlib.pyplot as plt
import pytest


def _has_latex():
    """Check if LaTeX is available on the system."""
    if not shutil.which("latex"):
        return False
    try:
        subprocess.run(
            ["latex", "--version"],
            check=True,
            capture_output=True,
            timeout=5,
        )
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ):
        return False
    return True


def pytest_collection_modifyitems(config, items):  # noqa: ARG001
    """Skip LaTeX tests if LaTeX is not installed."""
    if _has_latex():
        return

    skip_latex = pytest.mark.skip(reason="LaTeX not installed")
    for item in items:
        if "latex" in item.keywords:
            item.add_marker(skip_latex)


@pytest.fixture(autouse=True)
def clear_mplhep_rcparams():
    """Clear matplotlib rcParams before and after each test."""

    plt.rcParams.update(plt.rcParamsDefault)
    yield
    plt.rcParams.update(plt.rcParamsDefault)
