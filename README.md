# Agent 工程入门与实战：Java 开发者学习指南

一本面向 Java 开发者的中文 Agent 工程学习书。全书围绕一个可测试的知识库助手，逐步讲解 Agent 边界、模型接口、工具调用、上下文、检索、记忆、工作流、多 Agent、MCP、安全、评测、观测、性能与维护。

- 在线阅读：`https://aias00.github.io/agent-book/`
- EPUB 下载：`https://aias00.github.io/agent-book/downloads/agent-engineering-java.epub`
- 源码与书稿：`https://github.com/Aias00/agent-book`

## 本地阅读

在线站点和 EPUB 都由 `manuscript/` 章节生成。需要 Pandoc；示例需要 JDK 21 和 Maven：

```bash
./scripts/build-book.sh
./scripts/check-book.py
cd examples/agent-core && mvn test
```

`examples/agent-core` 的离线测试不需要模型密钥。真实模型适配只作为可选扩展，必须自行配置密钥、端点、超时和费用预算。本书中的示例输出会标记为“实际运行输出”或“示意输出”。

## 目录

前言 + 16 章 + 附录。章节 Markdown 是唯一内容源；`downloads/` 保存 EPUB，`docs/site/` 保存 GitHub Pages 静态站点，`docs/superpowers/` 保存设计、资料和实施记录。

## 资料与版权

论文、工具调用文档、MCP 规范和 EPUB 规范的版本及适用限制见 [`docs/superpowers/specs/2026-10-20-source-notes.md`](docs/superpowers/specs/2026-10-20-source-notes.md)。正文中的工程建议不冒充论文结论。

Copyright © 2026 Aias00. 书稿与示例代码的授权范围见仓库中的 LICENSE 文件。
