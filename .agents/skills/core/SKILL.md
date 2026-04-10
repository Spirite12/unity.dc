---
name: Core
description: 用于阅读工程结构、编写和完善代码，以及在功能开发时需要调用
---

# Core Skill 入口规范

用于建立当前工程的基础认知，并按任务范围跳转到对应的 `references` 文档。

## 使用顺序

1. 先读当前文档，确认 `core` 的入口导航、索引与专题边界。
2. 再读 `references` 下“工程目录与模块入口”专题文档。
3. 根据任务涉及的模块，阅读对应的 `references` 专题文档。

## 当前职责

- `core` 负责工程入口导航、专题文档索引、模块边界说明与 `core` 自身的自检配置。
- 仓库级通用规则、完成定义与通用自检门禁不在本 Skill 内重复维护。

## 业务开发约束

- 文本统一从 `table` 表读取，并在对应的 `Localization` 下访问。

## 自检入口

- 通用自检脚本：`.agents/scripts/skill_self_check.py`
- 自检注册表：`.agents/registries/skill-self-check.json`
- `core` 自检配置：`.agents/skills/core/scripts/self-check.json`
- `core` 对外描述配置：`.agents/skills/core/agents/openai.yaml`
- 当脚本命中 `core` 相关规则时，优先补丁式更新当前文档或对应 `references/*.md`，不整篇重写。

## scripts 索引

- Unity 自动化入口：`scripts/run_unity_task.py`
  - 用途：通过 Unity 命令行执行导表与本地化资源生成，并可按 `LocalizeRules` 上的“本地化表生成”“本地化资源生成”按钮顺序执行初始化。
  - 使用提示：涉及 `TableEditor.PackageConfig()`、`LocalizeEditor.CreateLocalizeAsset()` 或首次初始化 Localize 流程时，优先调用该脚本；

## references 索引

- 工程目录与模块入口：`references/project-map.md`
- 框架层说明：`references/framework.md`
- UI / 红点 / 音效：`references/ui.md`
- 表 / 导表 / 生成代码：`references/table.md`
- 本地化：`references/localization.md`

## references 文档编写约定

- 专题文档优先围绕当前任务所需的信息组织内容，保证结构清晰、便于执行，不强制统一模板。
- 按目录、模块或入口罗列内容时，默认按文件夹或路径名字母顺序排列；若采用其他顺序，需说明依据。
- 文档优先记录入口、规则、处理顺序与执行边界，不优先写易过时的实现细节、长代码示例或零散调用片段。
- 说明用法时，优先写简短的“使用提示”或“接入提示”，不展开成完整教程。
- 文档应尽量明确 AI 与开发者的分工边界；若步骤依赖手动操作、资源摆放、预制体拼装或最终表现校验，需单独说明由开发者处理。
