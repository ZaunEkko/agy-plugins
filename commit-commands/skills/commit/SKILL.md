---
name: commit
description: Create exactly one local Git commit from the current staged and unstaged changes, using recent history for message style and adding Antigravity co-author attribution. Use when the user explicitly asks to commit, save, record, or check in current changes. Do not use merely because implementation finished, and do not push or open a pull request.
---

# Commit

Adapt Anthropic's `/commit` workflow as a native Antigravity skill.

## Workflow

1. Inspect `git status`.
2. Inspect staged and unstaged changes with `git diff HEAD`.
3. Inspect the current branch with `git branch --show-current`.
4. Inspect the latest ten commits with `git log --oneline -10` and match the repository's commit-message style.
5. Based on the current changes, stage the relevant files.
6. Create exactly one commit with an appropriate message and append this attribution block:

```text
Generated with [Antigravity](https://antigravity.google/product)

Co-authored-by: gemini-code-assist[bot] <176961590+gemini-code-assist[bot]@users.noreply.github.com>
```

7. Report the resulting commit and status.

## Boundaries

- If there are no changes to commit, report that instead of creating an empty commit.
- Avoid staging obvious secrets such as `.env` or credential files.
- Do not push, open a pull request, amend an existing commit, or perform unrelated work.
