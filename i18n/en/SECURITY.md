# Security Policy

[简体中文](../../SECURITY.md) · [English](SECURITY.md) · [繁體中文](../zh-TW/SECURITY.md) · [日本語](../ja/SECURITY.md) · [한국어](../ko/SECURITY.md)

## Supported scope

The latest released content on `main` is supported, along with plugin changes being prepared on `dev`.

## Reporting security issues

If you find a security issue in this repository, do not post exploit details, tokens, API keys, passwords, private keys, or personal sensitive information in a public issue.

Please contact the maintainer privately through GitHub when possible, or open a public issue without sensitive details and ask to continue privately.

Relevant issues include:

- Unexpected command execution risk in command hooks.
- Sensitive data emitted by hook output.
- Documentation or examples that may lead users to leak credentials.
- Marketplace or manifest entries pointing to the wrong or untrusted path.

## Safety tips for installers

Before installing a Antigravity plugin that includes command hooks, run:

```text
/hooks
```

Review the actual command before trusting it. Do not blindly trust unknown hooks, and do not write API keys, tokens, or machine-specific paths into plugin output.
