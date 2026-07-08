# AGENTS.md

Guidance for coding agents working in this repository.

## What this repo is

This repository is an Antigravity plugin marketplace. It is content/configuration for skills, hooks, output styles, and docs rather than a conventional app package.

Current tracked layout uses top-level plugin directories:

- `commit-commands/skills/*/SKILL.md`
- `explanatory-output-style/hooks/hooks.json`
- `explanatory-output-style/hooks/session_start.py`
- `explanatory-output-style/skills/explanatory-output.md`
- `docs/<plugin>/README.md`
- `i18n/<locale>/...`

This checkout uses top-level plugin directories rather than a `plugins/` wrapper. Check tracked files before adding paths.

## Validate by affected surface

No global build/lint command is configured. Run focused checks:

```bash
python -m py_compile explanatory-output-style/hooks/session_start.py
python explanatory-output-style/hooks/session_start.py
python -m json.tool explanatory-output-style/hooks/hooks.json
agy-plugin marketplace list
```

Only run unittest commands when a `tests/` tree exists or the task adds one. For docs-only work, check links, paths, install commands, and i18n mirrors.

## Product behavior lives in markdown

For `commit-commands`, the `SKILL.md` frontmatter and workflow text define the actual Antigravity behavior. Preserve explicit boundaries:

- `commit` creates one local commit and does not push or open a PR.
- `commit-push-pr` is only for explicit PR intent and stops if prerequisites such as `origin` or authenticated `gh` are missing.
- `clean-gone` force-removes `[gone]` local branches/worktrees and is destructive; do not broaden when it auto-triggers.

For `explanatory-output-style`, hook behavior spans `hooks.json` and `session_start.py`. Keep hook output valid JSON and document any changed trust/review expectations for `/hooks`.

## Git Flow, docs, and PR notes

Follow standard Git Flow:

- `main` is stable release.
- `develop` is day-to-day integration; verify remote branch names before branch automation.
- `feature/<slug>` starts from `develop` and merges back to `develop` by PR.
- `release/<version>` starts from `develop` and merges to both `main` and `develop`.
- `hotfix/<slug>` starts from `main` and merges to both `main` and `develop`.
- Do not commit or push directly to `main` or `develop`.

The root README is the marketplace overview; plugin READMEs are user-facing install/validation docs; localized `i18n/` files should stay aligned for public-facing changes.

PRs should report the affected plugin, exact validation commands, and hook/security impact when command hooks or executable hook scripts change.
