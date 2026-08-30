# 本地化说明

## 定位

- 本文档用于说明文本本地化、资源本地化与相关业务代码的处理顺序。
- 本项目的文本本地化能力与 `table` 体系强关联；处理文案时，优先联动 `table.md` 一并确认。

## 关键目录与入口

- `Assets/Game/Settings/Localize/`：本地化系统配置入口与编辑器工具入口。
- `Assets/DCFrame/Modules/Localize/`：框架本地化运行时入口与规则目录。
- `Assets/Game/Localize/`：本地化资源根目录，文本与资源本地化均从这里组织；模板工程初始可不存在。含本地化字段或文本表的导表会创建文本表结构；资源本地化则需由开发者先准备资源类型和语言目录，不能仅靠新建空目录绕过生成器校验。
- 编辑器入口：
  - `Tools/资源项/本地化资源生成`
  - `CONTEXT/Text/Add Localize`
  - `CONTEXT/Image/Add Localize`
  - `CONTEXT/RawImage/Add Localize`

## 文本本地化

- 文本本地化来源统一来自 `table` 表。
- 生成结果统一进入 Localization 的字符串资源体系。
- 不允许在其他位置单独新增一套文本本地化来源。

### 文本来源

- 默认表：对勾选字段生成 `Localize.GetText(...)`
- 枚举表：对勾选枚举生成本地化字典
- 文本表：承接代码文本与预制体文本
- 常量表：不参与文本本地化

### key 规则

- 默认表字段：`表名.字段名.Id`
- 枚举表：`表名.枚举名.枚举值名`
- 文本表：`表名.Sign`

### 目录划分规则

- `Assets/Game/Localize/Text/`：文本本地化目录。
- `Text/Table/`：文本 Shared Data 与表资源目录。
- `Text/Zh-CN/` 等语言目录：存放对应语言的文本表资源。

## 资源本地化

- 统一通过 `Localize.LoadAsset<T>(key)` 加载。
- 资源统一放在 `Assets/Game/Localize/` 下，并按资源类型、语言进一步分层。
- 本地化资源通过现有生成工具生成表与 Shared Data，不手工绕过现有体系维护。

### 目录划分规则

- `Assets/Game/Localize/<资源类型>/`：资源本地化目录，例如 `Prefab/`、`Sprite/`、`Texture/` 等。
- `<资源类型>/Table/`：该资源类型的 Shared Data 与表资源目录。
- `<资源类型>/Zh-CN/` 等语言目录：存放对应语言的本地化资源。
- 本地化资源生成时，会扫描 `Assets/Game/Localize/` 下所有非 `Text` 目录，并按上述结构生成对应资源映射。

## 业务开发顺序

1. 先从策划案中拆出用户可见文案，以及需要随语言切换的资源。
2. 判断文案应落到默认表、枚举表还是文本表；不要直接在代码或预制体里长期写死文案。
3. 自动化前先确认项目实现了 `CodexBatchVerify.RunInitLocalize` 或对应单任务入口；入口存在时才可调用 `scripts/run_unity_task.py init-localize`，按 `LocalizeRules` 上“本地化表生成”“本地化资源生成”的顺序执行。入口缺失时，停止自动化并报告开发者，由开发者在 Unity Editor 中执行既有按钮，或先补齐适配器。
4. 仅涉及文本时，先完成含本地化字段或文本表的导表，再检查 `Assets/Game/Localize/Text/` 是否由 Unity Localization 生成；无本地化表规则时，根目录未生成属于正常结果。
5. 若涉及资源本地化，由开发者先准备资源类型目录、`Table/` 和语言目录；AI 不应为了通过目录检查而补建没有资源或命名依据的空目录。
6. 资源本地化文件需先由开发者放入对应语言目录；若需要占位资源，需先确认当前需求是否允许补建占位文件。
7. 完成 `table` 与本地化规则配置后，确认项目具备 `CodexBatchVerify.RunLocalizeCreateAsset` 时再调用 `scripts/run_unity_task.py localize`；否则由开发者通过 Unity Editor 的 `LocalizeEditor.CreateLocalizeAsset()` 入口执行。首次资源生成应先用小范围样例核对生成位置和表条目，再处理完整资源树。
   - `scripts/run_unity_task.py localize` 会在执行前校验根目录下至少存在一个非 `Text` 的资源类型目录及语言目录；仅有空目录或文本目录时应先补齐资源范围，或改用 `init-localize`。
8. 文本通过 `Localize.GetText(...)` 接入，资源通过 `Localize.LoadAsset<T>(key)` 接入。
9. 预制体上的多语言组件挂接、引用绑定与最终表现校验由开发者手动处理；AI 负责前后配置、命名约定与代码接入。
10. 若发现新增本地化地区时，需同时检查文本目录与各资源类型目录下是否已有对应语言文件；若缺失，应由开发者按现有目录结构补齐对应语言文件或经确认的占位文件。

## 完成定义

- AI 完成：
  - 本地化规则接入、代码读取入口已补齐。
  - 需要初始化 Localize 时，已按 `LocalizeRules` 的既有入口执行。
  - 可自动执行的生成步骤已执行；若未执行，已说明原因与当前状态。
- 开发者完成：
  - 实际多语言资源提供、预制体上的本地化组件挂接、切语表现验收。
  - 需要在 Unity 编辑器内确认的资源引用与语言切换效果。
- 判定标准：
  - 目录结构、语言目录和资源类型目录清楚；
  - 文本与资源的读取入口已接通；
