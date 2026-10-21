# KaoGongWeb 文档库

公路·个人版（考公刷题 APP）的架构文档。描述**架构与规则**，不记录实现细节与变更历史（实现看代码、变更看 git）。

## 目录

| 文档 | 内容 |
|---|---|
| [architecture.md](architecture.md) | 整体架构：技术形态、数据模型、模块划分、视图路由 |
| [rules.md](rules.md) | 业务规则：判分、过关判定、艾宾浩斯、错题收录等产品逻辑内核 |
| [import-format.md](import-format.md) | 题库导入格式规范：Excel / JSON / Markdown / TXT |
| [question-bank.md](question-bank.md) | 静态真题库：来源、转换管线、按需加载机制 |
| [material-index.md](material-index.md) | 本地金监局资料与 APP 知识树的映射、题源清单 |

## 维护约定

1. 文档描述架构而非实现——实现细节拿本文档去 `index.html` 找对应代码区。
2. 文档不是更新日志，不记"哪天改了什么"，只忠实描述**现存**架构。
3. 新增功能模块时：先在本库更新/新增架构文档，再改代码。
4. 代码区注释用 `/* ===== 区块名 ===== */` 分隔，与文档中的模块名一一对应。
