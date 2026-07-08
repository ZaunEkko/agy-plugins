# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` は [Anthropic 公式原版](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) の 3 つの slash command を Antigravity ネイティブ skill に適配します。

```text
$commit
$commit-push-pr
$clean-gone
```

ワークフロー手順は原版に従います。Antigravity 固有の差分はネイティブ skill 構造、明示的な意図による自動選択、`$skill-name` 呼び出し、Antigravity attribution だけです。

## インストール

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add commit-commands@zaunekko
```

インストールまたは更新後は、新しい Antigravity thread を開いてください。

## 自動選択の例

- 「この変更を commit して」で `commit` を選択できます。
- 「commit、push、PR 作成をして」で `commit-push-pr` を選択できます。
- 「gone ブランチをすべて整理して」で `clean-gone` を選択できます。
- 「実装が完了した」だけでは Git の副作用を実行しません。

## `$commit`

`git status`、`git diff HEAD`、現在のブランチ、最近 10 件の commit を確認し、現在の変更を stage して 1 つの commit を作成します。

```text
Co-authored-by: Antigravity <noreply@openai.com>
```

push や PR 作成は行わず、変更がない場合は空 commit も作成しません。

## `$commit-push-pr`

現在の status、diff、branch を確認します。現在のブランチが正確に `main` の場合だけ新しいブランチを作り、1 つの commit を作成して `origin` へ push し、`gh pr create` で PR を開きます。

明示的な PR 意図が必要です。原版と同様に、新しい commit なしで公開する経路や、`main` 以外のブランチ名をポリシーに合わせて自動移行する処理はありません。

GitHub CLI のインストールとログイン、および `origin` remote が必要です。

## `$clean-gone`

`git branch -v` と `git worktree list` で `[gone]` ブランチを探します。各候補について、関連する非 main worktree を `git worktree remove --force` で強制削除し、続けて `git branch -D` でブランチを強制削除します。

これは原版に合わせた破壊的な動作です。fetch、merge 検証、worktree の clean 確認、ignored ファイルの保護、統合ブランチ規則は追加しません。実行前にリポジトリ状態を確認してください。

## ローカル検証

```bash
python -m unittest discover -s tests
agy plugin list
```
