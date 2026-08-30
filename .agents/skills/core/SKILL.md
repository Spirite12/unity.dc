---
name: Core
description: 用于阅读工程结构、编写和完善代码，以及在功能开发时需要调用
---

# Core Skill 入口规范

用于建立当前工程的基础认知，并按任务范围跳转到对应的 `references` 文档。

## 使用顺序

1. 先读仓库根目录 `AGENTS.md`，确认本次任务的读写边界、完成定义与项目级协作规则。
2. 检查工作区状态、子模块状态和任务范围；除非用户明确要求，不把 `Library/`、`Logs/`、`obj/`、IDE 缓存等可再生文件当作工程源码审查对象。
3. 再读当前文档，确认 `core` 的入口导航、索引与专题边界。
4. 读取 `references/project-map.md`，根据任务涉及的模块继续读取对应专题文档。

## 当前职责

- `core` 负责工程入口导航、专题文档索引、模块边界说明与 `core` 自身的自检配置。
- 仓库级通用规则与完成定义不在本 Skill 内重复维护；PR 前 Core 检查流程由根目录 `AGENTS.md` 约束，通用 GitHub 操作由系统级 `github-workflow` Skill 执行。
- `Assets/DCFrame/` 是 Git 子模块；业务任务默认不修改其源码。涉及框架事实时，应同时报告父仓库记录的提交与当前子模块提交是否一致。

## 业务开发约束

- 文本统一从 `table` 表读取，并在对应的 `Localization` 下访问。

## 自检入口

- 通用自检脚本：`.agents/scripts/skill_self_check.py`
- 自检注册表：`.agents/registries/skill-self-check.json`
- `core` 自检配置：`.agents/skills/core/scripts/self-check.json`
- `core` 对外描述配置：`.agents/skills/core/agents/openai.yaml`
- 当 PR 前检查命中 `core` 相关规则时，优先补丁式更新当前文档或对应 `references/*.md`，不整篇重写。

## scripts 索引

- Unity 自动化入口：`scripts/run_unity_task.py`
  - 用途：通过 Unity 命令行调用项目提供的 `CodexBatchVerify` 批处理适配器，执行导表、本地化资源生成或其初始化顺序。
  - 适配器位置：`Assets/DCFrame/Editor/Foundation/CodexBatchVerify.cs`；该文件位于 DCFrame 子模块，修改后需同步核对子模块提交与父仓库指针。
  - 前置条件：项目必须实现脚本映射的静态入口；脚本会先扫描并验证该适配器，缺失时不得启动 Unity，也不得把未执行的生成步骤报告为已完成。
  - 使用提示：适配器存在时，涉及 `TableEditor.PackageConfig()`、`LocalizeEditor.CreateLocalizeAsset()` 或首次 Localize 初始化可优先调用该脚本；适配器缺失时，由开发者在 Unity Editor 的既有工具入口执行，或先补齐适配器。

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
