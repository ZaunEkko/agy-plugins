# CLAUDE.md

This file is local Claude Code context for working on this repository. It is intentionally ignored by git because this repository is primarily a Antigravity plugin marketplace, and public project guidance should stay in `AGENTS.md`, `README.md`, and `docs/`.

## Repository purpose

This repository hosts reusable Antigravity plugins, hooks, skills, presets, and related documentation. Treat Antigravity compatibility and installability as the primary product surface.

## Source of truth

- Public contributor and maintenance guidance: `AGENTS.md`
- Marketplace overview and installation entry: `README.md`
- Per-plugin user documentation: `docs/<plugin-name>/README.md`
- Plugin packages: `plugins/<plugin-name>/`

Do not copy Claude-specific workflow assumptions into public Antigravity plugin files unless the user explicitly asks for them.

## Working notes

- Keep changes on Git Flow branches such as `feature/*`, not directly on `dev` for new features.
- Do not modify `plugins/*/.agy-plugin/plugin.json` unless the user explicitly asks; installed Antigravity plugin metadata may already be validated.
- For plugin documentation, prefer one README per plugin under `docs/<plugin-name>/README.md`; use the root `README.md` as the route into those docs.
- If adding or changing hooks, preserve cross-platform commands and run the validation commands documented in `AGENTS.md`.
- Do not commit this file.
