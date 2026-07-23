# Agentic development instructions

# Key rules
- Ask for confirmation before committing. Editing files freely is fine; turning those edits
  into a commit is the user's call. Amending or rewriting existing commits needs its own
  confirmation, separate from any approval to commit
- Ask for confirmation before anything that reaches the remote — `git push`, opening or
  editing a pull request, creating or deleting remote branches or tags. Doing it on request
  is fine; doing it unprompted is not. Approval is per-request and does not carry over: being
  told to push one branch is not permission to push the next one.
- Never push to `main`/`master` unless explicitly instructed to do so
- Never force-push unless explicitly instructed. `--force` needs its own confirmation even
  when a plain push was already approved, and `--force-with-lease` is preferred over `--force`
- Prefer proposing the command for the user to run over running it, when an operation is hard
  to undo. Say plainly what is irreversible about it


# Development guidelines
- The general contributing guidelines are described @CONTRIBUTING.md

## Testing Guidelines
- This is a plotting library, as such most of the test we need and use are visual comparison tests. When introducing new features, ensure an appropriate test is added.
- **NEVER adjust tolerance values in pytest-mpl image comparison tests from 0** - We need to be able to reproduce test with 100% fidelity.
