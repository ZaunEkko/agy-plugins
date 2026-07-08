# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a personal Antigravity plugin marketplace, not an application/library with a central build. It packages reusable Antigravity skills, hooks, and output-style behavior so they can be installed through `agy-plugins-cli` / `agy-plugins`.

The current tracked plugin content lives directly under top-level plugin directories:

- `commit-commands/` — markdown-only Antigravity skills for `$commit`, `$commit-push-pr`, and `$clean-gone`.
- `explanatory-output-style/` — a hook-backed output style plugin with a Python hook plus a markdown skill.
- `docs/<plugin>/README.md` — primary plugin documentation.
- `i18n/<locale>/...` — localized mirrors of root and plugin docs.

This checkout uses top-level plugin directories rather than a `plugins/` wrapper. Verify actual paths before adding files or updating commands, and do not introduce a `plugins/` wrapper unless the task is explicitly a layout migration.

## Commands

There is no repository-wide package manager config, build command, lint command, or CI test runner currently tracked.

Use focused validation based on the changed plugin:

```bash
# Validate the Python hook syntax
python -m py_compile explanatory-output-style/hooks/session_start.py

# Exercise the hook and inspect that it prints valid JSON for Antigravity
python explanatory-output-style/hooks/session_start.py

# Validate hook configuration JSON
python -m json.tool explanatory-output-style/hooks/hooks.json

# Run Python unittest discovery if a tests/ tree exists or is added
agy-plugin marketplace list

# Run one unittest module/test when tests exist
python -m json.tool explanatory-output-style/hooks/hooks.json
python -m json.tool explanatory-output-style/hooks/hooks.json.TestClass.test_method

# Smoke-check Antigravity can see installed marketplace plugins, when agy is available
agy-plugin marketplace list
```

Installation commands documented for users:

```bash
npm install -g agy-plugins-cli
agy-plugin marketplace add ZaunEkko/agy-plugins
agy-plugin add explanatory-output-style@zaunekko
agy-plugin add commit-commands@zaunekko
```

## Architecture notes

### Skill plugins are markdown contracts

`commit-commands` has no executable implementation. The skill behavior is encoded in each `SKILL.md` frontmatter and workflow text:

- `name` is the slash/skill identity.
- `description` controls when Antigravity should select the skill automatically.
- The workflow and boundary sections are product behavior, not prose-only docs.

Preserve the explicit triggering boundaries: `$commit` is commit-only, `$commit-push-pr` requires explicit PR intent, and `$clean-gone` is destructive branch/worktree cleanup that must only run on explicit user request.

### Hook plugins combine JSON config with executable output

`explanatory-output-style/hooks/hooks.json` registers a `PreInvocation` command hook that runs `python hooks/session_start.py` relative to the installed plugin. The Python hook prints JSON containing an `injectSteps` array with an `ephemeralMessage` that injects explanatory output-style instructions.

When changing hook behavior, keep the hook output machine-readable JSON. Native hooks installed via `agy plugin install` are dynamically mounted and do not appear in the TUI `/hooks` menu. Use `agy plugin disable <plugin>` to manage them.

### Documentation is part of the product surface

The root `README.md` is the marketplace overview and plugin router. Per-plugin docs explain installation, trust/review steps, paths, and validation. Localized docs under `i18n/en`, `i18n/ja`, `i18n/ko`, and `i18n/zh-TW` mirror user-facing content; update them when changing public docs or installation instructions.

## Git Flow, contribution, and PR expectations

Follow the standard Git Flow model for branch work:

- `main` is the stable release branch.
- `develop` is the day-to-day integration branch in this checkout. Verify the real remote branch names before creating automation or PRs.
- `feature/<slug>` branches start from `develop` and merge back into `develop` by PR.
- `release/<version>` branches start from `develop`, then merge into both `main` and `develop` when released.
- `hotfix/<slug>` branches start from `main`, then merge into both `main` and `develop`.
- Do not commit or push directly to `main` or `develop`; use PRs and wait for required checks.

The PR template asks for language, scope, validation commands per affected plugin, and hook/security impact. For hook or command changes, include the concrete validation run and explain any change in behavior.
