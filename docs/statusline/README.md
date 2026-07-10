<div align="center">

# 📊 StatusLine 插件

### 为 Antigravity CLI 打造的简洁信息状态栏

</div>

---

## ✨ 功能

在 Antigravity CLI 底部状态栏实时展示关键工作上下文：

```
🤖 Gemini 3.1 Pro (High) [High] │ 📂 my-project │ ⎇ feature/my-branch*
📈 未命中输入: 30000 │ 🗂️ 缓存输入: 120000 │ 📤 输出: 450 │ 🎯 命中率: 80.0% │ 🧠 上下文使用: 7.5%
💰 会话消费: $0.0769 │ 🏢 目录消费: $0.0000 │ ⏱️ 耗时: 2m5s │ 🔌 MCP: 0 │ 🛠️ Skills: 6 │ 🪝 Hooks: 1
```

| 区段 | 数据来源 / 计算方式 |
|------|--------------------|
| 第一行 | `settings.json` 解析模型及思考强度，`os.getcwd()` 获取目录，`git status` 探测分支与脏标记。 |
| 第二行 | 解析 agy 传入的 `telemetry` JSON，拆解 `prompt_tokens` 和 `cached_prompt_tokens` 计算命中率及上下文使用占比。 |
| 第三行 | 解析计费金额，若缺失则根据 token 消耗按标准费率估算；统计 `.gemini/config/` 中的 MCP、Skills 和 Hooks 数量。 |

## 🚀 安装

### 方式一：原生安装 (推荐)

```bash
agy plugin install https://github.com/ZaunEkko/agy-plugins.git
```

### 方式二：Marketplace 安装

```bash
agy-plugin add statusline@zaunekko
```

## ⚙️ 配置

安装完成后，编辑 `~/.gemini/antigravity-cli/settings.json`，将 `statusLine` 改为：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python ~/.gemini/config/plugins/statusline/scripts/statusline.py",
    "enabled": true
  }
}
```

> **Windows 用户**：请将路径替换为完整绝对路径，例如：
> ```json
> "command": "python C:\\Users\\你的用户名\\.gemini\\config\\plugins\\statusline\\scripts\\statusline.py"
> ```

也可以通过 CLI 内置命令 `/statusline` 或 `/config` 交互式修改。

## 🎨 自定义

打开 `scripts/statusline.py`，在顶部的 **Configuration** 区块中即可自定义：

```python
# 显示哪些区段、以什么顺序
SEGMENTS = ["model", "branch", "workspace"]

# 区段之间的分隔符
SEPARATOR = " │ "

# 每个区段的前缀图标（设为 "" 可隐藏）
ICONS = {
    "model": "🤖",
    "branch": "⎇",
    "workspace": "📂",
}
```

## 🔧 工作原理

1. 每当 agent 状态变化，agy 将 JSON state payload 通过 **stdin** 传给脚本
2. 脚本解析 payload，优先使用其中的 `model`、`git_branch` 字段
3. 若 payload 中缺少对应字段，自动回退到读取 `settings.json` 或执行 `git` 命令
4. 格式化后的单行文本通过 **stdout** 返回给 agy 渲染

## 📋 要求

- Python 3.8+（无外部依赖）
- Git（用于分支检测）

## 📄 许可证

[MIT License](../../LICENSE)
