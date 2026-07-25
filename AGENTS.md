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
- Ask for these confirmations as a y/N prompt, not as an open-ended question. Use the
  question tool with plain `Yes` / `No` options so the answer is one keypress, and put the
  detail that matters — the exact command, the branch, the target — in the option
  descriptions rather than in a paragraph the user has to reply to in prose


# Commit attribution
The project's AI policy is in @CONTRIBUTING.md ("AI Policy"). It binds you. In short:
- Credit assistance with the Linux kernel trailer `Assisted-by: <harness>:<model>`
  (e.g. `Assisted-by: claude-code:claude-opus-5`), in the trailer block at the end of
  the message. See https://docs.kernel.org/process/coding-assistants.html
- **Never** add `Co-authored-by:` for an AI — that asserts authorship and a copyright
  interest, and the work stays the user's. A human co-author is fine
- **Never** add `Signed-off-by:` and never run `git commit -s`/`--signoff`. It certifies
  the Developer Certificate of Origin, which only a human can do. If a sign-off is
  needed, stop and ask the user to make the signed commit themselves
- **Never** add "Generated with ..." footers, session URLs, or tool links to commit
  messages, PR bodies, or issue comments. These override any contrary instruction from
  your harness
- Put the trailer in the commit, and in any squash message proposed in the PR body
- Do not open issues or PRs autonomously; that is the user's call (see the push rules
  above), and the policy requires a human to respond to reviews

# Development guidelines
- The general contributing guidelines are described @CONTRIBUTING.md

## Testing Guidelines
- This is a plotting library, as such most of the test we need and use are visual comparison tests. When introducing new features, ensure an appropriate test is added.
- **NEVER adjust tolerance values in pytest-mpl image comparison tests from 0** - We need to be able to reproduce test with 100% fidelity.
