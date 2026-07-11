"""
model_context.py — Antigravity Model Attribution Hook

Triggered on SessionStart. Reads the current model from the agy state
payload (stdin) or falls back to ~/.gemini/antigravity-cli/settings.json.
Injects the model name into the agent's conversation context so that
$commit and $commit-push-pr can write accurate Model: lines.
"""

import json
import os
import sys


SETTINGS_PATH = os.path.expanduser(r"~/.gemini/antigravity-cli/settings.json")


def read_model_from_state():
    """Read model from agy's stdin state payload."""
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
            if raw.strip():
                state = json.loads(raw)
                model = state.get("model")
                if isinstance(model, dict):
                    return model.get("display_name") or model.get("id")
                if isinstance(model, str) and model:
                    return model
    except Exception:
        pass
    return None


def read_model_from_settings():
    """Fallback: read model from settings.json."""
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("model")
    except Exception:
        return None


def build_context(model):
    if not model:
        return (
            "commit-commands runtime metadata for this turn:\n"
            "- The active Antigravity model is unavailable.\n"
            "- If `$commit` or `$commit-push-pr` runs, stop before staging or committing "
            "and report that model attribution cannot be resolved."
        )

    return (
        "commit-commands runtime metadata for this turn:\n"
        f"- Active Antigravity model: `{model}`.\n"
        "- If `$commit` or `$commit-push-pr` runs, write exactly "
        f"`Model: {model}` in its attribution block.\n"
        "- Ignore this metadata for every other task."
    )


def main():
    model = read_model_from_state() or read_model_from_settings()

    print(
        json.dumps(
            {
                "injectSteps": [
                    {
                        "ephemeralMessage": build_context(model)
                    }
                ]
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
