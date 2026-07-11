---
name: commit-push-pr
description: "Publish work as a GitHub pull request: create a branch when currently on main, create one attributed commit when the worktree has changes or reuse existing branch commits when it is clean, push to origin, and open a PR through the bundled wrapper that guarantees linked Antigravity attribution in the body. Use only when the user explicitly asks to create or open a pull request, including push-and-PR requests for already committed work. Do not use for commit-only, commit-and-push-only, or branch-publishing requests without explicit PR intent."
---

# Commit, Push, and Open PR

Adapt Anthropic's `/commit-push-pr` workflow as a native Antigravity skill.

## Workflow

1. Inspect `git status`, the staged and unstaged changes with `git diff HEAD`, the current branch with `git branch --show-current`, and the commits between the intended PR base and `HEAD`.
2. Require GitHub CLI, an authenticated `gh` session, and an `origin` remote. Use a base branch explicitly named by the user; otherwise use the remote default branch.
3. If the worktree has staged or unstaged changes:
   - Read the active model name from the `commit-commands runtime metadata for this turn` developer context injected by the plugin hook. Use the exact `Model:` line provided there; do not independently infer it from config, environment variables, or transcript files.
   - If that runtime metadata is missing or says the model is unavailable, stop before creating a branch, staging, or committing. Tell the user to review and trust the plugin hook with `/hooks`, then retry in a new turn.
   - If the current branch is exactly `main`, create a new work branch with `git checkout -b <branch>`.
   - Stage the current changes and create exactly one commit with an appropriate message. Append this attribution block:

```text
Generated with [Antigravity](https://antigravity.google/product)
Model: <active-model-name>

Co-authored-by: gemini-code-assist[bot] <176961590+gemini-code-assist[bot]@users.noreply.github.com>
```

4. If the worktree is clean, do not create an empty commit. Continue only when `HEAD` contains at least one commit that is not in the intended PR base; this path publishes already committed work. If the current branch is exactly `main`, first create a new work branch at the current `HEAD` with `git checkout -b <branch>` so `main` is never pushed as the PR head.
5. Push the current branch to `origin`.
6. Draft the complete PR body with a 1–3 bullet summary and a test-plan checklist. Do not add product attribution yourself; the bundled wrapper owns it.
7. Resolve `scripts/create_pr_with_attribution.py` relative to this `SKILL.md`. Pass the complete PR body on stdin and pass the intended `gh pr create` arguments after `--`, for example:

```bash
python3 <skill-directory>/scripts/create_pr_with_attribution.py -- --title "<title>" --base "<base>" --head "<head>"
```

   On Windows, use `python` when `python3` is unavailable. The wrapper appends `Generated with [Antigravity](https://antigravity.google/product)`, creates the PR with `gh pr create --body-file`, reads it back with `gh pr view`, repairs it once with `gh pr edit` if needed, and fails unless the footer is the final non-empty line.
8. Return the pull request URL printed by the wrapper.

## Boundaries

- Complete commit-if-needed, push, and PR creation as one workflow; do not turn this into a push-only path.
- A clean worktree is valid only for publishing existing branch commits. If `HEAD` has no commits outside the intended PR base, report that there is no PR content instead of creating an empty commit or empty PR.
- Never call `gh pr create` directly or substitute another PR creation path; the bundled wrapper is required so the body attribution cannot be skipped.
- Create a new branch automatically only when the current branch is `main`; do not add other policy-driven branch transitions to the original workflow.
- Never force push, stage obvious secrets, or perform unrelated work.
- Stop if GitHub CLI is unavailable or unauthenticated, or if `origin` is missing.
