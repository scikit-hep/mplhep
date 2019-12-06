import os
import sys
import papermill as pm
import pytest

os.environ["RUNNING_PYTEST"] = "true"


@pytest.fixture()
def common_kwargs(tmpdir):
    outputnb = tmpdir.join('output.ipynb')
    return {
        'output_path': str(outputnb),
        'kernel_name': 'python{}'.format(sys.version_info.major),
    }


def test_examples(common_kwargs):
    pm.execute_notebook('Examples.ipynb', **common_kwargs)
