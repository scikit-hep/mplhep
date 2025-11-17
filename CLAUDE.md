# CLAUDE.md - AI Assistant Guide for mplhep

This document provides comprehensive guidance for AI assistants working with the mplhep codebase.

## Project Overview

**mplhep** is a Python library that provides helpers for matplotlib to produce plots typically needed in High Energy Physics (HEP) and style them according to collaboration requirements (ROOT-like plots for CMS, ATLAS, LHCb, ALICE, DUNE).

- **Repository**: https://github.com/scikit-hep/mplhep
- **Documentation**: https://scikit-hep.org/mplhep/
- **Part of**: Scikit-HEP ecosystem
- **License**: MIT
- **Python Support**: 3.9+

## Repository Structure

```
mplhep/
├── src/mplhep/              # Main package source code
│   ├── __init__.py          # Package initialization & exports
│   ├── plot.py              # Core plotting functions (hist, histplot, hist2dplot, funcplot, model)
│   ├── label.py             # Experiment-specific labels
│   ├── utils.py             # Utility functions for plot manipulation
│   ├── _utils.py            # Internal utilities & plottable histogram handling
│   ├── comparison_*.py      # Comparison plotting functions
│   ├── error_estimation.py  # Error estimation utilities
│   ├── comp.py              # Compatibility layer
│   ├── exp_*.py             # Experiment-specific modules (cms, atlas, lhcb, alice, dune)
│   ├── styles/              # Matplotlib style definitions
│   │   ├── __init__.py      # Style loading & set_style function
│   │   ├── atlas.py         # ATLAS experiment style
│   │   ├── cms.py           # CMS experiment style
│   │   ├── lhcb.py          # LHCb experiment style
│   │   ├── alice.py         # ALICE experiment style
│   │   ├── dune.py          # DUNE experiment style
│   │   └── plothist.py      # General histogram plotting style
│   ├── _dev.py              # Developer CLI tool
│   ├── _deprecate.py        # Deprecation utilities
│   ├── _compat.py           # Compatibility utilities
│   └── _tools.py            # Internal tools (Config class)
├── tests/                   # Test suite
│   ├── baseline/            # Reference images for visual regression tests
│   ├── test_basic.py        # Basic functionality tests
│   ├── test_labels.py       # Label functionality tests
│   ├── test_comparison_*.py # Comparison plot tests
│   ├── test_inputs.py       # Input validation tests
│   ├── conftest.py          # Pytest configuration
│   └── helpers.py           # Test helper functions
├── docs/                    # Legacy documentation
├── new_docs/                # MkDocs documentation (current)
├── examples/                # Example notebooks and scripts
├── .github/                 # GitHub configuration
│   └── workflows/           # CI/CD workflows
├── pyproject.toml           # Project configuration & dependencies
├── noxfile.py               # Nox automation tasks
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── README.md                # Project README
└── CONTRIBUTING.md          # Contributor guidelines
```

## Core Architecture

### Main Modules

1. **plot.py** - Core plotting functions:
   - `hist()` - Main histogram plotting function
   - `histplot()` - Enhanced histogram plotting with more features
   - `hist2dplot()` - 2D histogram plotting
   - `funcplot()` - Function plotting
   - `model()` - Model overlay plotting

2. **label.py** - Experiment-specific labels and text:
   - Functions to add experiment-specific labels (CMS, ATLAS, etc.)
   - Text positioning and formatting utilities
   - `add_text()`, `append_text()`, `savelabels()`, `save_variations()`

3. **utils.py** - Plot manipulation utilities:
   - `subplots()` - Enhanced subplot creation
   - `append_axes()` - Axis appending utilities
   - `yscale_legend()`, `yscale_anchored_text()` - Y-axis scaling utilities
   - `sort_legend()`, `merge_legend_handles_labels()` - Legend utilities
   - `mpl_magic()` - Jupyter notebook magic

4. **_utils.py** - Internal utilities:
   - Histogram data processing
   - `EnhancedPlottableHistogram` class
   - `get_plottables()`, `make_plottable_histogram()` - Histogram conversion

