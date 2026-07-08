# explanatory-output-style

[简体中文](../../../../docs/explanatory-output-style/README.md) · [English](../../../en/docs/explanatory-output-style/README.md) · [繁體中文](../../../zh-TW/docs/explanatory-output-style/README.md) · [日本語](README.md) · [한국어](../../../ko/docs/explanatory-output-style/README.md)

`explanatory-output-style` は、Antigravity セッションで説明型の出力スタイルを有効にする Antigravity プラグインです。

Claude Code 公式 [`explanatory-output-style`](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style) プラグインの体験を参考にしています。`SessionStart` hook でセッション開始時に追加の指示を注入し、モデルがコードを書いたり変更したりするときに、現在のコードベースに沿った短い Insight を補足できるようにします。

## どんな場面に向いているか

- Antigravity に最終的な変更だけでなく、なぜその実装にしたのかも説明してほしい。
- チームで同じ「作業しながら説明する」協働スタイルを共有したい。
- 出力スタイルを各プロジェクトにプロンプトとしてコピーするのではなく、インストール可能なプラグインとして配布したい。

## Claude Code 公式プラグインとの関係

Claude Code 公式プラグインは `SessionStart` hook を使って、セッション開始時に説明型出力の指示を追加します。このリポジトリの実装は、その動作を Antigravity プラグインシステム向けに適配したものです。

- Antigravity プラグイン manifest: `plugins/explanatory-output-style/.agy-plugin/plugin.json`
- Antigravity hook 設定: `plugins/explanatory-output-style/hooks/hooks.json`
- Antigravity が期待する JSON payload を出力する Python hook: `hookSpecificOutput.additionalContext`
- クロスプラットフォームでインストールしやすいように Windows / Unix 両方の hook command を保持

## 注入後の協働動作

注入されたコンテキストは Antigravity に次を求めます。

1. コードを書く前後、または変更する前後に短い Insight を提供する。
2. 現在のコードベースにおける実装選択、プロジェクト規約、トレードオフに焦点を当てる。
3. 一般的なプログラミング概念を長いチュートリアルとして説明しない。
4. 狭いターミナルでも崩れにくい出力ブロック形式を使い、折り返しや右枠のずれを減らす。

現在の Insight ブロック例:

```text
`+-------------------- ★ Insight --------------------+`
| 現在の実装選択を説明する短い要点を 2-3 個
`+---------------------------------------------------+`
```

bullet 行には左側の `|` だけを残し、右側の枠は追加しません。これにより、ターミナルで自動折り返しが発生しても枠がずれにくくなります。

## インストールと有効化

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add explanatory-output-style@zaunekko
```

command hook を含むプラグインは、初回実行前に Antigravity で確認して trust する必要があります。

```text
/hooks
```

確認ポイント:

- `hooks/hooks.json` で実際に実行される command。
- `hooks/session_start.py` が期待された JSON のみを出力するか。
- hook 出力に API key、token、マシン固有のパス、その他の機密情報が含まれていないか。

## ローカル検証

リポジトリのルートから実行します。

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
agy plugin list
```

最初の 3 つは Python 構文、hook JSON payload、プラグイン出力形式を検証します。`agy plugin list` は Antigravity が marketplace プラグインを検出できることを確認するために使います。
