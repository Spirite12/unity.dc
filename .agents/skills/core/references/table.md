# 配表与导表说明

## 定位

- 本文档用于说明配表、表规则、生成代码、查表体系与表业务代码的处理顺序。
- 本项目的表逻辑优先通过 `CSV + TableRules + 生成代码` 完成，不手工绕过现有导表体系。

## 关键目录

- `Assets/Game/Table/`：`CSV` 配表目录，表数据源优先从这里确认。
- `Assets/Game/Settings/Table/TableRules.asset`：导表规则与表类型配置入口。
- `Assets/Game/Scripts/Table/`：导表生成结果与项目侧查表入口。
- `Assets/DCFrame/Modules/Table/`：表读取基类、底层规则。

## 表类型

- 默认表
  - 生成表字段类与查表函数。
  - 可对指定字段开启本地化。
- 常量表
  - 固定字段：`Id,Sign,Value,Desc`
  - 生成常量类。
- 枚举表
  - 固定字段：`Id,EnumSign,EnumName,Value,ValueSign,ValueName`
  - 可生成相关枚举和本地化枚举字典。
- 文本表
  - 固定字段：`Sign,String`
  - 用于承接代码文本与预制体文本的本地化来源。

## 业务开发顺序

1. 先从策划案中拆出表清单、字段结构、主键规则，以及是否涉及枚举、多 key 和文本本地化。
2. 检查 `Assets/Game/Table/` 下是否已有对应 `CSV`；有则优先在原表上扩展，没有再新增表。
3. 新建或修改 `CSV` 时，保持第一行为字段名、第二行为字段注释、第三行开始为配置数据；若任务未明确要求核对具体配置值，不必逐行深读数据内容。
4. 检查 `Assets/Game/Settings/Table/TableRules.asset` 是否已有对应规则；若没有，则补充表类型、本地化、多 key 与字段关联等配置。
5. 表字段若涉及文本本地化，必须通过 `TableRules` 勾选本地化配置并生成对应的 Localization 数据，再联动 `localization.md` 处理接入。
6. 规则确认后，通过现有工具执行导表，生成 `Assets/Game/Scripts/Table/` 下的表代码；优先调用 `scripts/run_unity_task.py table` 执行全量导表；若脚本不可用，再回退到 Unity Editor 内的 `TableEditor.PackageConfig()` 入口；不要把手改生成结果作为最终方案。
7. 若需要新增查表函数，先确认规则工具是否已支持对应模式；若暂不支持，再在生成脚本的 `#region 自定义内容` 与对应 `#endregion` 之间补充函数。

## 补充规则

- 大数字字段要注意 Excel 科学计数法，必要时检查现有 `ScientificToLongConvert` 处理路径。

## 完成定义

- AI 完成：
  - `CSV`、`TableRules.asset` 与生成代码接入关系已补齐。
  - 导表步骤已执行；若未执行，已明确说明原因与当前状态。
  - 若有自定义查表函数，已按现有生成规则落到正确位置。
- 开发者完成：
  - 配置值的业务正确性确认，以及策划数据本身的最终审核。
- 判定标准：
  - 表名、规则名、生成结果目录三者一致；
  - 需要本地化的字段已在规则中明确；
