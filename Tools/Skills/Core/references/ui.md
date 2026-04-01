# UI

## 范围

- `Assets/DCFrame/Modules/UIManager/`
- `Assets/DCFrame/Modules/RedTip/`
- `Assets/Game/Prefabs/Frame/`
- `Assets/Game/Scenes/Main.unity`
- `Assets/Game/Scripts/RedTip/`
- `Assets/Game/Settings/UIManager/`
- `Assets/Game/Settings/AudioToolkit/`
- `Assets/Plugins/AudioToolkit/`

## UIManager

- 负责 UI 根节点、界面堆栈、层级排序、全屏与非全屏界面切换、ESC 关闭界面、多分辨率适配。
- 开发新界面时优先沿 `UIBase`、`UIBaseSingleton`、`UIMgr` 体系扩展。
- 非明确需求，不修改 `UIManager` 的 `Editor` 工具代码。

## 代码参考

- `Assets/DCFrame/Modules/UIManager/UIMgr.cs`
- `Assets/DCFrame/Modules/UIManager/UIBase.cs`
- `Assets/Game/Scripts/Main/MainGame.cs`
- `Assets/Game/Scripts/RedTip/RedTipConst.cs`
- `Assets/Game/Scripts/RedTip/RedTipMain.cs`

## RedTip

- 归类在 UI 模块，因为它属于界面状态提示体系。
- 项目侧入口：
  - `Assets/Game/Scripts/RedTip/RedTipConst.cs`
  - `Assets/Game/Scripts/RedTip/RedTipMain.cs`
- 开发规则：
  - 新增红点时，优先在项目侧常量、树结构和实例映射中声明。
  - 根节点初始化和销毁跟随 `MainGame` 生命周期。

## Audio Toolkit

- 归类在 UI / 表现层能力。
- 项目接入资源：
  - `Assets/Game/Settings/AudioToolkit/AudioControllerMain.prefab`
  - `Assets/Game/Settings/AudioToolkit/AudioObject.prefab`
- 启动入口：
  - `Assets/Game/Scripts/Main/MainGame.cs`
- 常见调用：
  - `AudioController.PlayMusic(...)`
  - `AudioController.Play(...)`
- 处理规则：
  - 配置优先在 `AudioControllerMain` 与现有分类中完成。
  - 非明确需求，不改插件底层。

## 常见调用

- 音效控制器启动加载：
  - `string path = Asset.GetPrefabPath("AudioToolkit/AudioControllerMain", Asset.PrefixPath.Settings);`
  - `GameObject prefab = await LoadAsset<GameObject>(path);`
- 背景音乐：
  - `AudioController.PlayMusic("audioId")`
- 普通音效：
  - `AudioController.Play("audioId")`

## Settings 入口

- `Assets/Game/Settings/UIManager/UIAutoRef.asset`
- `Assets/Game/Settings/UIManager/Icon/`
- `Assets/Game/Settings/AudioToolkit/`

## 开发规则补充

- 进入 UI 开发前，先检查 `Assets/Game/Settings/UIManager/` 和 `Assets/Game/Settings/AudioToolkit/` 是否已有现成配置可复用。
- 需要新增界面逻辑时，优先从现有 UI 基类、红点入口和音效预制体配置中找对应接入点。
