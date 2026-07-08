# Contributing

[简体中文](CONTRIBUTING.md) · [English](i18n/en/CONTRIBUTING.md) · [繁體中文](i18n/zh-TW/CONTRIBUTING.md) · [日本語](i18n/ja/CONTRIBUTING.md) · [한국어](i18n/ko/CONTRIBUTING.md)

感谢你对 `agy-plugins` 的关注。这个仓库主要维护面向 Antigravity 的插件、hooks、skills、预设和相关文档。

## 分支与提交流程

本仓库使用 Git Flow：

- `main`：稳定发布分支。
- `dev`：日常集成分支。
- `feature/*`：新功能、文档、插件改动，从 `dev` 拉出，完成后通过 PR 合回 `dev`。
- `release/*`：发布准备，从 `dev` 拉出，完成后合入 `main` 和 `dev`。
- `hotfix/*`：紧急修复，从 `main` 拉出，完成后合入 `main` 和 `dev`。

不要直接推送到 `main` 或 `dev`。这两个分支受保护，改动应通过 Pull Request 合并，并等待必需检查通过。

## 仓库结构约定

新增插件时，优先遵循以下结构：

```text
plugins/<plugin-name>/
├── .agy-plugin/
│   └── plugin.json
└── ...

docs/<plugin-name>/
└── README.md
```

- `plugins/<plugin-name>/` 放可安装插件内容。
- `docs/<plugin-name>/README.md` 放面向安装者和使用者的插件说明。
- 根目录 `README.md` 只做仓库总览和插件文档路由。
- 不要提交本地 Claude Code 初始化文件 `CLAUDE.md`；它已被 `.gitignore` 忽略。

## 插件文档要求

每个插件文档至少说明：插件解决什么问题、安装方式、启用或信任步骤、主要文件路径、维护者如何验证。包含 command hook 时，需要说明 `/hooks` 审查和 trust。

## 验证要求

请根据本次改动影响的插件运行对应验证，不要只跑固定命令。

一般规则：

- 修改 Python hook：至少运行 `python -m py_compile <hook-script>`，并直接执行 hook 脚本确认输出是有效 JSON。
- 修改 hook 配置：确认 `hooks.json` 是有效 JSON，并审查 command / commandWindows 是否仍然安全、可读、跨平台。
- 修改插件 manifest：确认 `.agy-plugin/plugin.json` 是有效 JSON，且插件名、版本、描述和 marketplace 入口一致。
- 修改插件行为：运行该插件对应测试；如果没有测试，应补充聚焦测试或在 PR 中说明未补测试的原因。
- 修改文档：检查链接、路径和安装命令是否仍然准确。
- 新增插件：确认 marketplace 能发现该插件，并在文档中写明安装和信任步骤。

当前 `explanatory-output-style` 插件的维护者验证示例：

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
```

这些命令只是该插件的示例；新增插件应在自己的文档或测试中定义对应验证方式。

## Hook 与安全要求

- 不要在 hook 输出、manifest、测试或文档中写入 API key、token、密码、私钥或机器专属路径。
- 不要引入不透明或难以审查的命令字符串。
- 保留必要的跨平台支持；Windows 和 Unix 命令不同时，应分别写清楚。
- 新增或修改 command hook 后，必须在 PR 中说明安全影响和用户需要 review / trust 的内容。

## Pull Request 要求

PR 描述应包含变更内容、已运行的验证命令、是否修改 hook / manifest / marketplace 元数据、Hook / 安全影响，以及未运行验证的原因。
