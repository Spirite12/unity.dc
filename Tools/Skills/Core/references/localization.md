# Localization

## 范围

- `Assets/DCFrame/Modules/Localize/`
- `Assets/Game/Settings/Localize/`
- `Assets/Game/Localize/`
- `Assets/Game/Table/`
- `Assets/Game/Scripts/Table/`

## 文本本地化

- 文本本地化来源统一来自 `table` 表。
- 生成结果统一进入 Localization 的字符串资源体系。
- 不允许在其他地方单独新增一套文本本地化来源。

### 主要来源

- 默认表：对勾选字段生成 `Localize.GetText(...)`
- 枚举表：对勾选枚举生成本地化字典
- 文本表：承接代码文本与预制体文本
- 常量表：不参与文本本地化

### 关键 key 规则

- 默认表字段：`表名.字段名.Id`
- 枚举表：`表名.枚举名.枚举值名`
- 文本表：`表名.Sign`

### 使用规则

- 新增文案时，先判断应该落到默认表、枚举表还是文本表。
- 不要在代码里长期写死用户可见文案。
- 预制体文本优先通过现有 Localization 组件与工具接入。

### 代码参考

- `Assets/DCFrame/Modules/Localize/Localize.cs`
- `Assets/Game/Scripts/Table/TableString.cs`
- `Assets/Game/Scripts/Table/TableEnum.cs`

- `Assets/Game/Scripts/Main/MainGame.cs`

### 常见调用

- 文本：
  - `Localize.GetText("TableString.Test1")`

## 资源本地化

- 统一通过 `Localize.LoadAsset<T>(key)` 加载。
- 当前 `Localize.AssetTableNameDic` 已支持相关类型；

### 资源组织规则

- `Assets/Game/Localize/` 下按资源类型建目录。
- 每种资源类型下按语言建目录，如 `Zh-CN`、`En`。
- 通过现有本地化资源生成工具生成表与 Shared Data。

### 代码参考

- `Assets/DCFrame/Modules/Localize/Localize.cs`
- `Assets/Game/Scripts/Main/MainGame.cs`

### 常见调用

- 预制体：
  - `await Localize.LoadAsset<GameObject>("SomePrefabKey")`

### Settings 入口

- `Assets/Game/Settings/Localize/Localization Settings.asset`
- `Assets/Game/Settings/Localize/LocalizeRules.asset`
