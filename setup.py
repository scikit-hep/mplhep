import os
from setuptools import setup
from setuptools.command.install import install
import sys

INSTALL_REQUIRES = [
    "matplotlib<3" if sys.version_info.major < 3 else "matplotlib>=3.1",
    "numpy>=1.16.0",
    "scipy>=1.1.0",
    "requests~=2.21",
    "packaging",
]

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

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None

with open(os.path.join(base_dir, "mplhep", ".VERSION")) as version_file:
    __version__ = version_file.read().strip()

setup(
    name="mplhep",
    version=__version__,
    author="andrzejnovak",
    author_email="novak5andrzej@gmail.com",
    license="MIT License",
    description="Matplotlib styles for HEP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/andrzejnovak/mplhep/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.5",
    install_requires=INSTALL_REQUIRES,
    extras_require=extras_require,
    packages=["mplhep"],
    include_package_data=True,
)

# To push on pypi
# python setup.py sdist
# twine upload dist/*
