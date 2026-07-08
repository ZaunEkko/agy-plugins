# 仓库协作指南

## Context7 文档查询规则

当用户询问库、框架、SDK、API、CLI 工具或云服务相关问题时，必须使用 `ctx7` CLI 获取当前文档，即使是 React、Next.js、Prisma、Express、Tailwind、Django、Spring Boot 等常见技术也一样。适用范围包括 API 语法、配置项、版本迁移、特定库调试、安装步骤和 CLI 用法。

不要把 `ctx7` 用于重构、从零编写脚本、业务逻辑调试、代码审查或通用编程概念。

执行步骤：

1. 解析库：`npx ctx7@latest library <name> "<用户完整问题>"`。库名使用官方写法，例如 `Next.js`，不要写成 `nextjs`。
2. 根据名称匹配度、描述相关性、代码片段数量、来源可信度和 benchmark 分数选择最佳结果。结果不合适时，最多换一种名称或查询方式重试。
3. 获取文档：`npx ctx7@latest docs <libraryId> "<用户完整问题>"`。
4. 基于获取到的文档回答。

除非用户直接提供 `/org/project` 格式的库 ID，否则必须先运行 `library` 获取有效 ID。每个问题最多运行 3 条 Context7 命令。不要在查询中包含 API key、密码、凭据等敏感信息。

如果命令因额度限制失败，告知用户并建议运行 `npx ctx7@latest login` 或设置 `CONTEXT7_API_KEY`。不要静默退回到训练数据。如果 Context7 CLI 在 Antigravity 默认沙箱内出现 DNS、ENOTFOUND、host resolution 或 fetch failed 等网络错误，应在沙箱外重试。

## 项目结构与模块组织

本仓库是个人 Antigravity 插件市场。根目录 `README.md` 描述市场定位和当前插件清单。市场元数据位于 `.agents/plugins/marketplace.json`，每个插件条目指向本地插件目录。

插件包放在 `plugins/<plugin-name>/` 下。当前包含 `explanatory-output-style` 和 `commit-commands`。每个插件的清单位于 `.agy-plugin/plugin.json`；hook 放在 `hooks/`，skill 放在 `skills/<skill-name>/SKILL.md`。

简体中文插件文档放在 `docs/<plugin-name>/README.md`，English、繁體中文、日本語和 한국어 版本放在 `i18n/<language>/docs/<plugin-name>/README.md`。新增插件或修改用户可见行为时，必须同步根 `README.md`、四个 `i18n/<language>/README.md` 和对应语言的插件文档。

测试目前放在 `tests/` 目录。行为变复杂时，继续添加聚焦测试；小型插件专属测试也可以放在对应插件附近。

## 构建、测试与开发命令

从仓库根目录运行轻量验证命令：

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest discover -s tests
agy plugin list
```

`py_compile` 用于检查 Python 语法。直接运行 `session_start.py` 会输出 hook JSON payload，适合在修改注入上下文后确认内容。`python -m unittest discover -s tests` 运行所有插件测试。`agy plugin list` 用于确认 Antigravity 能发现已安装的市场插件。

## 代码风格与命名约定

JSON 使用两个空格缩进，Python 使用四个空格缩进。插件和 skill 目录名保持小写短横线格式，并分别与 manifest 名称或 `SKILL.md` 的 `name` 一致，例如 `explanatory-output-style` 和 `clean-gone`。

Hook 脚本保持小而明确。优先使用 Python 的 `json.dumps()` 生成结构化 JSON，不要手写 JSON 字符串。保留 `hooks/hooks.json` 中的跨平台 hook 命令，包括 Unix 和 Windows 的独立命令形式。

## 测试规范

修改 Python hook 后，必须运行 `python -m py_compile`、直接执行 hook，并运行相关单元测试。确认输出是有效 JSON，且包含预期的 `hookSpecificOutput` 字段。

新增插件时，既要测试市场发现能力，也要测试插件的主要 hook 或 skill 路径，并验证五种语言的文档入口完整。Skill 测试应覆盖隐式触发描述和显式 `$skill-name` 入口。如果 hook 需要 Antigravity 信任，应在 README 或插件文档中说明 `/hooks` 审查步骤。

## 本地跨会话交接

开始工作时，如果仓库根目录存在 `HANDOFF.local.md`，先读取它再决定下一步。该文件用于记录未完成任务、当前分支、验证结果和后续动作，只保留在本机并由 `.gitignore` 忽略。

结束未提交或未推送的工作前，更新 `HANDOFF.local.md`。不要在其中写入 API key、token、密码、机器专属凭据或其他敏感信息。

## Git 工作流

本仓库遵循 Git Flow 分支模型：

- `main` 是稳定生产分支，只接收已完成的 release 或 hotfix 变更。
- `dev` 是日常开发集成分支。
- `feature/*` 用于新功能和非紧急改动，从 `dev` 拉出，完成后合回 `dev`。
- `release/*` 用于发布准备，从 `dev` 拉出，只做发布润色、版本号、文档和发布前 bug 修复，完成后合入 `main` 和 `dev`。
- `hotfix/*` 用于线上紧急修复，从 `main` 拉出，修复后合入 `main` 和 `dev`。

改动前先运行 `git status`，保护用户已有改动，不要回滚无关文件。避免在 `main` 上直接做功能开发；如果仓库尚未建立 `dev` 或对应分支，先按用户指示处理分支，不要擅自推送远端。

允许在本地进行清晰、聚焦的提交；远程 push 必须等用户明确指示后再执行。

## 提交与拉取请求规范

提交信息使用简短的中文祈使句，不加句号，并让主题聚焦到变更对象，例如 `更新说明输出样式 hook` 或 `补充插件市场文档`。

Pull Request 应说明插件行为变化、列出已运行的验证命令，并注明 hook 信任或安全影响。只有用户可见文档或市场展示发生变化时，才需要附截图。

## 安全与配置提示

不要把 API key、密钥、凭据或机器专属路径写进 hook 输出或插件 manifest。信任 command hook 前要仔细审查；修改 hook 脚本或命令字符串后，需要重新审查。修改 skill 后应刷新插件缓存版本、重新安装并新开 thread 验证。
