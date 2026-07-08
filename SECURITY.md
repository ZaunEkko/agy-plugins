# Security Policy

[简体中文](SECURITY.md) · [English](i18n/en/SECURITY.md) · [繁體中文](i18n/zh-TW/SECURITY.md) · [日本語](i18n/ja/SECURITY.md) · [한국어](i18n/ko/SECURITY.md)

## 支持范围

当前支持 `main` 分支上的最新发布内容，以及正在 `dev` 分支准备中的插件改动。

## 报告安全问题

如果你发现与本仓库相关的安全问题，请不要在公开 issue 中贴出可利用细节、token、API key、密码、私钥或个人敏感信息。

建议先通过 GitHub 私下联系维护者，或创建一个不包含敏感细节的 issue，说明需要私下沟通安全问题。

适合报告的问题包括：

- command hook 中存在意外命令执行风险。
- hook 输出包含敏感信息。
- 插件文档或示例可能诱导用户泄露凭据。
- marketplace 或 manifest 指向了错误或不可信路径。

## 安装者安全提示

安装包含 command hook 的 Antigravity 插件前，请在 Antigravity 中执行：

```text
/hooks
```

审查实际命令后再 trust。不要盲目信任未知 hook，也不要把 API key、token 或机器专属路径写进插件输出。
