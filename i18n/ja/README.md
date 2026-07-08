<div align="center">

# 🧩 Antigravity Plugins

### Antigravity ワークフロー向けの個人マーケットプレイス

*便利な plugins、skills、hooks、出力スタイルを、他の人もインストールできる形でまとめます。*

[简体中文](../../README.md) · [English](../en/README.md) · [繁體中文](../zh-TW/README.md) · [日本語](README.md) · [한국어](../ko/README.md)

</div>

---

## ✨ このリポジトリについて

このリポジトリは Antigravity 向けの個人ワークフローマーケットプレイスです。再利用できる Antigravity プラグイン、skills、hooks、起動コンテキスト、出力スタイル、開発支援フローをまとめます。

## 📦 現在の内容

| プラグイン | 種類 | 説明 | ドキュメント |
|------------|------|------|--------------|
| explanatory-output-style | Plugin + SessionStart Hook | Claude Code 公式の explanatory-output-style 体験を Antigravity に適配します。 | [プラグイン docs](docs/explanatory-output-style/README.md) |
| commit-commands | Plugin + Skills | Anthropic 原版の commit、commit-push-pr、gone ブランチの force cleanup を提供します。 | [プラグイン docs](docs/commit-commands/README.md) |

## 🚀 クイックスタート

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add explanatory-output-style@zaunekko
agy plugin add commit-commands@zaunekko
```

command hook を含むプラグインは、初回利用前に Antigravity で確認して trust してください。

```text
/hooks
```

## 📚 プラグイン docs

- [explanatory-output-style](docs/explanatory-output-style/README.md): 機能、インストール、hook の trust、ローカル検証。
- [commit-commands](docs/commit-commands/README.md): commit、PR 公開、ブランチ整理、安全制約、ローカル検証。

## ⚠️ Trust & Safety

- インストール前にプラグイン説明を確認してください。
- `/hooks` で command hook を確認してください。
- hook を変更したら再度 trust してください。
- commit、push、ブランチ削除を行う skill を起動する前に、リポジトリの状態を確認してください。
- API key、token、パスワード、マシン固有パスを hook 出力に含めないでください。

## 📄 ライセンス

このプロジェクトは [MIT License](../../LICENSE) で公開されています。

## 🤝 コミュニティ

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
