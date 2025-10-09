# Installation# Contributing



mplhep is a Python package for creating publication-quality plots in high-energy physics. This page covers installation and basic setup.We welcome contributions to mplhep! This guide will help you get started with contributing to the project.



## Quick Start## Getting Started



If you're already familiar with Python environments, you can install mplhep with:### Fork and Clone



```bash1. Fork the [mplhep repository](https://github.com/scikit-hep/mplhep) on GitHub

pip install mplhep2. Clone your fork locally:

``````bash

git clone https://github.com/YOUR_USERNAME/mplhep.git

Then create your first plot:cd mplhep

```

```python

import numpy as np### Development Installation

import matplotlib.pyplot as plt

import mplhep as mhInstall mplhep in development mode with all dependencies:



# Generate sample data```bash

h, bins = np.histogram(np.random.random(1000))python -m pip install --upgrade --editable ".[all]"

```

# Create plot

fig, ax = plt.subplots()Or use the convenient install script:

mh.histplot(h, bins)```bash

mh.cms.label()  # Add CMS labelbash install.sh

plt.show()```

```

## Development Workflow

## Prerequisites

### Setting up Pre-commit Hooks

mplhep requires:

Install and set up pre-commit hooks to ensure code quality:

- Python 3.8 or newer

- matplotlib```bash

- numpypip install pre-commit

- packagingpre-commit install

```

!!! note

    Python 2.7 support was dropped with mplhep v0.3.0. All major scientific Python packages have ended Python 2 support.### Running Tests



## Installation MethodsRun the fast unit tests:

```bash

### PyPI (Recommended)pytest --mpl --ignore=tests/test_notebooks.py

```

Install from the Python Package Index:

Run the complete test suite (including slower notebook tests):

```bash```bash

# System-wide installationpython -m pytest -r sa --mpl --mpl-results-path=pytest_results -n 4

pip install mplhep```



# User installation (if no admin rights)### Making Changes

pip install --user mplhep

1. Create a feature branch:

# Upgrade existing installation```bash

pip install --upgrade mplhepgit checkout -b feature/your-feature-name

``````



### Conda2. Make your changes and test them



If you use conda environments:3. Commit using [Conventional Commits](https://www.conventionalcommits.org/):

```bash

```bashgit commit -m "feat: add new plotting function"

# Activate your environment```

conda activate myenv

4. Push to your fork:

# Install mplhep```bash

pip install mplhepgit push origin feature/your-feature-name

``````



### Development Installation5. Create a Pull Request on GitHub



For contributors or development:## Pull Request Guidelines



```bash### Before Submitting

# Clone the repository

git clone https://github.com/scikit-hep/mplhep.git- Ensure all tests pass

cd mplhep- Update documentation if needed

- Add tests for new features

# Install in development mode- Follow the existing code style

pip install -e .

```### Visual Test Baselines



## Platform SupportIf your changes affect visual output, generate new baseline images:



mplhep is tested on:```bash

python -m pytest -r sa --mpl -n 4 --mpl-generate-path=tests/baseline

- Linux (Ubuntu, CentOS, etc.)```

- macOS

- Windows!!! warning

    Only include actually modified baseline images in your PR. Some images may look identical but differ bit-wise.

All functional features are routinely tested across supported Python versions.

## Reporting Issues

## Virtual Environments

For bug reports or feature requests, please [open an issue](https://github.com/scikit-hep/mplhep/issues) on GitHub.

Using virtual environments is recommended:

## Development Dependencies

```bash

# Create virtual environmentThe `[all]` extra installs:

python -m venv mplhep_env- Testing dependencies (pytest, pytest-mpl)

- Documentation dependencies (mkdocs, mkdocstrings)

# Activate environment- Development tools (pre-commit, ruff)

source mplhep_env/bin/activate  # Linux/macOS- All optional dependencies

# or

mplhep_env\Scripts\activate     # Windows## Code Quality



# Install mplhepWe use:

pip install mplhep- **ruff** for linting and formatting

```- **mypy** for type checking

- **pre-commit** for automated quality checks

## Testing Installation- **pytest-mpl** for visual regression testing



Verify your installation:## Getting Help



```python- Check existing [issues](https://github.com/scikit-hep/mplhep/issues) and [discussions](https://github.com/scikit-hep/mplhep/discussions)

import mplhep- Ask questions in the scikit-hep community

print(f"mplhep version: {mplhep.__version__}")- Review the [API documentation](api.md) for implementation details


# Test basic functionality
import matplotlib.pyplot as plt
import numpy as np

plt.style.use(mplhep.style.CMS)
h, bins = np.histogram(np.random.normal(0, 1, 100))
fig, ax = plt.subplots()
mplhep.histplot(h, bins)
print("Installation successful!")
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'mplhep'**
- Ensure mplhep is installed in the correct Python environment
- Check that you're using the right Python interpreter

**Style not found**
- Verify matplotlib version compatibility
- Try updating matplotlib: `pip install --upgrade matplotlib`

**Font issues**
- Some experiment styles require specific fonts
- Install additional fonts if needed

### Getting Help

- Check the [GitHub repository](https://github.com/scikit-hep/mplhep) for issues
- Ask questions in the [scikit-hep discussions](https://github.com/scikit-hep/mplhep/discussions)

## Next Steps

Now that mplhep is installed:

1. Read the [Getting Started](guide.md) guide
2. Explore the [Gallery](gallery/index.md) for examples
3. Check the [API Reference](api.md) for detailed documentation
