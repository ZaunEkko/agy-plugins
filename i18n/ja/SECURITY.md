# Security Policy

[简体中文](../../SECURITY.md) · [English](../en/SECURITY.md) · [繁體中文](../zh-TW/SECURITY.md) · [日本語](SECURITY.md) · [한국어](../ko/SECURITY.md)

## サポート範囲

現在は `main` ブランチの最新リリース内容と、`dev` ブランチで準備中のプラグイン変更をサポートします。

## セキュリティ問題の報告

このリポジトリに関するセキュリティ問題を見つけた場合、悪用可能な詳細、token、API key、パスワード、秘密鍵、個人情報を公開 issue に投稿しないでください。

可能であれば GitHub 経由でメンテナーへ非公開で連絡してください。公開 issue を作成する場合は、機密情報を含めず、非公開での連絡が必要であることだけを書いてください。

## インストール時の安全確認

command hook を含む Antigravity プラグインをインストールする前に、Antigravity で次を実行してください。

```text
/hooks
```

実際のコマンドを確認してから trust してください。未知の hook を盲目的に信頼せず、API key、token、マシン固有のパスをプラグイン出力に書き込まないでください。
