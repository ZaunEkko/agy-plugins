# Contributing

[简体中文](../../CONTRIBUTING.md) · [English](../en/CONTRIBUTING.md) · [繁體中文](CONTRIBUTING.md) · [日本語](../ja/CONTRIBUTING.md) · [한국어](../ko/CONTRIBUTING.md)

感謝你對 `agy-plugins` 的關注。這個倉庫主要維護面向 Antigravity 的插件、hooks、skills、預設和相關文件。

## 分支與提交流程

本倉庫使用 Git Flow：

- `main`：穩定發布分支。
- `dev`：日常整合分支。
- `feature/*`：新功能、文件、插件改動，從 `dev` 拉出，完成後透過 PR 合回 `dev`。
- `release/*`：發布準備，從 `dev` 拉出，完成後合入 `main` 和 `dev`。
- `hotfix/*`：緊急修復，從 `main` 拉出，完成後合入 `main` 和 `dev`。

不要直接推送到 `main` 或 `dev`。這兩個分支受保護，改動應透過 Pull Request 合併，並等待必要檢查通過。

## 倉庫結構約定

新增插件時，優先遵循以下結構：

```text
plugins/<plugin-name>/
├── .agy-plugin/
│   └── plugin.json
└── ...

docs/<plugin-name>/
└── README.md
```

- `plugins/<plugin-name>/` 放可安裝插件內容。
- `docs/<plugin-name>/README.md` 放面向安裝者和使用者的插件說明。
- 根目錄 `README.md` 只做倉庫總覽和插件文件路由。
- 不要提交本地 Claude Code 初始化檔案 `CLAUDE.md`；它已被 `.gitignore` 忽略。

## 插件文件要求

每個插件文件至少說明：插件解決什麼問題、安裝方式、啟用或信任步驟、主要檔案路徑、維護者如何驗證。包含 command hook 時，需要說明 `/hooks` 審查和 trust。

## 驗證要求

請根據本次改動影響的插件執行對應驗證，不要只跑固定命令。

一般規則：

- 修改 Python hook：至少執行 `python -m py_compile <hook-script>`，並直接執行 hook 腳本確認輸出是有效 JSON。
- 修改 hook 設定：確認 `hooks.json` 是有效 JSON，並審查 command / commandWindows 是否仍然安全、可讀、跨平台。
- 修改插件 manifest：確認 `.agy-plugin/plugin.json` 是有效 JSON，且插件名、版本、描述和 marketplace 入口一致。
- 修改插件行為：執行該插件對應測試；如果沒有測試，應補充聚焦測試或在 PR 中說明未補測試的原因。
- 修改文件：檢查連結、路徑和安裝命令是否仍然準確。
- 新增插件：確認 marketplace 能發現該插件，並在文件中寫明安裝和信任步驟。

目前 `explanatory-output-style` 插件的維護者驗證範例：

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
```

這些命令只是該插件的範例；新增插件應在自己的文件或測試中定義對應驗證方式。

## Hook 與安全要求

- 不要在 hook 輸出、manifest、測試或文件中寫入 API key、token、密碼、私鑰或機器專屬路徑。
- 不要引入不透明或難以審查的命令字串。
- 保留必要的跨平台支援；Windows 和 Unix 命令不同時，應分別寫清楚。
- 新增或修改 command hook 後，必須在 PR 中說明安全影響和使用者需要 review / trust 的內容。

## Pull Request 要求

PR 描述應包含變更內容、已執行的驗證命令、是否修改 hook / manifest / marketplace metadata、Hook / 安全影響，以及未執行驗證的原因。
