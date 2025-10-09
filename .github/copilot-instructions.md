## General Copilot Instructions

- Commit messages and PR names should follow Conventional Commits specification (https://www.conventionalcommits.org/en/v1.0.0/)
- Use present tense ("add feature" not "added feature")

## Folder Structure

- `/src/mplhep`: Contains the source code for project.
- `/tests`: Contains tests.
- `/docs`: Contains documentation for the project, including API specifications and user guides.
- `/examples`: Is a joint folder for examples which are parts of both documentation and tests.

## Coding Standards

- Use single quotes for strings. Such that printed statements containing strings can use double quotes.
- Follow PEP 8 guidelines for Python code.
- Write docstrings for all public functions and classes using the NumPy/SciPy style.
- Follow ruff configuration in pyproject.toml for linting and formatting
- Use type hints where appropriate (mypy configuration available)
- Run pre-commit hooks before committing


## Testing Guidelines

- For new features, add tests to the `tests/copilot` directory
- When resolving issues, write tests into `tests/from_issues` directory
- Use pytest-mpl for matplotlib-based tests that require visual comparison (most cases)
- If you think it's useful, you can run the test suite with `python -m pytest -r sa --mpl --mpl-results-path=pytest_results -n 4` before submitting changes
- Intentionally changed behaviours might require a new baseline generated as `pytest --mpl-generate-path=tests/baseline` if visual outputs change


## Project-Specific Guidelines

- Keep backward compatibility in mind for public APIs
- Consider optional dependencies vs core requirements carefully
