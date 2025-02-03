from __future__ import annotations

import os
import sys

# import papermill as pm
import pytest

os.environ["RUNNING_PYTEST"] = "true"


@pytest.fixture
def common_kwargs(tmpdir):
    outputnb = tmpdir.join("output.ipynb")
    return {
        "output_path": str(outputnb),
        "kernel_name": f"python{sys.version_info.major}",
    }


# def test_examples(common_kwargs):
#     pm.execute_notebook("examples/Examples.ipynb", **common_kwargs)
