# Security Policy

[简体中文](../../SECURITY.md) · [English](../en/SECURITY.md) · [繁體中文](SECURITY.md) · [日本語](../ja/SECURITY.md) · [한국어](../ko/SECURITY.md)

## 支援範圍

目前支援 `main` 分支上的最新發布內容，以及正在 `dev` 分支準備中的插件改動。

## 回報安全問題

如果你發現與本倉庫相關的安全問題，請不要在公開 issue 中貼出可利用細節、token、API key、密碼、私鑰或個人敏感資訊。

建議先透過 GitHub 私下聯絡維護者，或建立一個不包含敏感細節的 issue，說明需要私下溝通安全問題。

## 安裝者安全提示

安裝包含 command hook 的 Antigravity 插件前，請在 Antigravity 中執行：

```text
/hooks
```

審查實際命令後再 trust。不要盲目信任未知 hook，也不要把 API key、token 或機器專屬路徑寫進插件輸出。
