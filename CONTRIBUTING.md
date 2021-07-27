# Contributing to mplhep

We are happy to accept contributions to `mplhep` via Pull Requests to the GitHub repo. To get started fork the repo.

## Pull Requests

### Pull Requests Procedure

If you would like to make a pull request please:

1. Make a fork of the project
2. Install `pre-commit` and the project's `pre-commit` hooks
3. Commit your changes to a feature branch of your fork push to your branch
4. Test your changes with `pytest`
5. Make a PR

## Bug Reports

TBD.

## Installing the development environment

```
python -m pip install --upgrade --editable ".[all]"
```

<!-- To make the PR process much smoother we also strongly recommend that you setup the Git pre-commit hook for [Black](https://github.com/psf/black) by running

```
pre-commit install
```

This will run `black` over your code each time you attempt to make a commit and warn you if there is an error, canceling the commit. -->

## Running the tests

You can run the unit tests (which should be fast!) via the following command.

```bash
pytest --mpl --ignore=tests/test_notebooks.py
```

Note: This ignores the notebook tests (which are run via [papermill](https://github.com/nteract/papermill) which run somewhat slow.
Make sure to run the complete suite before submitting a PR

```bash
pytest --mpl
```

## Making a pull request

We try to follow [Conventional Commit](https://www.conventionalcommits.org/) for commit messages and PR titles. Since we merge PR's using squash commits, it's fine if the final commit messages (proposed in the PR body) follow this convention.

## Generating Reference Visuals

If you modified expected outcomes of the test. New baseline visuals can be generated using this command:

```bash
pytest --mpl-generate-path=tests/baseline
```
