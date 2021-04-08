from __future__ import annotations

from setuptools import setup

extras_require = {
    "test": [
        "scipy>=1.1.0",
        "pytest",
        "pytest-mpl",
        "pytest-mock",
        "papermill~=1.0",
        "nteract-scrapbook~=0.3",
        "uproot",
        "uproot4",
        "boost_histogram",
        "scikit-hep-testdata",
    ],
    "dev": ["flake8", "jupyter", "bumpversion", "twine", "black", "pre-commit"],
}
extras_require["all"] = sorted(set(sum(extras_require.values(), [])))


setup(
    extras_require=extras_require,
)

# To push on pypi
# python setup.py sdist
# twine upload dist/*
