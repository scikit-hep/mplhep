from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import matplotlib.figure


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

    original_savefig = matplotlib.figure.Figure.savefig

    def suppressed_savefig(*args, **kwargs):
        pass

    matplotlib.figure.Figure.savefig = suppressed_savefig  # type: ignore[method-assign]

    try:
        globals_dict = runpy.run_path(str(script_path))
    finally:
        matplotlib.figure.Figure.savefig = original_savefig  # type: ignore[method-assign]

    return globals_dict.get(name)
