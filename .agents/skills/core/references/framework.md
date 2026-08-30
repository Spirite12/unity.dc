# 框架层说明

## 定位

- `Assets/DCFrame/` 为框架层目录。
- 本文档用于记录框架能力、主要入口与使用边界。
- 业务开发优先在 `Assets/Game/` 扩展，并通过现有框架入口接入功能。

## 高频模块

以下内容按文件夹命名字母顺序排列，记录当前业务开发最常用的模块；未列出的模块不代表不存在或不可用，必要时仍需按目录继续排查。

- `Addressable`
  - 目录：`Assets/DCFrame/Modules/Addressable/`
  - 配置：`Assets/Game/Settings/Addressables/AARules.asset`
  - 用途：Addressable 分组规则、自动标记、AA 打包。
  - 使用提示：涉及资源分组、地址标记或打包规则时，优先先看对应配置资产；热更还要核对 `AAHotUpdateSettings.json`、Catalog 更新链路和上传工具配置。
- `Cache`
  - 目录：`Assets/DCFrame/Modules/Cache/`
  - 用途：本地缓存读写、版本控制、按账号类型保存。
  - 使用提示：涉及本地持久化或账号维度缓存时，优先沿现有缓存基类扩展；先确认 `Assets/Game/Scripts/Cache/CacheInit.cs` 已返回真实玩家、区服和账号标识。
- `Event`
  - 目录：`Assets/DCFrame/Modules/Event/`
  - 项目自定义事件入口：`Assets/Game/Scripts/Event/EventConst.cs`
  - 框架内置事件入口：`Assets/DCFrame/Modules/Event/EventFrame.cs`
  - 用途：统一声明和派发事件，当前最多支持 4 个参数。
  - 使用提示：新增项目业务事件时，优先在 `Assets/Game/Scripts/Event/EventConst.cs` 中补充；新增框架事件或者若要复用框架已有事件名，查看 `EventBase.Frame` 对应的 `Assets/DCFrame/Modules/Event/EventFrame.cs`。当前 `EventConst.cs` 默认是占位空类，不要把它误判为“项目没有事件系统”。
- `FSM`
  - 目录：`Assets/DCFrame/Modules/FSM/`
  - 用途：提供有限状态机、状态节点、转换条件与状态接口。
  - 使用提示：涉及角色、流程或界面状态切换时，优先评估是否可复用现有 FSM 节点与转换结构。
- `Localize`
  - 目录：`Assets/DCFrame/Modules/Localize/`
  - 配置：`Assets/Game/Settings/Localize/`
  - 用途：负责文本与资源本地化读取，文本来源统一接入 `table` 体系。
  - 使用提示：涉及文本或资源本地化时，先检查本地化配置与现有读取入口。
- `Pool`
  - 目录：`Assets/DCFrame/Modules/Pool/`
  - 用途：按池名统一管理运行时对象复用，支持预热、回收、清理与缓存数量查询。
  - 使用提示：涉及高频实例化/回收的运行时对象时，优先先定义好全局唯一的池名，再通过统一入口取出和回收。
- `RedTip`
  - 目录：`Assets/DCFrame/Modules/RedTip/`
  - 项目入口：`Assets/Game/Scripts/RedTip/`
  - 用途：负责红点树底层能力，项目侧在常量、树结构和实例映射中接入具体红点逻辑。
  - 使用提示：新增红点逻辑时，优先从项目侧常量、树结构和入口映射开始接入。
- `Singleton`
  - 目录：`Assets/DCFrame/Modules/Singleton/`
  - 用途：提供 `Singleton<T>` 与 `MonoSingleton<T>` 基类，供框架管理器和主入口对象复用。
  - 使用提示：新增全局管理器或唯一运行实例时，先判断是否适合复用现有单例基类。
- `Table`
  - 目录：`Assets/DCFrame/Modules/Table/`
  - 配置：`Assets/Game/Settings/Table/TableRules.asset`
  - 用途：负责表读取基类、导表规则、生成代码与科学计数法处理。
  - 使用提示：涉及配表或查表逻辑时，优先先看规则资产与生成结果，不直接绕过导表体系。
