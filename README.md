# 公路 · 个人版

个人专用的考公刷题 App（行测 / 申论 / 金监局计算机专业课），纯前端单页应用 + Android WebView 壳。

## 下载

最新安装包见 [Releases](https://github.com/lionheart6666/demo/releases/latest)：

| 版本 | 大小 | 说明 |
|---|---|---|
| [gonglu.apk](https://github.com/lionheart6666/demo/releases/download/v1.0/gonglu.apk) | 约 14 MB | 精简版：题库全在，不含题图；缺图处显示「（题图缺失）」 |
| [gonglu-full.apk](https://github.com/lionheart6666/demo/releases/download/v1.0/gonglu-full.apk) | 约 280 MB | 含 39,461 张题图，图形推理/资料分析可正常做 |

下载后点开安装，系统提示时允许「安装未知来源应用」。

## 功能

- **练习**：行测、申论、金监局专业课（8 组 23 考点，含 500 题冲刺题库）
- **技巧库**：各模块解题方法论
- **课程**：本地视频导入 + 网盘链接
- **背诵**：艾宾浩斯复习（1/2/4/7/15/30 天）
- **导图**：知识点骨架
- **我的**：正确率趋势、打卡、每日计划、备份导出/导入

刷题规则：10 题一组，连续 3 组 ≥80% 判定过关；错题与「拿不准」自动收录；单题超 2 分钟提醒。

## 目录结构

```
index.html            主程序（单文件：数据层 / 视图 / 逻辑 / 样式）
data/bank/            静态题库（按考点分 JSON，manifest.json 为索引）
docs/                 架构文档（架构、业务规则、导入格式、题库管线）
vendor/               xlsx 解析库（本地化，避免 CDN 依赖）
android/              WebView 壳源码与打包脚本
```

`data/img/` 不纳入仓库（256 MB，仅打进完整版 APK）。

## 构建 APK

需要 JDK 17 + Android build-tools 34 + android.jar(API 33)。手工构建，无需 Gradle：

```bash
python android/stage_assets.py        # 生成精简版 assets
python android/build_apk.py assets 公路.apk

python android/stage_full.py          # 生成含图 assets（需 data/img）
python android/build_apk.py assets_full 公路-完整版.apk
```

脚本内的 SDK 路径按本机实际情况修改。

## 数据

所有做题记录、错题、背诵卡存在本地 `localStorage`（键 `kg_db_v1`）。手机与电脑数据不互通，用「我的 → 导出备份」迁移。

## 文档

架构与规则见 [docs/README.md](docs/README.md)。
