# commit-commands

[简体中文](README.md) · [English](../../i18n/en/docs/commit-commands/README.md) · [繁體中文](../../i18n/zh-TW/docs/commit-commands/README.md) · [日本語](../../i18n/ja/docs/commit-commands/README.md) · [한국어](../../i18n/ko/docs/commit-commands/README.md)

`commit-commands` 将 [Anthropic 官方原版](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) 的三个 slash command 适配为原生 Antigravity skill：

```text
$commit
$commit-push-pr
$clean-gone
```

工作流步骤以原版为准。Antigravity 适配差异只包括原生 skill 结构、明确意图的自动选择、`$skill-name` 显式入口和 Antigravity attribution。

## 安装与启用

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add commit-commands@zaunekko
```

安装或更新后请新开 Antigravity thread，使新的 skill 元数据进入会话。

## 自动选择示例

- “提交这些改动”可以自动选择 `commit`。
- “提交这些改动、推送并创建 PR”可以自动选择 `commit-push-pr`。
- “清理所有 gone 分支”可以自动选择 `clean-gone`。
- “功能已经完成”不会自行触发任何 Git 副作用。

## `$commit`

检查 `git status`、`git diff HEAD`、当前分支和最近十条提交，暂存当前改动并创建一个 commit。生成的提交会追加：

```text
Co-authored-by: Antigravity <noreply@openai.com>
```

该 skill 不会推送或创建 PR；没有改动时也不会创建空提交。

## `$commit-push-pr`

检查当前状态、diff 和分支。只有当前分支恰好是 `main` 时才创建新分支，然后创建一个 commit、推送到 `origin`，并使用 `gh pr create` 创建 PR。

该 skill 只在用户明确要求 PR 时触发。与原版一样，它不支持“没有新 commit 也发布 PR”，也不会因为其他分支名称不符合仓库策略而自动迁移分支。

需要已安装并登录 GitHub CLI，仓库还需要配置 `origin` remote。

## `$clean-gone`

使用 `git branch -v` 和 `git worktree list` 查找标记为 `[gone]` 的分支。对每个候选项，先使用 `git worktree remove --force` 强制移除关联的非主 worktree，再使用 `git branch -D` 强制删除分支。

这是与原版一致的破坏性行为：不会自动 fetch，不验证是否已合并，不检查 worktree 是否干净，也不保护 ignored 文件或集成分支。调用前必须自行确认仓库状态。

## 本地验证

```bash
python -m unittest discover -s tests
agy plugin list
```
