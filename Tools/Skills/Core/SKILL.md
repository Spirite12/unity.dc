---
name: Core
description: 用于阅读工程结构、编写和完善代码，以及在功能开发时需要调用
---

# Unity Project Core

从这里开始阅读当前工程。先确认全局约束，再按任务跳转到对应 references。

## 全局约束

- 所有文本文件读取统一使用 UTF-8；
- 在写函数的时候，需填写相对应脚本语言的中文注释；
- 禁止修改 `Assets/Plugins/` 下的第三方插件代码；
- 非明确需求，不修改`Assets/Docs/` 下任何文件；
- 非明确需求，不修改 `Assets/DCFrame/` 下的框架基类与公共模块；
- 游戏功能开发时：
  - 文本读取统一来自 `table` 表，并在对应 `Localization` 下读取；


## 阅读顺序

1. 先读当前文档，确认硬规则和只读边界。
3. 根据任务涉及的模块，阅读对应的 `references` 专题文档。

## references 导航

- 工程目录与模块入口：`references/project-map.md`
- 框架层说明：`references/framework.md`
- UI / 红点 / 音效：`references/ui.md`
- 表 / 导表 / 生成代码：`references/table.md`
- 本地化：`references/localization.md`
