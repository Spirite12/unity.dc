# Table

## 关键目录

- `Assets/DCFrame/Modules/Table/`
- `Assets/Game/Table/`
- `Assets/Game/Scripts/Table/`
- `Assets/Game/Settings/Table/TableRules.asset`

## 表体系识别顺序

当任务涉及配表或查表，按这个顺序判断：

1. 看 `Assets/Game/Table/*.csv`，确认表数据来源和表名。
2. 看 `Assets/Game/Settings/Table/TableRules.asset`，确认表类型和生成规则。
3. 看 `Assets/Game/Scripts/Table/*.cs`，判断该脚本是否为导表生成结果。
4. 看 `Assets/DCFrame/Modules/Table/`，确认底层读取方式、表基类和科学计数法处理。
5. 若需要新增或修改表逻辑，优先改 CSV 和规则，再生成代码，不直接绕过生成体系手写一套。

## 代码参考

- `Assets/DCFrame/Modules/Table/TableBase.cs`
- `Assets/DCFrame/Modules/Table/TableBaseSingle.cs`
- `Assets/Game/Scripts/Table/TableConst.cs`
- `Assets/Game/Scripts/Table/TableEnum.cs`
- `Assets/Game/Scripts/Table/TableString.cs`

## 常见调用

- 常量表：
  - `TableConst.Test1`
- 枚举表：
  - `TableEnum.Instance.ColorTypeDic[TableEnum.ColorType.Yellow]()`
- 文本表：
  - `TableString.Instance.Test1`
- 默认表查表：
  - `TableTest.Instance.GetConfigById(1)`

## 表类型

- 默认表
  - 生成表字段类与查表函数。
  - 可对指定字段开启本地化。
- 常量表
  - 固定字段：`Id,Sign,Value,Desc`
  - 生成常量类。
- 枚举表
  - 固定字段：`Id,EnumSign,EnumName,Value,ValueSign,ValueName`
  - 可生成本地化枚举字典。
- 文本表
  - 用于承接代码文本和预制体文本的本地化来源。

## 生成表规则

- 先检查生成的表格是否在 `Assets\Game\Table`文件夹下是否已经存在相对应文件夹；
- 存在则结束生成；否则执行接下来步骤；
- 生成对应名的 `.csv` 的表格文件，并在里面填写字段名；
- 查看 `TableRules`内是否有对应的表规则，没有的话则添加，并处理相关数据，如：本地化，多key函数；字段关联，这些取决于是否有策划案；
- 如果处理好规则后，则自动帮忙点击`导当前表` 按钮，生成对应的表代码；

## 维护规则

- 开始改表前先检查 `Assets/Game/Settings/Table/TableRules.asset`。
- 优先通过 `TableRules` 工具生成通用代码。
- 需要新增查表函数时，先确认规则工具是否已支持对应模式。
- 生成代码在 `Assets/Game/Scripts/Table/`，不要只改生成结果而不改规则。
- 所有文本文件读取统一使用 UTF-8。

## 特殊问题

- 大数字注意 Excel 科学计数法，项目已有 `ScientificToLongConvert` 处理路径。
- 表字段如果涉及文本本地化，必须通过 `TableRules` 配置并生成对应的 Localization 数据，不手工绕过表体系新增文本来源。
