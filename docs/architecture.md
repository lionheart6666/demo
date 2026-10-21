# 架构

## 技术形态

单文件 Web APP：`index.html`（HTML+CSS+JS 一体，无构建步骤、无后端）。
静态服务器托管（开发用 `python -m http.server 5174`），浏览器打开即用。
移动端真机版本为独立 Expo 项目 `../KaoGong`（React Native），与本 Web 版并行，功能对齐。

## 数据模型

两类存储，职责分离：

**1. 用户数据 `DB`（localStorage，键 `kg_db_v1`）** —— 全部可写数据：

| 字段 | 说明 |
|---|---|
| questions | 用户导入/示例题目（id/module/question_type/exam_point/stem/options/answer/analysis/source/pass_rate） |
| records | 每题作答记录（ok 是否正确、ms 用时、redo 是否错题重做），统计页数据源 |
| groups | 每组（10题）成绩，过关判定与趋势图数据源 |
| progress | 考点进度 `{模块|考点: {passed, streak}}` |
| mistakes | 错题/标记题快照（含错因 reason、resolved、wrongCount）；重做答对自动置 resolved |
| videos | 视频条目（本地 blob 引用或网盘链接） |
| cards | 背诵卡片（deck/front/back/stage/next） |
| tips | 用户自建技巧（m 模块/t 标题/b 正文） |
| checkins | 打卡日期数组（`YYYY-MM-DD`），连续天数由它推算 |
| settings | 外观（theme: default/dark/auto, font, size） |
| moduleOrder | 练习页模块排列顺序（key 数组） |
| hiddenPoints | 被删除（隐藏）的考点小标题，可恢复，题目不删 |
| hiddenGroups | 被删除的分组，存 `模块key:组名`，可恢复 |

**2. 静态真题库（`data/*.json`，fetch 按需加载，不写 localStorage）** —— 见 [question-bank.md](question-bank.md)。
内存中三份注册表：`BANK_MANIFEST`（考点→题数，用于练习页计数）、`BANK_FILES`（考点→文件名）、`BANK_DATA`（已加载题目缓存）。

## 视图路由

无路由库。全局状态 `S = {view, tab, params}`，`render()` 按 `S.view` 分发到 `view*()` 函数，拼 header + body + tabbar。
底部 6 个 Tab：练习 / 技巧 / 课程 / 背诵 / 导图 / 我的；`quiz / import / mistake` 为栈式页面（顶部有返回，Tab 高亮保持来源页）。

## 模块划分（代码区与之一一对应）

| 代码区块 | 职责 |
|---|---|
| 数据层 | load/save、ID 分配 |
| 外观设置 | 亮/暗/跟随系统（prefers-color-scheme 监听）、字体、字号 |
| 判分 | judge()：单选/多选（集合全等）/判断 |
| 练习 | 模块树（两级折叠）、模块手动排序、考点/分组删除与恢复、考点计数（用户题+真题库）、今日计划卡、打卡、正确率趋势 |
| 刷题 | QZ 状态机：抽题→作答→提交→解析→下一题→组结算→过关判定；单题计时 + 2 分钟提醒；组结算含用时诊断 |
| 组卷 | 错题重做（target 90%，答对移出）、弱项组卷（近期 <80% 考点 + 错题，不足补真题库随机考点，20 题） |
| 错题本 | 错题/标记题列表、错因标注、一键重做 |
| 导入题库 | 四格式解析（见 import-format.md） |
| 课程 | 本地视频（blob 播放）、网盘链接管理 |
| 背诵 | 艾宾浩斯卡片：单卡表单 + 批量粘贴导入、卡组筛选 |
| 技巧库 | 内置 UP 主方法论（TIPS_BUILTINS 常量，只读）+ 用户技巧 CRUD |
| 导图 | 知识点骨架树（静态 TREE 常量） |
| 我的 | 统计、打卡、趋势、数据备份（导出/导入 JSON）、过关列表、外观设置、基线信息、重置 |

## 关键设计取舍

- **题目快照进错题本**：错题记录冗余存题目内容，与题库无外键关联，删题不影响错题本。
- **真题库不入 localStorage**：5.9 万题远超 5MB 配额，故静态 JSON + 按需 fetch + 内存缓存。
- **本地视频用 blob**：刷新即失效（浏览器限制）；网盘链接持久但跳转外部打开。真机版无此限制。
- **禁用原生对话框**：预览环境（iframe）禁用 `alert/confirm/prompt`。确认操作用应用内弹层 `askConfirm(msg, onYes)`（`render()` 末尾渲染 `.overlay`），提示用 `toast(msg)`，输入操作一律用内嵌表单。
