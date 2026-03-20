---
mode: "agent"
description: "Start MypyFixer autonomous flow and create a PR"
---

Use the selected `MypyFixer` agent to run an autonomous fix workflow.

1. Run `uv run mypy app --strict`.
2. Fix the smallest type error.
3. Re-run `uv run mypy app --strict` after each fix.
4. Continue until mypy has zero errors.
5. Run relevant tests for changed files.
6. Commit with `fix(types): <short summary>`.
7. Push the current branch (do not create or switch branches).
8. Open a PR targeting the current branch (not `main`).

Return:
- changed files
- final mypy output summary
- test results summary
- commit hash
- PR URL
