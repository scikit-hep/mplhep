from __future__ import annotations

import runpy
import sys
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.figure
import matplotlib.pyplot as plt
import pytest


def with_benchmark(func):
    """
    Decorator that automatically creates a benchmark version of a test function.

    Usage:
        @with_benchmark
        @pytest.mark.mpl_image_compare(style="default", remove_text=True)
        def test_simple():
            # your plotting code
            return fig

    This creates both:
    - test_simple() - for image comparison
    - test_simple_benchmark() - for performance benchmarking
    """

    # Create the benchmark version
    @pytest.mark.benchmark
    def benchmark_test(benchmark):
        def run_test():
            fig = func()
            if fig is not None:
                plt.close(fig)  # Clean up figures to prevent memory issues

        benchmark(run_test)

    # Set the benchmark function name and add to the current module
    benchmark_name = func.__name__ + "_benchmark"
    benchmark_test.__name__ = benchmark_name
    benchmark_test.__doc__ = f"Benchmark version of {func.__name__}"

    # Get the module where the decorator is being used
    caller_frame = sys._getframe(1)
    caller_globals = caller_frame.f_globals

    # Add the benchmark test to the caller's globals so pytest can find it
    caller_globals[benchmark_name] = benchmark_test

    # Return the original function unchanged
    return func


def run_script_and_get_object(script_path_str: str, name: str) -> Any | None:
    """
    Runs a Python script from a given file path, temporarily disables saving of matplotlib figures
    to suppress file output, and retrieves a variable from the script's global namespace by name.
    The retrieved variable can be of any type.

    Typically used with name="fig" to get the figure object created in the script.

    Parameters:
        script_path_str (str): Path to the Python script file to execute.
        name (str): Name of the variable in the script's global namespace to retrieve.

    Returns:
        Any or None: The specified variable from the script's global namespace if present;
                     otherwise, None.
    """
    script_path = Path(script_path_str).resolve()

    if not script_path.is_file():
        msg = f"Script file not found: {script_path_str}"
        raise FileNotFoundError(msg)
    original_savefig = mpl.figure.Figure.savefig

    def suppressed_savefig(*args, **kwargs):
        pass

    mpl.figure.Figure.savefig = suppressed_savefig  # type: ignore[method-assign]

    try:
        globals_dict = runpy.run_path(str(script_path))
    finally:
        mpl.figure.Figure.savefig = original_savefig  # type: ignore[method-assign]

    return globals_dict.get(name)
