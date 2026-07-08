<div align="center">

# 🧩 Antigravity Plugins

### 個人化 Antigravity 工作流程市集

*把順手的 plugins、skills、hooks 和提示詞風格，打包成其他人也能安裝的能力*

[简体中文](../../README.md) · [English](../en/README.md) · [繁體中文](README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md)

</div>

---

## ✨ 這個倉庫是什麼

這是一個面向 Antigravity 的個人工作流程 marketplace，用來沉澱可重複使用的 Antigravity 個人化能力：插件、skills、hooks、啟動上下文、輸出風格和開發輔助流程。

## 📦 目前內容

| 插件 | 類型 | 說明 | 文件 |
|------|------|------|------|
| explanatory-output-style | Plugin + SessionStart Hook | 將 Claude Code 官方 explanatory-output-style 體驗適配到 Antigravity。 | [插件文件](docs/explanatory-output-style/README.md) |
| commit-commands | Plugin + Skills | 依 Anthropic 原版提供 commit、commit-push-pr 與 gone 分支 force 清理流程。 | [插件文件](docs/commit-commands/README.md) |

## 🚀 快速開始

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add explanatory-output-style@zaunekko
agy plugin add commit-commands@zaunekko
```

首次使用包含 command hook 的插件前，請在 Antigravity 中審查並信任：

```text
/hooks
```

## 📚 插件文件

- [explanatory-output-style](docs/explanatory-output-style/README.md)：功能、安裝、hook 信任與本地驗證說明。
- [commit-commands](docs/commit-commands/README.md)：提交、PR 發布、分支清理、安全限制與本機驗證說明。

## ⚠️ Trust & Safety

- 安裝前閱讀插件說明。
- 在 `/hooks` 中審查 command hook。
- 修改 hook 後重新 trust。
- 觸發會提交、推送或刪除分支的 skill 前，先檢查目前倉庫狀態。
- 不要把 API key、token、密碼或機器專屬路徑寫進 hook 輸出。

## 📄 授權

本專案使用 [MIT License](../../LICENSE) 開源。

## 🤝 社群與貢獻

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
