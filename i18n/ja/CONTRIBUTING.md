# Contributing

[简体中文](../../CONTRIBUTING.md) · [English](../en/CONTRIBUTING.md) · [繁體中文](../zh-TW/CONTRIBUTING.md) · [日本語](CONTRIBUTING.md) · [한국어](../ko/CONTRIBUTING.md)

`agy-plugins` に関心を持っていただきありがとうございます。このリポジトリでは、Antigravity 向けのプラグイン、hooks、skills、プリセット、関連ドキュメントを管理しています。

## ブランチと貢献フロー

このリポジトリは Git Flow を使用します。

- `main`: 安定リリースブランチ。
- `dev`: 日常的な統合ブランチ。
- `feature/*`: 新機能、ドキュメント、プラグイン変更。`dev` から分岐し、Pull Request で `dev` に戻します。
- `release/*`: リリース準備。`dev` から分岐し、完了後 `main` と `dev` にマージします。
- `hotfix/*`: 緊急修正。`main` から分岐し、完了後 `main` と `dev` にマージします。

`main` または `dev` へ直接 push しないでください。両方のブランチは保護されており、変更は Pull Request と必須チェックを通してマージします。

## リポジトリ構成

新しいプラグインは基本的に次の構成にしてください。

```text
plugins/<plugin-name>/
├── .agy-plugin/
│   └── plugin.json
└── ...

docs/<plugin-name>/
└── README.md
```

- `plugins/<plugin-name>/` にはインストール可能なプラグイン内容を置きます。
- `docs/<plugin-name>/README.md` にはインストール者・利用者向けの説明を置きます。
- ルート `README.md` はリポジトリ概要とプラグインドキュメントへの導線に留めます。
- ローカルの Claude Code 初期化ファイル `CLAUDE.md` はコミットしないでください。`.gitignore` で無視されています。

## プラグインドキュメント要件

各プラグインのドキュメントには、解決する問題、インストール方法、有効化または trust の手順、主要ファイルパス、メンテナー向け検証方法を含めてください。command hook を含む場合は、`/hooks` での確認と trust を説明してください。

## 検証要件

変更の影響を受けるプラグインに応じた検証を実行してください。すべての PR で固定のコマンドだけに依存しないでください。

一般ルール:

- Python hook の変更: `python -m py_compile <hook-script>` を実行し、hook スクリプトを直接実行して有効な JSON を出力することを確認します。
- hook 設定の変更: `hooks.json` が有効な JSON であることを確認し、command / commandWindows の安全性、可読性、クロスプラットフォーム性を確認します。
- manifest の変更: `.agy-plugin/plugin.json` が有効な JSON であり、プラグイン名、バージョン、説明、marketplace エントリと一致することを確認します。
- 振る舞いの変更: 対象プラグインのテストを実行します。テストがない場合は焦点を絞ったテストを追加するか、PR で追加しない理由を説明します。
- ドキュメント変更: リンク、パス、インストールコマンドを確認します。
- 新規プラグイン: marketplace がプラグインを検出できることを確認し、インストールと trust 手順をドキュメントに記載します。

現在の `explanatory-output-style` プラグインのメンテナー検証例:

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
```

これらのコマンドはこのプラグインの例です。新しいプラグインは、自身のドキュメントまたはテストで検証方法を定義してください。

## Hook とセキュリティ要件

- hook 出力、manifest、テスト、ドキュメントに API key、token、パスワード、秘密鍵、マシン固有のパスを書かないでください。
- レビューしにくい不透明なコマンド文字列を追加しないでください。
- 必要なクロスプラットフォーム対応を維持してください。Windows と Unix のコマンドが異なる場合は、それぞれ明確に記載します。
- command hook を追加または変更した場合、PR でセキュリティ影響とユーザーが review / trust すべき内容を説明してください。

## Pull Request 要件

PR の説明には、変更概要、実行した検証コマンド、hook / manifest / marketplace metadata の変更有無、Hook / セキュリティ影響、検証を省略した場合の理由を含めてください。
