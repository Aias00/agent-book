# Agent 工程入门与实战 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 编写面向 Java 开发者的中文 Agent 学习书，生成可验证的 EPUB 和 GitHub Pages 在线阅读站点，并提交到用户的 GitHub。

**Architecture:** 以 Markdown 章节作为唯一内容源，同时生成 EPUB 与静态 HTML。Java 21 + Maven 示例按渐进检查点组织，核心离线模拟不依赖模型密钥；可选模型适配层单独隔离。生成脚本把在线站点写入 `docs/site/`，把 EPUB 写入 `docs/downloads/`，保留 `docs/superpowers/` 设计与计划文件；GitHub Actions 发布整个 `docs/`。

**Tech Stack:** Java 21, Maven, JUnit 5, Jackson（仅模型适配需要）, Pandoc, HTML/CSS, GitHub Actions, GitHub Pages。

---

### Task 1: 初始化项目与构建骨架

**Files:**
- Create: `README.md`, `LICENSE`, `pom.xml`, `.gitignore`, `metadata.yaml`
- Create: `manuscript/00-preface.md`, `manuscript/01-boundary.md`, `manuscript/02-model-and-interface.md`, `manuscript/03-agent-loop.md`, `manuscript/04-tools.md`, `manuscript/05-context.md`, `manuscript/06-rag.md`, `manuscript/07-memory.md`, `manuscript/08-workflows.md`, `manuscript/09-multi-agent.md`, `manuscript/10-mcp.md`, `manuscript/11-security.md`, `manuscript/12-evaluation.md`, `manuscript/13-observability.md`, `manuscript/14-performance.md`, `manuscript/15-capstone.md`, `manuscript/16-maintenance.md`, `manuscript/99-appendix.md`
- Create: `examples/agent-core/src/main/java/...`, `examples/agent-core/src/test/java/...`
- Create: `scripts/build-book.sh`, `scripts/check-book.py`, `assets/style.css`

- [ ] 建立 Java 21 Maven 模块、目录和固定版本。
- [ ] 写最小可运行的离线 Agent 核心与 JUnit 测试，先验证命令和输出。
- [ ] 编写书稿公共元数据、章节模板和构建脚本；模板强制包含学习目标、原理、Java 示例、失败分析、练习、参考答案、小结和引用。

### Task 2: 编写基础章节与离线核心示例

**Files:** `manuscript/00-preface.md`, `01-boundary.md`, `02-model-and-interface.md`, `03-agent-loop.md`, `04-tools.md`, `examples/agent-core/**`

- [ ] 完成前言和第 1–4 章，包含目标、原理、Java 示例、失败分析、练习及答案链接。
- [ ] 实现 `ModelGateway`, `Tool`, `ToolRegistry`, `AgentLoop` 等最小接口，覆盖预算耗尽、参数非法和工具错误。
- [ ] 运行 JUnit 与示例命令并记录真实输出。

### Task 3: 编写上下文、检索、记忆与工作流章节

**Files:** `manuscript/05-context.md`, `manuscript/06-rag.md`, `manuscript/07-memory.md`, `manuscript/08-workflows.md`, `examples/agent-core/src/main/java/book/agent/retrieval/**`, `examples/agent-core/src/main/java/book/agent/state/**`, `examples/agent-core/src/main/java/book/agent/workflow/**`, `examples/agent-core/src/test/java/book/agent/**`

- [ ] 用本地知识库和可解释关键词评分实现检索，返回来源标识与无结果状态。
- [ ] 实现会话状态、长期事实的过期/删除、检查点和恢复。
- [ ] 完成第 5–8 章及可运行测试，报告固定输入下的结果。

### Task 4: 编写协作、安全、评测、观测和部署章节

**Files:** `manuscript/09-multi-agent.md`, `manuscript/10-mcp.md`, `manuscript/11-security.md`, `manuscript/12-evaluation.md`, `manuscript/13-observability.md`, `manuscript/14-performance.md`, `manuscript/15-capstone.md`, `manuscript/16-maintenance.md`, `manuscript/99-appendix.md`, `examples/agent-core/src/main/java/book/agent/collaboration/**`, `examples/agent-core/src/main/java/book/agent/security/**`, `examples/agent-core/src/main/java/book/agent/evaluation/**`, `examples/agent-core/src/main/java/book/agent/observability/**`, `examples/agent-core/src/main/java/book/agent/model/**`, `examples/agent-core/src/test/java/book/agent/**`

- [ ] 完成第 9–16 章，覆盖 MCP 工具边界、提示注入防护、人工审批、基线评测、事件追踪、并发/超时和运行手册。
- [ ] 为拒绝调用、恶意文档、恢复、副作用计数和评测指标增加离线测试。
- [ ] 添加可选模型适配说明，明确真实 API 测试与模拟测试的边界，不在无密钥环境伪造结果；为每个引用结论链接 `docs/superpowers/specs/2026-10-20-source-notes.md` 中的来源编号。
- [ ] 将来源映射落实为章节引用：R1→第 1、3、8 章，R2→第 6、15 章，R3→第 5、12 章，R4→第 2、4 章，R5→第 2–4 章，R6→第 10、11 章，R7→构建与附录；沿用来源笔记中的限制说明和章节验收证据。

### Task 5: 构建 EPUB 与在线阅读站点

**Files:** `scripts/build-book.sh`, `scripts/check-book.py`, `assets/cover.svg`, `assets/style.css`, `docs/site/index.html`, `docs/site/style.css`, `docs/downloads/agent-engineering-java.epub`, `.github/workflows/pages.yml`

- [ ] 用 `metadata.yaml` 和 `assets/cover.svg` 生成 EPUB 3；把 Markdown 转为 `docs/site/` 静态 HTML，生成章节导航、代码样式和指向 `../downloads/agent-engineering-java.epub` 的下载入口；脚本不得删除 `docs/superpowers/`。
- [ ] 检查 EPUB ZIP/XML、内部链接、元数据和阅读顺序；如环境可用运行 EPUBCheck。
- [ ] 用本地 HTTP 服务人工检查桌面/移动布局、中文排版、目录导航、Java 代码块和下载。

### Task 6: GitHub 发布与验收

**Files:** `README.md`, `.github/workflows/pages.yml`

- [ ] 创建或确认 `Aias00/agent-book` 公开仓库，提交源稿、示例、EPUB 和站点。
- [ ] 启用 GitHub Pages，等待工作流完成并实际访问正文和 EPUB 下载 URL。
- [ ] 对照设计验收清单记录 Java/Maven 测试、EPUB 检查、站点检查、远端提交和发布 URL。

### Task 7: 内容完整性与引用门槛

**Files:** `scripts/check-book.py`, `manuscript/*.md`, `docs/superpowers/specs/2026-10-20-source-notes.md`, `README.md`

- [ ] 检查 16 章和附录全部存在；每章必须包含学习目标、原理、Java 示例、失败分析、练习、参考答案、小结和至少一个与来源笔记对应的引用或明确标注“工程推导”。
- [ ] 检查中文正文（不含代码、目录、元数据）总量达到 40,000–60,000 字符；脚本报告每章字符数和缺失段落。
- [ ] 只有完整性检查、测试、EPUB 检查和在线人工阅读全部有证据后，才在 README 标注可读地址和下载地址。

每个任务完成后运行相关验证并单独提交；最终发布前执行全量验证，只有证据齐全才报告完成。
