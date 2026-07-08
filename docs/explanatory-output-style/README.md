# explanatory-output-style

[简体中文](README.md) · [English](../../i18n/en/docs/explanatory-output-style/README.md) · [繁體中文](../../i18n/zh-TW/docs/explanatory-output-style/README.md) · [日本語](../../i18n/ja/docs/explanatory-output-style/README.md) · [한국어](../../i18n/ko/docs/explanatory-output-style/README.md)

`explanatory-output-style` 是一个 Antigravity 插件，用来在 Antigravity 会话中启用解释型输出风格。

它参考 Claude Code 官方 [`explanatory-output-style`](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style) 插件的功能体验：通过 `SessionStart` hook 在会话开始时加入额外指导，让模型在写代码或修改代码时补充简短、贴近当前代码库的 Insight 说明。

## 适合什么场景

- 希望 Antigravity 不只给最终改动，也解释为什么这样实现。
- 希望团队共享同一套“边做边解释”的协作风格。
- 希望把输出风格作为可安装插件分发，而不是每个项目都复制提示词。

## 和 Claude Code 官方插件的关系

Claude Code 官方插件使用 `SessionStart` hook 在会话开始时加入解释型输出指导。这个仓库中的实现面向 Antigravity 插件系统重新适配：

- 使用 Antigravity 插件 manifest：`plugins/explanatory-output-style/.agy-plugin/plugin.json`
- 使用 Antigravity hook 配置：`plugins/explanatory-output-style/hooks/hooks.json`
- 使用 Python hook 输出 Antigravity 需要的 JSON payload：`hookSpecificOutput.additionalContext`
- 保留 Windows / Unix 两套 hook command，方便跨平台安装

## 注入后的协作效果

插件注入的上下文会要求 Antigravity：

1. 在写代码或修改代码前后提供简短 Insight。
2. 重点解释当前代码库里的实现选择、项目约定和取舍。
3. 避免泛泛而谈，不把通用编程概念写成长篇教程。
4. 使用适合窄终端的输出块格式，减少换行和右边框错位。

当前 Insight 块格式示例：

```text
`+-------------------- ★ Insight --------------------+`
| 说明当前实现选择的 2-3 条简短要点
`+---------------------------------------------------+`
```

bullet 行只保留左侧 `|`，不添加右侧边框，避免终端自动换行后出现边框错位。

## 安装与启用

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add explanatory-output-style@zaunekko
```

包含 command hook 的插件首次运行前需要在 Antigravity 中审查并信任：

```text
/hooks
```

审查重点：

- `hooks/hooks.json` 中实际执行的 command。
- `hooks/session_start.py` 是否只输出预期 JSON。
- hook 输出里不应包含 API key、token、机器专属路径或其他敏感信息。

## 本地验证

从仓库根目录运行：

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
agy plugin list
```

前三条分别验证 Python 语法、hook JSON payload 和插件输出格式；`agy plugin list` 用于确认 Antigravity 能发现 marketplace 插件。
