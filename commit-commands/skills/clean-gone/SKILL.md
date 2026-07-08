---
name: clean-gone
description: Remove every local Git branch marked [gone], force-removing its associated non-main worktree and force-deleting the branch to match Anthropic's original clean_gone command. Use only when the user explicitly asks to clean gone or deleted-remote branches and accepts this destructive cleanup. Never use merely because stale branches exist.
---

# Clean Gone Branches

Adapt Anthropic's `/clean_gone` workflow as a native Antigravity skill.

## Workflow

1. Run `git branch -v` and collect every local branch shown with `[gone]`. A `+` prefix indicates an associated worktree.
2. Run `git worktree list` and map worktree paths to those `[gone]` branches.
3. For each collected branch:
   - Report the branch being processed.
   - If it has an associated worktree and that path is not the main worktree from `git rev-parse --show-toplevel`, run `git worktree remove --force <path>`.
   - Run `git branch -D <branch>`.
4. Report every removed worktree and branch. If no branch is marked `[gone]`, report that no cleanup was needed.

## Original behavior

- Treat `[gone]` as the cleanup criterion; do not add merge-base, cleanliness, ignored-file, protected-branch, or integration-branch checks.
- Do not run `git fetch` or `git fetch --prune` automatically. The caller is responsible for refreshing remote-tracking state before invoking this skill when needed.
- Never remove the main worktree or delete remote branches.
