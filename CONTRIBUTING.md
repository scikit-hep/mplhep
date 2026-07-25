# Contributing to mplhep

We are happy to accept contributions to `mplhep` via Pull Requests to the GitHub repo. To get started fork the repo.

## AI Policy

AI-assisted contributions are welcome. We ask that you:

- **Disclose** that AI was used, and name the tool and model.
- **Review and understand every line you submit.** You are responsible for it.
- **Meet the same quality, testing, and style standards** as any other contribution.
- **Do not use fully autonomous agents** to open issues or pull requests.
- **Respond to review comments yourself.**

This applies to issues and comments as well as pull requests. Using AI for
translation or grammar help is fine and needs no disclosure.

Unsolicited, undisclosed, or low-effort AI pull requests may be closed at
maintainer discretion.

### Crediting AI in commits

Only humans can be named as co-authors, and an AI can _never_ sign off on a commit.

- Do **not** add a `Co-authored-by:` trailer for an AI. That trailer asserts
  authorship and a copyright interest — an AI is a tool, not an author, and the
  work stays yours.
- Do **not** let a tool add `Signed-off-by:` on your behalf. That line certifies
  the [Developer Certificate of Origin](https://developercertificate.org/), a
  legal statement only a human can make.

Credit AI assistance with the trailer the Linux kernel standardised in
[`Documentation/process/coding-assistants.rst`](https://docs.kernel.org/process/coding-assistants.html):

```text
Assisted-by: <harness>:<model>
```

for example:

```text
Assisted-by: claude-code:claude-opus-5
```

Put the trailer in your commit messages — that is the only place it needs to be.
When a pull request is squash-merged, GitHub builds the final message out of the
branch's commit messages, so the trailer carries through on its own. It does not
read the pull request description, so putting the trailer only there loses it.

A branch with several commits repeats the trailer once per commit in the squashed
message, so keep the branch to a single well-written commit where you can.

## Bug Reports

Please open an [issue](https://github.com/scikit-hep/mplhep/issues).

## Cloning the repository

```bash
git clone https://github.com/scikit-hep/mplhep.git
```

That is all you need — roughly 26 MB.

The built documentation site does not live here. It is published to
[scikit-hep/mplhep_docs](https://github.com/scikit-hep/mplhep_docs), because keeping the
rendered HTML for every released version in this repository meant every contributor
downloaded the whole published site just to work on the library. Doc *sources* stay here,
under `new_docs/`; only the build output is elsewhere.

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

We follow [Conventional Commit](https://www.conventionalcommits.org/) for commit messages and PR titles. On a squash-merge the final message is assembled from the PR title and the branch's commit messages, so both need to follow the convention — the PR description is not used. A single, well-written commit per pull request gives the cleanest history; a PR whose commits are already well organised may instead be rebased on, in which case every one of them lands as it is.

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

The documentation is built using [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. To contribute to the documentation, please look at the
[`new_docs/CONTRIBUTING_DOC.md`](https://github.com/scikit-hep/mplhep/blob/main/new_docs/CONTRIBUTING_DOC.md)
file for instructions.
