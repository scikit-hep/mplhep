# Contributing to mplhep

We are happy to accept contributions to `mplhep` via Pull Requests to the GitHub
repo. To get started fork the repo.

## Bug Reports

Please open an issue.

## Installing the development environment

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

You can run the unit tests (which should be fast!) via the following command.

```bash
pytest --mpl --ignore=tests/test_notebooks.py
```

Note: This ignores the notebook tests (which are run via
[papermill](https://github.com/nteract/papermill) and run somewhat slow. Make
sure to run the complete suite before submitting a PR

```bash
pytest --mpl
```

### Making a pull request

We follow [Conventional Commit](https://www.conventionalcommits.org/) for commit
messages and PR titles. Since we merge PR's using squash commits, it's fine if
the final commit messages (proposed in the PR body) follow this convention.

### Generating Reference Visuals

If you modified expected outcomes of the tests. New baseline visuals can be
generated using this command:

```bash
pytest --mpl-generate-path=tests/baseline
```

Only include the actually modified baseline images in your PR! Running `git add
-a` and the like will sometimes result in including images which are visually
identically but not the same bit-wise.
