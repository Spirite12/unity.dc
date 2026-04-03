---
name: Core
description: 用于阅读工程结构、编写和完善代码，以及在功能开发时需要调用
---

# Core Skill 入口规范

用于建立当前工程的基础认知，并按任务范围跳转到对应的 `references` 文档。

## 使用顺序

1. 先读当前文档，确认硬规则和只读边界。
2. 再读 `references` 下“工程目录与模块入口”专题文档。
3. 根据任务涉及的模块，阅读对应的 `references` 专题文档。

## 硬性约束

- 所有文本文件统一使用 UTF-8 读取。
- 新增或修改函数时，按对应脚本语言习惯补充简洁的中文注释。

## 业务开发约束

- 文本统一从 `table` 表读取，并在对应的 `Localization` 下访问。

## references 索引

- 工程目录与模块入口：`references/project-map.md`
- 框架层说明：`references/framework.md`
- UI / 红点 / 音效：`references/ui.md`
- 表 / 导表 / 生成代码：`references/table.md`
- 本地化：`references/localization.md`
