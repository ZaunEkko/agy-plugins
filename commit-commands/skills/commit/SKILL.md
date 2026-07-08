---
name: commit-commands
description: A skill to assist with writing semantic Git commit messages. Includes automatic signatures.
---

# Commit Commands Skill

When a user asks you to write a commit message or commit their changes, you should format the commit message according to the `commit.rule.json`.

**Important Requirements:**
1. Analyze the `git diff` or the changes provided by the user to understand what has been modified.
2. Formulate a short, descriptive subject line following conventional commits format (e.g. `feat:`, `fix:`, `refactor:`, `docs:`).
3. Provide a clear and concise body explaining the context and the reason for the change, if necessary.
4. **Mandatory**: As per the rules, always end the commit message with `Co-authored-by: gemini-code-assist[bot] <176961590+gemini-code-assist[bot]@users.noreply.github.com>`.

Example format:
```
feat: add marketplace source management

Implemented the config manager to save marketplace repositories locally.

Co-authored-by: gemini-code-assist[bot] <176961590+gemini-code-assist[bot]@users.noreply.github.com>
```
