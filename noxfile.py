from __future__ import annotations

import argparse

import nox

nox.options.sessions = ["lint", "tests"]
nox.needs_version = ">=2025.2.9"
nox.options.default_venv_backend = "uv|venv"

PYTHON_ALL_VERSIONS = ["3.9", "3.13"]


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("prek")
    session.run("prek", "run", "--all-files", *session.posargs)


@nox.session(python=PYTHON_ALL_VERSIONS)
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install("-e", ".")
    session.install(*pyproject["project"]["optional-dependencies"]["test"])
    session.run("pytest", "--mpl", "-n", "auto", *session.posargs)


@nox.session(reuse_venv=True)
def generate_examples_figures(session: nox.Session) -> None:
    """
    Generate the example figures. Pass "-- tests/test_examples_*.py" to run only the relevant tests.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install("-e", ".")
    session.install(*pyproject["project"]["optional-dependencies"]["test"])
    session.run(
        "pytest",
        "--mpl-generate-path=tests/baseline",
        *session.posargs,
    )


@nox.session(venv_backend="conda", reuse_venv=True)
def root_tests(session):
    """
    Test ROOT histograms. Note: a conda installation is needed to run this test.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.conda_install("--channel=conda-forge", "ROOT")
    session.install("-e", ".")
    session.install(*pyproject["project"]["optional-dependencies"]["test"])
    session.run("pytest", "tests/test_make_plottable_histogram.py", *session.posargs)


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    """
    Build the documentation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve the docs locally. By default, the docs are built instead.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Build docs without generating the codeblock examples.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to serve the docs on if --serve is used. Default is 8000.",
    )
    args, posargs = parser.parse_known_args(session.posargs)

    pyproject = nox.project.load_toml("pyproject.toml")
    session.install("-e", ".")
    session.install(*pyproject["project"]["optional-dependencies"]["docs"])
    session.install(*pyproject["project"]["optional-dependencies"]["test"])
    session.chdir("new_docs")
    session.install("-r", "requirements.txt")

    cmd = ["mkdocs"]

    if args.serve:
        cmd.extend(["serve", "--dev-addr", f"127.0.0.1:{args.port}"])
    else:
        cmd.append("build")

    if args.fast:
        cmd.extend(["-f", "mkdocs_norender.yml"])

    session.run(*cmd, *posargs)
