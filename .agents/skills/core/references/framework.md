# Framework

## 定位

- `Assets/DCFrame/` 是框架层，默认只读；
- 这里只记录框架能力、入口和使用边界，不把框架拆成多个 skill。
- 业务开发优先在 `Assets/Game/` 扩展，通过现有框架入口接入功能。

## 当前关注模块

- `Addressable`
  - 目录：`Assets/DCFrame/Modules/Addressable/`
  - 配置：`Assets/Game/Settings/Addressables/AARules.asset`
  - 用途：Addressable 分组规则、自动标记、AA 打包。
- `Cache`
  - 目录：`Assets/DCFrame/Modules/Cache/`
  - 用途：本地缓存读写、版本控制、按账号类型保存。
- `Event`
  - 目录：`Assets/DCFrame/Modules/Event/`
  - 项目事件入口：`Assets/Game/Scripts/Event/EventConst.cs`
  - 用途：统一声明和派发事件，当前最多支持 4 个参数。
- `TextFilter`
  - 目录：`Assets/DCFrame/Modules/TextFilter/`
  - 配置：`Assets/Game/Settings/TextFilter/TextFilter.txt`
  - 用途：基于屏蔽词判断与替换。
- `UniTask`
  - 插件目录：`Assets/Plugins/UniTask/`
  - 用途：项目主异步方案。
  - 当前示例调用：
    - `Assets/DCFrame/Modules/Localize/Localize.cs`

## 代码参考

- `Assets/Game/Scripts/Main/MainGame.cs`
- `Assets/Game/Scripts/Event/EventConst.cs`
- `Assets/DCFrame/Modules/Localize/Localize.cs`
- `Assets/DCFrame/Modules/UIManager/UIMgr.cs`

## 使用规则

- 开发前先检查对应模块在 `Assets/Game/Settings/` 下是否已有配置资产。
- 优先用项目已有封装和示例，而不是直接进插件源码或框架底层改。
- 事件常量放项目侧 `EventConst`，不要把项目事件直接塞进框架基类。
- 继续沿用 `UniTask`，不要额外引入另一套异步框架。
- 若需求能在业务层完成，不向 `DCFrame` 反向补新能力，除非以下情况：
  - `Assets/DCFrame/Utility/` ：是工具文件夹，可添加同类脚本，新增函数；修改此处需告知开发者；
  - `Assets/DCFrame/Modules/`：文件夹下除非有特别通用的代码需要添加，否则只读；修改此处需要先让开发者审核后，才能修改；