5. **styles/** - Matplotlib style definitions:
   - Each experiment has its own style file
   - Styles define colors, fonts, sizes, etc. to match collaboration requirements
   - `set_style()` function to apply styles

6. **exp_*.py** - Experiment-specific convenience modules:
   - Each provides shortcuts to experiment-specific styles and labels
   - e.g., `mplhep.cms.label()`, `mplhep.atlas.label()`

### Key Classes

- `EnhancedPlottableHistogram` - Enhanced histogram data structure
- `StairsArtists` - Return type for stairs plots
- `ErrorBarArtists` - Return type for error bar plots
- `ColormeshArtists` - Return type for colormesh plots
- `Config` - Configuration management class

## Development Workflow

### Setting Up Development Environment

```bash
# Clone and install in editable mode
python -m pip install --upgrade --editable ".[all]"

# Or use convenience script
bash install.sh

# Install pre-commit hooks
pre-commit install
```

### Running Tests

**Quick tests (without notebooks):**
```bash
pytest --mpl --ignore=tests/test_notebooks.py
```

**Full test suite:**
```bash
python -m pytest -r sa --mpl --mpl-results-path=pytest_results -n 4
```

**Using Nox:**
```bash
nox -s tests          # Run tests
nox -s lint           # Run linters
nox -s docs           # Build documentation
nox -s docs -- --serve  # Serve documentation locally
```

### Testing Strategy

- **Visual regression testing**: Uses `pytest-mpl` to compare generated plots against baseline images
- **Baseline images**: Stored in `tests/baseline/`
- **Parallel execution**: Tests run in parallel with `pytest-xdist` (`-n 4`)
- **Markers**: `@pytest.mark.latex` for tests requiring LaTeX

### Generating New Baseline Images

When plots are intentionally changed:

```bash
# Generate new baselines
python -m pytest -r sa --mpl -n 4 --mpl-generate-path=tests/baseline

# Or with Nox
nox -s generate_examples_figures
```

**Important**: Only commit actually modified baseline images, not bit-wise different but visually identical ones.

## Code Quality & Style

### Linting & Formatting

- **Tool**: Ruff (replaces black, isort, flake8, pylint, etc.)
- **Type checking**: mypy
- **Pre-commit hooks**: Enforced via `.pre-commit-config.yaml`

**Running linters:**
```bash
# Via pre-commit
pre-commit run --all-files

# Via Nox
nox -s lint
```

### Ruff Configuration

Extensive Ruff rules enabled in `pyproject.toml`:
- `B` - flake8-bugbear
- `I` - isort (import sorting)
- `PERF` - performance lints
- `ARG` - unused arguments
- `C4` - comprehensions
- `DTZ` - datetime timezone
- `UP` - pyupgrade (modern Python idioms)
- `NPY` - NumPy-specific rules
- `TRY` - tryceratops (exception handling)
- Many more (see pyproject.toml:146-183)

**Key ignores:**
- `PLR09` - Too many arguments/branches (complexity checks)
- `ISC001` - Conflicts with formatter
- `T20` - print statements (allowed in tests/examples)

### Type Checking

- **mypy** configured in `pyproject.toml`
- Target: Python 3.9+
- Currently not strict (gradual typing)
- Run via pre-commit hook

### Conventional Commits

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification.

**Format:** `<type>(<scope>): <description>`

**Common types:**
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `test:` - Test changes
- `refactor:` - Code refactoring

**Examples:**
```
feat(plot): add support for weighted histograms
fix(label): correct ATLAS label positioning
docs: update API documentation
chore(deps): update matplotlib to 3.8
```

## Key Conventions

### Code Style

1. **Imports**: Sorted automatically by Ruff (isort rules)
   - Standard library first
   - Third-party packages second
   - Local imports last
   - Use `from __future__ import annotations` for modern type hints

2. **Naming**:
   - Functions: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_CASE`
   - Private functions: `_leading_underscore`

3. **Documentation**:
   - Docstrings for public functions
   - Type hints preferred
   - Examples in docstrings where helpful

4. **Error handling**:
   - Use specific exceptions
   - Avoid bare `except:`
   - Follow TRY rules from Ruff

### Testing Conventions

1. **Test files**: Named `test_*.py`
2. **Test functions**: Named `test_<feature>`
3. **Visual tests**: Use `@pytest.mark.mpl_image_compare` decorator
4. **Markers**: Use `@pytest.mark.latex` for LaTeX-requiring tests
5. **Fixtures**: Defined in `conftest.py`
6. **Helpers**: Shared test utilities in `helpers.py`

### Git Workflow

1. **Branching**: Feature branches from `main`
2. **Commits**: Follow Conventional Commits (enforced by pre-commit hook)
3. **PR titles**: Also follow Conventional Commits
4. **Merging**: Squash commits on merge (final commit message must follow convention)

## Dependencies

### Core Dependencies
- `matplotlib>=3.4` - Plotting library
- `numpy>=1.16.0` - Numerical computing
- `mplhep-data>=0.0.4` - Data files (fonts, etc.)
- `uhi>=0.2.0` - Unified Histogram Interface
- `packaging` - Version parsing

### Development Dependencies
- `pre-commit` - Git hook management
- `pytest`, `pytest-mpl`, `pytest-xdist` - Testing
- `nox` - Task automation
- `ruff` - Linting & formatting
- `mypy` - Type checking

### Documentation Dependencies
- `mkdocs>=1.6` - Documentation generator
- `mkdocs-material[imaging]>=9.0` - Material theme
- `mkdocstrings[python]>=0.20` - API documentation

### Optional Dependencies
- `hist`, `boost_histogram` - Histogram libraries
- `uproot`, `uproot4` - ROOT file reading
- `scipy>=1.1.0` - Scientific computing

## Important Notes for AI Assistants

### When Making Changes

1. **Always run tests** before committing:
   ```bash
   pytest --mpl --ignore=tests/test_notebooks.py
   ```

2. **Run pre-commit hooks**:
   ```bash
   pre-commit run --all-files
   ```

3. **Update baseline images** if plots intentionally change:
   ```bash
   nox -s generate_examples_figures
   ```

4. **Follow Conventional Commits** for commit messages

5. **Update documentation** if adding new features

### Common Tasks

**Add a new plotting function:**
1. Add to `src/mplhep/plot.py`
2. Export in `src/mplhep/__init__.py`
3. Add tests in `tests/test_basic.py` or new test file
4. Add baseline images if visual test
5. Update documentation

**Add a new experiment style:**
1. Create `src/mplhep/styles/<exp>.py`
2. Create `src/mplhep/exp_<exp>.py`
3. Import in `src/mplhep/__init__.py`
4. Add tests
5. Add examples

**Fix a bug:**
1. Write a test that reproduces the bug
2. Fix the bug
3. Ensure test passes
4. Run full test suite
5. Commit with `fix:` prefix

### Anti-Patterns to Avoid

1. **Don't** modify baseline images unless you're intentionally changing plot output
2. **Don't** commit without running pre-commit hooks
3. **Don't** use bare `except:` clauses
4. **Don't** add print statements in production code (use logging)
5. **Don't** skip tests or linting
6. **Don't** use `git add -a` when updating baselines (be selective)

### Understanding Visual Tests

Visual regression tests compare generated plots pixel-by-pixel against baseline images:

```python
@pytest.mark.mpl_image_compare
def test_my_plot():
    fig, ax = plt.subplots()
    mplhep.histplot([1,2,3], bins=3, ax=ax)
    return fig
```

- Returns the figure for comparison
- Baseline stored as PNG in `tests/baseline/`
- Named `<test_module_name>.<test_function_name>.png`
- Small differences may be acceptable (tolerance configurable)

### Working with Experiments

Each HEP experiment has specific style requirements:

- **CMS**: Helvetica font, specific label positions, ROOT-like appearance
- **ATLAS**: Similar to CMS but with ATLAS-specific labels
- **LHCb**: Unique color scheme and label requirements
- **ALICE**: ALICE collaboration standards
- **DUNE**: DUNE experiment standards

When working with experiment-specific code:
1. Check existing experiment modules for patterns
2. Consult collaboration plot guidelines
3. Verify with baseline images
4. Be careful with font rendering (can differ across systems)

### Performance Considerations

- Use NumPy operations over Python loops
- PERF rules from Ruff help catch performance issues
- Benchmark with `pytest-benchmark` if needed
- Consider memory usage for large histograms

## CI/CD

### GitHub Actions Workflows

- **ci.yml**: Main CI pipeline (tests on multiple Python versions)
- **ci_latex.yml**: Tests requiring LaTeX installation
- **ci-pages.yml**: Documentation building and deployment
- **cd.yml**: Continuous deployment (PyPI publishing)
- **head-dependencies.yml**: Tests with development versions of dependencies

### Pre-commit CI

- Runs pre-commit hooks on PRs
- Auto-fixes issues when possible
- Updates pre-commit versions automatically

## Documentation

### Structure

- **Old docs**: In `docs/` (Sphinx-based)
- **New docs**: In `new_docs/` (MkDocs-based) - **Current**
- **API docs**: Auto-generated from docstrings via mkdocstrings
- **Examples**: Jupyter notebooks in `examples/`

### Building Documentation

```bash
# Build docs
nox -s docs

# Serve locally
nox -s docs -- --serve

# Fast build (no code execution)
nox -s docs -- --fast
```

### Contributing to Documentation

See `new_docs/CONTRIBUTING_DOC.md` for detailed documentation contribution guidelines.

## Version Management

- **Version source**: Git tags (via hatch-vcs)
- **Version file**: `src/mplhep/_version.py` (auto-generated)
- **Bump version**: Uses bumpversion tool
- **Config**: `.bumpversion.cfg`

## Useful Commands Reference

```bash
# Development
python -m pip install -e ".[all]"        # Install in editable mode
bash install.sh                          # Convenience install script

# Testing
pytest --mpl --ignore=tests/test_notebooks.py  # Quick tests
pytest --mpl -n 4                        # Parallel tests
nox -s tests                             # Nox tests
nox -s root_tests                        # ROOT integration tests (requires conda)

# Linting
pre-commit run --all-files               # Run all pre-commit hooks
nox -s lint                              # Run linters via Nox

# Baseline generation
pytest --mpl-generate-path=tests/baseline  # Generate baselines
nox -s generate_examples_figures         # Generate via Nox

# Documentation
nox -s docs                              # Build docs
nox -s docs -- --serve                   # Serve docs locally
nox -s docs -- --serve --port 8080       # Custom port
nox -s docs -- --fast                    # Fast build

# Developer CLI
dev                                      # Run developer CLI (if installed)
```

## Additional Resources

- **Main Documentation**: https://scikit-hep.org/mplhep/
- **GitHub Repository**: https://github.com/scikit-hep/mplhep
- **PyPI Package**: https://pypi.org/project/mplhep/
- **Conda Package**: https://anaconda.org/conda-forge/mplhep
- **Scikit-HEP**: https://scikit-hep.org/
- **Tutorial**: https://www.youtube.com/watch?v=gUziXqCGe0o (PyHEP 2020)
- **Binder Examples**: https://mybinder.org/v2/gh/scikit-hep/mplhep/master

## Quick Reference for Common Operations

### Running a complete check before PR

```bash
# 1. Run linters
pre-commit run --all-files

# 2. Run tests
pytest --mpl -n 4

# 3. Build docs (optional)
nox -s docs

# 4. If plots changed, regenerate baselines
nox -s generate_examples_figures
```

### Adding a new feature

```bash
# 1. Create feature branch
git checkout -b feat/my-feature

# 2. Make changes
# ... edit files ...

# 3. Add tests
# ... add to tests/ ...

# 4. Run tests
pytest --mpl -n 4

# 5. Update docs if needed
# ... edit new_docs/docs/ ...

# 6. Commit with conventional commit message
git commit -m "feat: add my awesome feature"

# 7. Push and create PR
git push origin feat/my-feature
```

## Project Philosophy

- **User-friendly**: Easy to create publication-quality plots
- **Collaboration-compliant**: Follow experiment-specific guidelines
- **Well-tested**: Comprehensive visual regression testing
- **Documented**: Clear examples and API documentation
- **Maintained**: Active development, regular updates
- **Community-driven**: Part of Scikit-HEP ecosystem

---

**Last Updated**: 2025-11-17
**Version**: Auto-generated from repository analysis

For questions or clarifications, refer to CONTRIBUTING.md or open an issue on GitHub.
