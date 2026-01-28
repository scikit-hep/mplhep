# Claude Code Instructions for mplhep

## Testing Guidelines

- **NEVER adjust tolerance values in pytest-mpl image comparison tests.** If tests fail due to image differences, regenerate the baseline images properly instead of increasing tolerances.
- Baseline images should be regenerated using `pytest --mpl-generate-path=tests/baseline <test_path>`
- If baseline regeneration doesn't fix CI failures, investigate the root cause (e.g., platform differences, font rendering) rather than masking the issue with tolerance changes.
