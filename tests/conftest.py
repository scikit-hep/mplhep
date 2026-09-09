import os
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


def _alias_private_nodeid(items):
    """Expose ``item.nodeid`` under the old private name ``item._nodeid``.

    pytest-benchmark 5.3.0 reads ``node._nodeid``, which pytest main replaced
    with a structured id (pytest-dev/pytest#14758, unreleased as of 9.2.0.dev),
    so the ``benchmark`` fixture errors at setup there. Drop this once
    pytest-benchmark reads the public ``node.nodeid``.
    """
    for item in items:
        if not hasattr(item, "_nodeid"):
            item._nodeid = item.nodeid


def pytest_collection_modifyitems(config, items):  # noqa: ARG001
    """Skip LaTeX tests if LaTeX is not installed.

    Set MPLHEP_REQUIRE_LATEX to fail instead. CI LaTeX sets it so that a broken
    texlive install cannot produce a green run by skipping the whole suite.
    """
    _alias_private_nodeid(items)

    if _has_latex():
        return

    if os.environ.get("MPLHEP_REQUIRE_LATEX"):
        msg = "MPLHEP_REQUIRE_LATEX is set but no working `latex` was found on PATH."
        raise pytest.UsageError(msg)

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
