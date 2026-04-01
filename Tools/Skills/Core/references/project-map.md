# 工程目录总览

## 顶层结构

- `Assets/DCFrame/`：框架模块与少量工具代码。
- `Assets/Game/`：业务脚本、配置、场景、预制体、表、本地化资源。
- `Assets/Docs/`：版本、规范、记录文档，只读。
- `Assets/Plugins/`：第三方插件目录，默认只做轻量说明与接入参考，不作为业务开发主战场。

## 主要业务入口

- `Assets/Game/Scenes/Main.unity`：主场景。
- `Assets/Game/Prefabs/Frame/`：运行时 UI / 框架预制体入口。
- `Assets/Game/Scripts/Main/MainGame.cs`：游戏启动入口。
- `Assets/Game/Scripts/Event/EventConst.cs`：项目事件声明入口。
- `Assets/Game/Scripts/RedTip/`：项目红点常量与根节点实现。
- `Assets/Game/Scripts/Table/`：生成后的表代码目录。
- `Assets/Game/Table/`：CSV 配表目录。
- `Assets/Game/Localize/`：本地化文本与资源数据目录。

## 框架模块入口

- `Assets/DCFrame/Modules/UIManager/`：UI 栈、层级、适配、预制体引用工具。
- `Assets/DCFrame/Modules/Table/`：表读取基类、规则定义、科学计数法转换。
- `Assets/DCFrame/Modules/Localize/`：文本与资源本地化读取入口。
- `Assets/DCFrame/Modules/Event/`：事件管理与框架事件基类。
- `Assets/DCFrame/Modules/Cache/`：本地缓存。
- `Assets/DCFrame/Modules/Addressable/`：Addressable 资源规则与工具。
- `Assets/DCFrame/Modules/TextFilter/`：屏蔽词过滤。
- `Assets/DCFrame/Modules/RedTip/`：红点树底层实现。

## 只读优先区

- `Assets/Docs/`
- `Assets/DCFrame/`
- `Assets/Plugins/`
- 任意 `Editor/` 目录

## Plugins

`Assets/Plugins/` 优先通过项目封装和示例使用插件，默认不做深度逐文件阅读，不作为业务开发主战场，也不对此目录下文件做修改；

### 当前插件目录

- `Assets/Plugins/AudioToolkit/`
  - 音效插件，项目接入入口在 `Assets/Game/Settings/AudioToolkit/`
- `Assets/Plugins/CsvHelper/`
  - CSV 读取库，供 Table 模块使用
- `Assets/Plugins/Demigiant/`
  - 动效相关插件目录
- `Assets/Plugins/TextMesh Pro/`
  - TMPro 文本系统依赖
- `Assets/Plugins/UniTask/`
  - 项目主异步方案
