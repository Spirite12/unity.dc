---
name: project-core
description: Unity 工程主入口与全局约束。用于理解工程结构、编写和完善代码，以及在功能开发时遵循已有框架、配置与模块边界。
---

# Unity Project Core

从这里开始阅读当前工程。先确认全局约束，再按任务跳转到对应 references。

## 全局约束

- 所有文本文件读取统一使用 UTF-8。
- 禁止修改 `Assets/Docs/` 下任何文件；该目录只允许读取。
- 非明确需求，不修改任何 `Editor` 目录代码。
- 非明确需求，不修改 `Assets/Plugins/` 下的第三方插件代码。
- 非明确需求，不修改 `Assets/DCFrame/` 下的框架基类与公共模块。
- 文本本地化来源统一来自 `table` 表，并生成到 Localization 资源；不要在其他位置单独新增一套文本本地化来源。

## 工程定位

- `Assets/DCFrame/`：框架层，提供 UI、Table、Localize、Event、Cache、Addressable、TextFilter、RedTip 等基础能力。
- `Assets/Game/`：业务层，包含场景、预制体、配置、表、本地化数据、业务脚本。
- `Assets/Game/Settings/`：系统配置入口，开发前优先检查是否已有对应配置资源。
- `Assets/Plugins/`：第三方插件目录，默认只做接入层说明，不做修改。

## 阅读顺序

1. 先读当前文档，确认硬规则和只读边界。
2. 开发前先检查 `Assets/Game/Settings/` 下是否已有对应系统配置资源。
3. 根据任务涉及的模块，阅读对应的 `references` 专题文档。
4. 若任务是完整功能开发、跨多个模块，或需要安排实现顺序，再阅读 `references/workflow.md`。

## references 导航

- 工程目录与模块入口：`references/project-map.md`
- 框架层轻说明：`references/framework.md`
- UI / 红点 / 音效：`references/ui.md`
- 表 / 导表 / 生成代码：`references/table.md`
- 本地化：`references/localization.md`
- 开发流程占位：`references/workflow.md`
