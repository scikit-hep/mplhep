# Agentic development instructions

# Key rules
- Never make difficult to revert git operations like git push and absolutely never with   `--force`
- Never make a commit unless explicitly instructed to do so


# Development guidelines
- The general contributing guidelines are described @CONTRIBUTING.md

## Testing Guidelines
- This is a plotting library, as such most of the test we need and use are visual comparison tests. When introducing new features, ensure an appropriate test is added.
- **NEVER adjust tolerance values in pytest-mpl image comparison tests from 0** - We need to be able to reproduce test with 100% fidelity.