- `TextFilter`
  - 目录：`Assets/DCFrame/Modules/TextFilter/`
  - 用途：基于屏蔽词判断与替换。
  - 配置：`Assets/Game/Settings/TextFilter/TextFilter_global.txt`、`Assets/Game/Settings/TextFilter/TextFilter_<locale>.txt`
  - 使用提示：业务开发若需判断或替换敏感词，优先通过 `Assets/DCFrame/Modules/TextFilter/TextFilter.cs` 的现有接口接入；词库文本文件仅作为配置来源，不直接在业务代码中读取。
- `UGUI`
  - 目录：`Assets/DCFrame/UGUI/`
  - 用途：沉淀拖拽、滑动识别、滚动列表、页签、图片与文本效果等 UGUI 组件。
  - 使用提示：新增通用 UI 交互或表现组件时，先检查该目录是否已有可复用实现；业务界面逻辑仍优先落在 `Assets/Game/`。
- `UIManager`
  - 目录：`Assets/DCFrame/Modules/UIManager/`
  - 配置：`Assets/Game/Settings/UIManager/`
  - 用途：负责 UI 根节点、界面栈、层级排序、全屏与非全屏界面切换，以及多分辨率适配。
  - 使用提示：新增界面或调整界面行为时，优先沿现有 UI 基类和管理器体系扩展。
- `UniTask`
  - 插件目录：`Assets/Plugins/UniTask/`
  - 用途：项目主异步方案。
  - 使用提示：涉及异步流程时，优先沿项目现有的 `UniTask` 使用方式保持一致。
  - 参考位置：`Assets/DCFrame/Modules/Localize/Localize.cs`

## 主入口脚本

- `Assets/DCFrame/Main/MainFrame.cs`：框架主入口脚本。
- 负责承接框架级生命周期管理与核心能力接入。
- 涉及框架初始化、运行时调度或统一清理时，优先从该脚本确认入口。

## 运行时启动与热更新

- 主场景 `Assets/Game/Scenes/Main.unity` 的 `MainRoot` 同时挂载 `MainFrame` 与 `MainGame`：前者初始化 GC、屏蔽词、UI 与缓存基础设施，后者注册项目侧红点和缓存标识，并在启动后加载音频控制器。
- 新增启动异步流程时，必须明确与上述初始化的先后关系；不要仅依赖同一 GameObject 上 `Awake` 的隐式调用顺序。
- `HotUpdateBootstrapTest` 是独立测试辅助脚本，不应因文件存在就被视为生产启动链路。接入正式热更前，应明确 Catalog 更新、启动资源下载、失败回退和用户提示的责任边界。

## 高频工具目录

- `Assets/DCFrame/Utility/`：高频工具目录，供业务层和框架层复用通用能力。
- 当前主要包括字符串、文件、本地化、配表、时间等通用辅助能力。
- 适合沉淀无业务状态、可跨模块复用的辅助逻辑；不适合放具体业务规则或模块专属流程。
- `Assets/DCFrame/Foundation/`：框架基础运行时目录，当前包含 `GCCollect.cs` 与 `StepFlow.cs`。
- `StepFlow` 适用于单脚本内按步骤顺序推进的轻量流程控制；步骤通过 `AddStep(...)` 注册，通过 `CompleteStep()` 自动推进到下一步。
- `Assets/DCFrame/Editor/UGUI/`：UGUI 通用组件的编辑器扩展入口。

## 使用规则

- 开发前先检查对应模块在 `Assets/Game/Settings/` 下是否已有配置资产、规则或可复用示例。
- 优先复用项目已有封装与示例，不直接修改插件源码或框架底层实现。
- 业务需求优先在 `Assets/Game/` 实现，非必要不修改 `DCFrame`。
- `Assets/DCFrame/Foundation/`：适合沉淀框架级基础能力与轻量流程控制；新增或调整前需先告知开发者。
- `Assets/DCFrame/Utility/`：可按现有方式补充同类工具；修改前需先告知开发者。
- `Assets/DCFrame/Modules/`：默认只读；仅在需要沉淀通用能力时，且经开发者审核后，才允许修改。
