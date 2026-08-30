# 工程目录与模块入口

用于快速定位工程目录、模块入口与读写边界。

## 顶层目录

- `Assets/AddressableAssetsData`：Addressable 资源数据目录，默认不读、不改。
- `Assets/DCFrame/`：框架模块与工具代码，也是独立 Git 子模块；需同时关注父仓库记录版本与子模块当前版本。
- `Assets/Docs/`：版本、规范、记录等相关文档。
- `Assets/Game/`：业务开发文件夹。
- `Assets/Plugins/`：第三方插件目录。
- `Packages/`：Unity Package Manager 清单与锁定依赖。
- `ProjectSettings/`：Unity 版本、构建场景和平台配置入口。
- `Tools/`：导表模板、Addressables 上传等项目工具。

## 读写边界

以下标识用于说明目录权限：

- ①：只读，不改。
- ②：业务开发模式下，只可读。
- ③：框架开发模式下，只可读。

相关目录如下：

- `Assets/DCFrame/`：②
- `Assets/Docs/`：②、③
- 任意 `Editor/` 目录：②
- `Assets/Plugins/`：①

## 业务入口

- `Assets/Game/Localize/`：本地化文本与资源数据根目录；模板工程初始可不存在。文本表导出或开发者准备资源类型/语言目录后才会出现，不要仅为绕过校验而新建空目录。
- `Assets/Game/Prefabs/Frame/`：运行时 UI / 框架预制体入口。
- `Assets/Game/Scenes/Main.unity`：主场景。
- `Assets/Game/Scripts/Event/EventConst.cs`：项目事件声明入口。
- `Assets/Game/Scripts/Main/MainGame.cs`：游戏侧启动入口；与 `MainFrame` 同挂在主场景的 `MainRoot`。
- `Assets/Game/Scripts/Main/HotUpdateBootstrapTest.cs`：Addressables 热更测试辅助脚本；是否接入启动链路必须以场景挂载与显式调用为准。
- `Assets/Game/Scripts/Cache/CacheInit.cs`：账号、区服、玩家维度缓存标识的项目侧接入点。
- `Assets/Game/Scripts/RedTip/`：项目红点常量与根节点实现。
- `Assets/Game/Scripts/Table/`：生成后的表代码目录。
- `Assets/Game/Table/`：CSV 配表目录。
- `Assets/Game/Settings/Addressables/AAHotUpdateSettings.json`：本地热更开关配置；打包前由 Addressables 工具同步。

## 框架入口

- `Assets/DCFrame/Modules/Addressable/`：Addressable 资源规则与工具。
- `Assets/DCFrame/Foundation/Attribute/`：Inspector 辅助特性声明。
- `Assets/DCFrame/Modules/Cache/`：本地缓存。
- `Assets/DCFrame/Foundation/`：框架基础运行时辅助目录，当前包含 `GCCollect.cs` 与 `StepFlow.cs` 等基础能力入口。
- `Assets/DCFrame/Modules/Event/`：事件管理与框架事件基类。
- `Assets/DCFrame/Modules/Localize/`：文本与资源本地化读取入口。
- `Assets/DCFrame/Modules/Pool/`：按池名管理的对象池入口。
- `Assets/DCFrame/Modules/RedTip/`：红点树底层实现。
- `Assets/DCFrame/Modules/Singleton/`：单例基类入口。
- `Assets/DCFrame/Modules/Table/`：表读取基类、规则定义、科学计数法转换。
- `Assets/DCFrame/Modules/TextFilter/`：屏蔽词过滤。
- `Assets/DCFrame/Modules/UIManager/`：UI 栈、层级、适配、预制体引用工具。

## 工具入口

- `Assets/DCFrame/Editor/Foundation/CodexBatchVerify.cs`：Unity 命令行导表与本地化任务适配器；属于 `Assets/DCFrame` 子模块，修改后需核对子模块 SHA 与父仓库指针。
- `Tools/HotUpdate/UploadAddressables.ps1`：Addressables 构建产物上传工具。
- `Tools/HotUpdate/upload-addressables.temp.json`：上传配置模板。
- `Tools/HotUpdate/AAUploadData.json`：本机私有上传配置；应保持在忽略规则内，不应提交密钥路径、服务器或部署凭据。

## 插件目录边界

`Assets/Plugins/` 优先通过项目封装和示例接入，默认不做逐文件深入阅读，也不作为业务开发主战场；通常不直接修改该目录下文件。

### 当前插件目录

- `Assets/Plugins/AudioToolkit/`
  - 音效插件，项目接入入口位于 `Assets/Game/Settings/AudioToolkit/`
- `Assets/Plugins/CsvHelper/`
  - CSV 读取库，供 Table 模块使用
- `Assets/Plugins/Demigiant/`
  - 动效相关插件目录
- `Assets/Plugins/TextMesh Pro/`
  - TMPro 文本系统依赖
- `Assets/Plugins/UnityTimer/`
  - 计时器插件，提供运行时定时、取消、暂停与恢复能力
- `Assets/Plugins/UniTask/`
  - 项目主异步方案
