# Contributing

[简体中文](../../CONTRIBUTING.md) · [English](CONTRIBUTING.md) · [繁體中文](../zh-TW/CONTRIBUTING.md) · [日本語](../ja/CONTRIBUTING.md) · [한국어](../ko/CONTRIBUTING.md)

Thank you for your interest in `agy-plugins`. This repository maintains Antigravity-oriented plugins, hooks, skills, presets, and related documentation.

## Branch and contribution flow

This repository uses Git Flow:

- `main`: stable release branch.
- `dev`: daily integration branch.
- `feature/*`: features, documentation, and plugin changes. Branch from `dev`, then merge back through a Pull Request.
- `release/*`: release preparation. Branch from `dev`, then merge into both `main` and `dev`.
- `hotfix/*`: urgent fixes. Branch from `main`, then merge into both `main` and `dev`.

Do not push directly to `main` or `dev`. Both branches are protected; changes should be merged through Pull Requests after required checks pass.

## Repository structure

New plugins should generally follow this layout:

```text
plugins/<plugin-name>/
├── .agy-plugin/
│   └── plugin.json
└── ...

docs/<plugin-name>/
└── README.md
```

- `plugins/<plugin-name>/` contains installable plugin files.
- `docs/<plugin-name>/README.md` contains installer- and user-facing plugin documentation.
- The root `README.md` should stay as a repository overview and plugin documentation router.
- Do not commit the local Claude Code initialization file `CLAUDE.md`; it is ignored by `.gitignore`.

## Plugin documentation requirements

Each plugin document should explain the problem solved, installation steps, enablement or trust steps, key file paths, and maintainer validation. If the plugin includes command hooks, document `/hooks` review and trust.

## Validation requirements

Run validation for the plugins affected by your change. Do not rely on one fixed command set for every PR.

General rules:

- Python hook changes: run `python -m py_compile <hook-script>` and execute the hook script directly to confirm it emits valid JSON.
- Hook configuration changes: confirm `hooks.json` is valid JSON and review command / commandWindows for safety, readability, and cross-platform behavior.
- Manifest changes: confirm `.agy-plugin/plugin.json` is valid JSON and matches the plugin name, version, description, and marketplace entry.
- Behavior changes: run that plugin's tests. If tests do not exist, add focused tests or explain why they were not added in the PR.
- Documentation changes: check links, paths, and installation commands.
- New plugins: confirm the marketplace can discover the plugin, and document installation and trust steps.

Current maintainer validation example for `explanatory-output-style`:

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
```

These commands are examples for that plugin only. New plugins should define their own validation steps in documentation or tests.

## Hook and security requirements

- Do not write API keys, tokens, passwords, private keys, or machine-specific paths into hook output, manifests, tests, or documentation.
- Do not introduce opaque command strings that are hard to review.
- Preserve necessary cross-platform support. If Windows and Unix commands differ, document both clearly.
- After adding or modifying a command hook, explain the security impact and what users need to review / trust in the PR.

## Pull Request requirements

PR descriptions should include the change summary, validation commands run, whether hook / manifest / marketplace metadata changed, hook / security impact, and reasons for any skipped validation.
