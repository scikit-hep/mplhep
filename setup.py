from setuptools import setup

extras_require = {
    "test": [
        "pytest",
        "pytest-mpl",
        "papermill~=1.0",
        "nteract-scrapbook~=0.3",
        "uproot",
        "uproot4",
        "boost_histogram",
        "scikit-hep-testdata",
    ],
    "develop": ["flake8", "jupyter", "bumpversion", "twine", "black", "pre-commit"],
}
extras_require["complete"] = sorted(set(sum(extras_require.values(), [])))


setup(
    extras_require=extras_require,
)

# To push on pypi
# python setup.py sdist
# twine upload dist/*
