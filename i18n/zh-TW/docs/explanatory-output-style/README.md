# explanatory-output-style

[简体中文](../../../../docs/explanatory-output-style/README.md) · [English](../../../en/docs/explanatory-output-style/README.md) · [繁體中文](README.md) · [日本語](../../../ja/docs/explanatory-output-style/README.md) · [한국어](../../../ko/docs/explanatory-output-style/README.md)

`explanatory-output-style` 是一個 Antigravity 插件，用來在 Antigravity 會話中啟用解釋型輸出風格。

它參考 Claude Code 官方 [`explanatory-output-style`](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style) 插件的功能體驗：透過 `SessionStart` hook 在會話開始時加入額外指引，讓模型在寫程式碼或修改程式碼時補充簡短、貼近目前程式碼庫的 Insight 說明。

## 適合什麼場景

- 希望 Antigravity 不只給最終改動，也解釋為什麼這樣實作。
- 希望團隊共享同一套「邊做邊解釋」的協作風格。
- 希望把輸出風格作為可安裝插件分發，而不是每個專案都複製提示詞。

## 和 Claude Code 官方插件的關係

Claude Code 官方插件使用 `SessionStart` hook 在會話開始時加入解釋型輸出指引。這個倉庫中的實作面向 Antigravity 插件系統重新適配：

- 使用 Antigravity 插件 manifest：`plugins/explanatory-output-style/.agy-plugin/plugin.json`
- 使用 Antigravity hook 設定：`plugins/explanatory-output-style/hooks/hooks.json`
- 使用 Python hook 輸出 Antigravity 需要的 JSON payload：`hookSpecificOutput.additionalContext`
- 保留 Windows / Unix 兩套 hook command，方便跨平台安裝

## 注入後的協作效果

插件注入的上下文會要求 Antigravity：

1. 在寫程式碼或修改程式碼前後提供簡短 Insight。
2. 重點解釋目前程式碼庫裡的實作選擇、專案約定和取捨。
3. 避免泛泛而談，不把通用程式設計概念寫成長篇教學。
4. 使用適合窄終端的輸出區塊格式，減少換行和右邊框錯位。

目前 Insight 區塊格式範例：

```text
`+-------------------- ★ Insight --------------------+`
| 說明目前實作選擇的 2-3 條簡短要點
`+---------------------------------------------------+`
```

bullet 行只保留左側 `|`，不加入右側邊框，避免終端自動換行後出現邊框錯位。

## 安裝與啟用

```bash
agy plugin marketplace add ZaunEkko/agy-plugins
agy plugin add explanatory-output-style@zaunekko
```

包含 command hook 的插件首次執行前需要在 Antigravity 中審查並信任：

```text
/hooks
```

審查重點：

- `hooks/hooks.json` 中實際執行的 command。
- `hooks/session_start.py` 是否只輸出預期 JSON。
- hook 輸出裡不應包含 API key、token、機器專屬路徑或其他敏感資訊。

## 本機驗證

從倉庫根目錄執行：

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
agy plugin list
```

前三條分別驗證 Python 語法、hook JSON payload 和插件輸出格式；`agy plugin list` 用於確認 Antigravity 能發現 marketplace 插件。
