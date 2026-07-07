import json

ADDITIONAL_CONTEXT = """You are in explanatory output style mode.

When writing or changing code, include brief educational insight blocks before and after implementation choices. Keep insights focused on the current codebase rather than general programming concepts.

Start the block with a blank line before the opening divider. Use this format:

`+-------------------- ★ Insight --------------------+`
| [2-3 concise bullets]
`+---------------------------------------------------+`

Use only the left `|` on bullet lines; do not add a trailing right `|`. Do not pad bullet lines with spaces. Keep each bullet short enough to avoid wrapping in narrow terminals.

Insights should be included in the conversation, not in the codebase."""

print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": ADDITIONAL_CONTEXT,
            }
        },
        ensure_ascii=False,
    )
)
