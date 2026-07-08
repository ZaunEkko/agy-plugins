# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` adapts the three slash commands from the [official Anthropic original](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) as native Antigravity skills:

```text
$commit
$commit-push-pr
$clean-gone
```

Workflow steps follow the original. Antigravity-specific differences are limited to native skill packaging, explicit-intent implicit selection, `$skill-name` invocation, and Antigravity attribution.

## Installation

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add commit-commands@zaunekko
```

Start a new Antigravity thread after installing or updating so the new skill metadata is loaded.

## Implicit selection examples

- "Commit these changes" can select `commit`.
- "Commit these changes, push, and open a PR" can select `commit-push-pr`.
- "Clean all gone branches" can select `clean-gone`.
- "The implementation is finished" does not authorize a Git side effect.

## `$commit`

Inspects `git status`, `git diff HEAD`, the current branch, and the latest ten commits. It stages the current changes and creates exactly one commit with:

```text
Co-authored-by: Antigravity <noreply@openai.com>
```

It does not push or open a PR, and it does not create an empty commit when there are no changes.

## `$commit-push-pr`

Inspects the current status, diff, and branch. It creates a new branch only when the current branch is exactly `main`, then creates one commit, pushes to `origin`, and opens a PR with `gh pr create`.

The skill requires explicit PR intent. Like the original, it has no publish-without-a-new-commit path and does not create policy-driven replacement branches for names other than `main`.

GitHub CLI must be installed and authenticated, and the repository must have an `origin` remote.

## `$clean-gone`

Uses `git branch -v` and `git worktree list` to find branches marked `[gone]`. For each candidate, it force-removes an associated non-main worktree with `git worktree remove --force`, then force-deletes the branch with `git branch -D`.

This deliberately matches the original destructive behavior: it does not fetch, verify merges, inspect worktree cleanliness, protect ignored files, or apply integration-branch rules. Review repository state before invoking it.

## Local validation

```bash
python -m unittest discover -s tests
agy plugin list
```
