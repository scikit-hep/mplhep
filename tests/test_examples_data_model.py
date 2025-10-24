import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

# Add the tests directory to sys.path to find helpers
tests_dir = Path(__file__).parent
if str(tests_dir) not in sys.path:
    sys.path.insert(0, str(tests_dir))

from helpers import run_script_and_get_object

import mplhep

mpl_image_compare_kwargs = {
    "baseline_dir": "baseline",
    "savefig_kwargs": {"bbox_inches": "tight"},
    "style": mplhep.style.plothist,
    "deterministic": True,
}

script_dir = Path(mplhep.__file__).parent / ".." / ".." / "examples" / "model_ex"

current_module = sys.modules[__name__]


@pytest.fixture(autouse=True)
def close_all_figures():
    """Automatically close all figures after each test."""
    yield
    plt.close("all")


for script_path in script_dir.glob("*.py"):
    filename = f"{script_path.stem}.png"
    test_name = f"test_{script_path.stem}"

    def make_test(script_path=script_path):
        @pytest.mark.mpl_image_compare(
            filename=f"{script_path.stem}.png", **mpl_image_compare_kwargs
        )
        def func_test():
            return run_script_and_get_object(script_path, "fig")

        return func_test

    test_func = make_test()
    test_func.__name__ = test_name
    setattr(current_module, test_name, test_func)
