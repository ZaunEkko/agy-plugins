---
name: commit-push-pr
description: Create a branch when currently on main, create exactly one commit from the current changes, push the branch to origin, and open a pull request with GitHub CLI. Use only when the user explicitly asks to create or open a pull request, or explicitly requests the full commit-push-PR workflow. Do not use for commit-only, commit-and-push-only, or branch-publishing requests without explicit PR intent.
---

# Commit, Push, and Open PR

Adapt Anthropic's `/commit-push-pr` workflow as a native Antigravity skill.

## Workflow

1. Inspect `git status`, the staged and unstaged changes with `git diff HEAD`, and the current branch with `git branch --show-current`.
2. If the current branch is exactly `main`, create a new work branch with `git checkout -b <branch>`.
3. Stage the current changes and create exactly one commit with an appropriate message. Append:

```text
Co-authored-by: Antigravity <noreply@google.com>
```

4. Push the current branch to `origin`.
5. Create a pull request with `gh pr create`.
6. Describe the full branch in the PR body with a 1–3 bullet summary, a test-plan checklist, and:

```text
Generated with Antigravity assistance.
```

7. Return the pull request URL.

## Boundaries

- Complete commit, push, and PR creation as one workflow; do not turn this into a push-only or PR-only path.
- If there are no changes to commit, report that the original workflow cannot continue instead of creating an empty commit.
- Create a new branch automatically only when the current branch is `main`; do not add other policy-driven branch transitions to the original workflow.
- Never force push, stage obvious secrets, or perform unrelated work.
- Stop if GitHub CLI is unavailable or unauthenticated, or if `origin` is missing.
