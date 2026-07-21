# Contributing to mplhep

We are happy to accept contributions to `mplhep` via Pull Requests to the GitHub repo. To get started fork the repo.

## Bug Reports

Please open an [issue](https://github.com/scikit-hep/mplhep/issues).

## Installing the development environment

```bash
python -m pip install --upgrade --editable ".[all]"
```
Also conveniently accessible as `bash install.sh`.

## Pull Requests

### Pull Requests Procedure

If you would like to make a pull request please:

1. Make a fork of the project
2. Clone your fork locally
3. Install `prek` and the project's `pre-commit` hooks
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

We use `prek` to manage code formatting and linting. Make sure to run it before committing your changes:

**With  prek**

```bash
prek run --all-files
```

**With  nox**

```bash
nox -s lint
```

## Contributing to the documentation

The documentation is built using [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. To contribute to the documentation, please look at the [`new_docs/CONTRIBUTING_DOC.md`](CONTRIBUTING_DOC.md) file for instructions.
