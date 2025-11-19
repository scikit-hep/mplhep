# Contributing to mplhep

We are happy to accept contributions to `mplhep` via Pull Requests to the GitHub repo. To get started fork the repo.

## Bug Reports

Please open an [issue](https://github.com/scikit-hep/mplhep/issues).

## Installing the development environment

```bash
### Using pixi (recommended)

[Pixi](https://prefix.dev/docs/pixi/overview) provides a fast, reproducible development environment:

```bash
```bash
```bash
# Install the default environment (includes all development tools)
pixi install

# Activate a shell with all tools
pixi shell

# Or run commands directly
pixi run test-basic
```

Available pixi tasks (now just `pixi run <task>`):
- `pixi run test` - Run full test suite with visual comparison
- `pixi run test-parallel` - Run tests in parallel (auto-detects optimal worker count)
- `pixi run test-basic` - Run basic tests without visual comparison
- `pixi run generate-baseline` - Generate new baseline images
- `pixi run lint` - Check code with ruff
- `pixi run format` - Format code with ruff
- `pixi run format-check` - Check formatting without changes

Benchmarking tasks (requires benchmark environment):
- `pixi run -e benchmark benchmark` - Run benchmark tests
- `pixi run -e benchmark benchmark-run` - Run and save benchmark results
- `pixi run -e benchmark benchmark-compare` - Compare benchmark results

**Note:** For development work, use the default environment (`pixi install`) which includes all tools. The specialized environments (`dev`, `test`, `docs`, `benchmark`) are available for specific use cases.

```
python -m pip install --upgrade --editable ".[all]"
```
Also conveniently accessible as `bash install.sh`.

## Pull Requests

### Pull Requests Procedure

If you would like to make a pull request please:

1. Make a fork of the project
2. Clone your fork locally
3. Install `pre-commit` and the project's `pre-commit` hooks
4. Test your changes with `pytest`
5. Commit your changes to a feature branch of your fork, push to your branch
6. Make a PR

### Running the tests

You can run the unit tests (which should be fast!) via the following command:

**With  pytest**

```bash
pytest --mpl --ignore=tests/test_notebooks.py
```

Note: This ignores the notebook tests (which are run via [papermill](https://github.com/nteract/papermill)) and run somewhat slow.

Make sure to run the complete suite before submitting a PR

```bash
python -m pytest -r sa --mpl --mpl-results-path=pytest_results -n 4
```

**With  nox**

```bash
nox -s tests
```

### Making a pull request

We follow [Conventional Commit](https://www.conventionalcommits.org/) for commit messages and PR titles. Since we merge PR's using squash commits, it's fine if the final commit messages (proposed in the PR body) follow this convention.

### Generating Reference Visuals

If you modified expected outcomes of the tests. New baseline visuals can be generated using this command:

**With  pytest**

```bash
 python -m pytest -r sa --mpl -n 4 --mpl-generate-path=tests/baseline
```

**With  nox**

```bash
 nox -s generate_examples_figures
```

Only include the actually modified baseline images in your PR! Running `git add -a` and the like will sometimes result in including images which are visually identically but not the same bit-wise.

### Linting and Formatting

We use `pre-commit` to manage code formatting and linting. Make sure to run it before committing your changes:

**With  pre-commit**

```bash
pre-commit run --all-files
```

**With  nox**

```bash
nox -s lint
```

## Contributing to the documentation

The documentation is built using [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. To contribute to the documentation, please look at the [`new_docs/CONTRIBUTING_DOC.md`](CONTRIBUTING_DOC.md) file for instructions.
