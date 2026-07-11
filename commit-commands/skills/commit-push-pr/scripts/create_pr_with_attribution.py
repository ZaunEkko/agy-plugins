"""
create_pr_with_attribution.py — Antigravity PR Attribution Wrapper

Accepts the PR body on stdin and `gh pr create` arguments after `--`.
Appends the Antigravity attribution footer, creates the PR via `--body-file`,
reads the body back with `gh pr view`, repairs it once if needed, and fails
unless the footer is the exact final non-empty line.

Adapted from codex-plugins' create_pr_with_attribution.py for the
Antigravity ecosystem.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


FOOTER = "Generated with [Antigravity](https://antigravity.google/product)"
LEGACY_FOOTERS = {
    "Generated with Antigravity assistance.",
    "Generated with Antigravity",
}
PR_URL_PATTERN = re.compile(r"https?://[^/\s]+/[^/\s]+/[^/\s]+/pull/\d+")


def final_nonempty_line(body):
    for line in reversed(body.splitlines()):
        if line.strip():
            return line.strip()
    return None


def render_body(body):
    lines = body.rstrip().splitlines()
    if lines and lines[-1].strip() in LEGACY_FOOTERS | {FOOTER}:
        lines.pop()

    content = "\n".join(lines).rstrip()
    return f"{content}\n\n{FOOTER}\n" if content else f"{FOOTER}\n"


def run_gh(arguments):
    try:
        return subprocess.run(
            ["gh", *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError as error:
        raise SystemExit("commit-commands: GitHub CLI `gh` is unavailable") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or str(error)).strip()
        raise SystemExit(f"commit-commands: gh command failed: {detail}") from error


def pull_request_url(output):
    matches = PR_URL_PATTERN.findall(output)
    if not matches:
        raise SystemExit("commit-commands: `gh pr create` did not return a pull request URL")
    return matches[-1]


def read_pull_request(url):
    result = run_gh(["pr", "view", url, "--json", "body,url"])
    try:
        pull_request = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit("commit-commands: `gh pr view` returned invalid JSON") from error

    if not isinstance(pull_request, dict):
        raise SystemExit("commit-commands: `gh pr view` returned an invalid pull request")
    return pull_request


def create_pull_request(body, gh_arguments):
    rendered_body = render_body(body)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            suffix=".md",
            delete=False,
        ) as stream:
            stream.write(rendered_body)
            temporary_path = Path(stream.name)

        result = run_gh(
            ["pr", "create", *gh_arguments, "--body-file", str(temporary_path)]
        )
        url = pull_request_url(result.stdout)
        pull_request = read_pull_request(url)

        if final_nonempty_line(pull_request.get("body") or "") != FOOTER:
            run_gh(["pr", "edit", url, "--body-file", str(temporary_path)])
            pull_request = read_pull_request(url)

        if final_nonempty_line(pull_request.get("body") or "") != FOOTER:
            raise SystemExit(
                "commit-commands: pull request body is missing the required Antigravity attribution"
            )

        return pull_request.get("url") or url
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(
        description="Create a pull request whose body ends with Antigravity attribution."
    )
    parser.add_argument("gh_arguments", nargs=argparse.REMAINDER)
    arguments = parser.parse_args(argv)
    gh_arguments = list(arguments.gh_arguments)
    if gh_arguments and gh_arguments[0] == "--":
        gh_arguments.pop(0)

    forbidden = {"--body", "-b", "--body-file", "-F"}
    for argument in gh_arguments:
        if (
            argument in forbidden
            or argument.startswith("--body=")
            or argument.startswith("--body-file=")
        ):
            parser.error("pass the pull request body on stdin; do not supply --body or --body-file")
    return gh_arguments


def main():
    gh_arguments = parse_arguments()
    print(create_pull_request(sys.stdin.read(), gh_arguments))


if __name__ == "__main__":
    main()
