<div align="center">

# 🧩 Antigravity Plugins

### 个性化 Antigravity 工作流市场

*把顺手的 plugins、skills、hooks 和提示词风格，打包成别人也能一键安装的能力*

[简体中文](README.md) · [English](i18n/en/README.md) · [繁體中文](i18n/zh-TW/README.md) · [日本語](i18n/ja/README.md) · [한국어](i18n/ko/README.md)

[![Antigravity](https://img.shields.io/badge/Antigravity-Workflow-111827.svg)]()
[![Marketplace](https://img.shields.io/badge/Marketplace-ZaunEkko-orange.svg)]()
[![Plugins](https://img.shields.io/badge/Includes-Plugins-blue.svg)]()
[![Hooks](https://img.shields.io/badge/Supports-Hooks-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ 这个仓库是什么

这是一个专为 **Google Antigravity (agy)** 打造的个人工作流 marketplace，用来持续沉淀可复用的 Antigravity 个性化能力。
本项目摒弃了繁琐的配置文件，完全采用了高度语义化的 `SKILL.md` 和底层生命周期 Hooks 来严格约束 AI 的行为边界与工作流节点。

目标是把平时用着顺手的 Antigravity 配置打包起来，让大家通过 CLI 能够一键安装、静默更新和全局复用。

## 🧰 收录范围

| 类型 | 说明 |
|------|------|
| Skills | 可复用的任务工作流，让 Antigravity 在特定场景下按固定方法做事（完全摒弃繁琐的 rule.json，依赖原生 markdown 驱动）。 |
| Hooks | 在 Antigravity 生命周期事件中自动运行脚本，例如 `PreInvocation`，用于全局上下文注入等动态拦截。 |

## 📦 当前内容

| 插件 | 类型 | 说明 | 文档 |
|------|------|------|------|
| explanatory-output-style | Hook | 通过拦截 Session 启动生命周期，把原生的解释型协作体验（Insight 框）自动注入到 Antigravity 中。 | [插件文档](docs/explanatory-output-style/README.md) |
| commit-commands | Skills | 提供极为严谨的 `commit`、`commit-push-pr` 与 `clean-gone` Git 分支工作流，并强制携带 Antigravity 联合开发者签名。 | [插件文档](docs/commit-commands/README.md) |

## 🚀 快速开始

本项目依赖专门构建的 Antigravity 插件管理工具 `agy-plugins-cli`。

### 1. 安装 CLI
全局安装我们的包管理器：
```bash
npm install -g agy-plugins-cli
```

### 2. 绑定当前仓库并安装插件
通过 CLI 沉浸式安装您需要的插件：
```bash
# 绑定 ZaunEkko 的本插件仓库
agy-plugin marketplace add ZaunEkko/agy-plugins

# 启动交互式 TUI 面板，一键勾选所需插件（如 explanatory-output-style）
agy-plugin marketplace list
```

如果不想使用交互式面板，也可以用传统的命令式语法（支持 `@namespace` 定位）：
```bash
agy-plugin add explanatory-output-style@zaunekko
agy-plugin add commit-commands@zaunekko
```

## 🎯 插件使用方式

**explanatory-output-style**：
安装后全局生效。每次与 Antigravity 对话时，它都会自动在底层触发 Hook，并以精美的 `+--- ★ Insight ---+` 风格向您解释代码逻辑，非常适合代码学习与架构探讨。

**commit-commands**：
在终端直接通过 slash 命令呼叫，Antigravity 将严格遵循工作流边界执行：
- `$commit`: 一键本地提交并签名。
- `$commit-push-pr`: 开发完毕后自动开新分支、提交、推送并使用 `gh` CLI 提 PR。
- `$clean-gone`: 自动检索本地标记为 `[gone]` 的上游已删分支，并暴力清场工作区。

*(注：涉及危险操作的 Skill（如 `clean-gone`）在删除分支前必须由用户人工审计确认。)*

## 📚 插件架构

本仓库采用纯粹的 Antigravity 兼容结构：

```text
agy-plugins/
├── commit-commands/
│   └── skills/
│       ├── commit/SKILL.md
│       ├── commit-push-pr/SKILL.md
│       └── clean-gone/SKILL.md
├── explanatory-output-style/
│   ├── hooks/
│   │   ├── hooks.json
│   │   └── session_start.py
│   └── skills/
│       └── explanatory-output.md
```
所有的工作流逻辑都死死地钉在 `SKILL.md` 里，没有任何过度设计的周边配置文件！

## ⚠️ Trust & Safety

- 包含 command hook（如 Python 脚本）的插件在首次安装后，请留意本地安全提示。
- 切勿在 Hook 中输出任何明文敏感 Token。
- 触发自动提交或分支清理操作前，确保当前工作区没有未保存的贵重代码。

## 📄 许可证

本项目使用 [MIT License](LICENSE) 开源。

## 🤝 社区与贡献

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
