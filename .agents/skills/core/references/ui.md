# UI说明

## 定位

- 本文档用于说明 UI 相关业务代码的处理顺序，以及常见联动模块的接入方式。
- UI 业务开发优先沿项目现有框架扩展；业务新增内容优先放在 `Assets/Game/` 下，不单独新增一套界面管理逻辑。

## UI联动模块

- `UIManager`
  - 在 UI 内负责界面根节点、界面栈、层级排序、界面切换、ESC 关闭界面与分辨率适配。
  - 读取：优先看当前文档与 `framework.md`。
  - 接入位置：
    - `Assets/Game/Prefabs/`：界面预制体所在位置；
    - `Assets/Game/Scripts/Script/`：界面逻辑层对应的脚本约定目录；
    - `Assets/Game/Scripts/Mono/`：预制体对应物体的绑定脚本；
  - 接入提示：当前 UI 创建工具默认将界面逻辑脚本输出到 `Assets/Game/Scripts/Script/`；处理界面相关脚本时，以该目录和 `Assets/Game/Scripts/Mono/` 为主要落点。
- `RedTip`
  - 在 UI 内负责界面红点显示、红点树挂接与状态刷新。
  - 读取：优先看当前文档与 `framework.md`。
  - 接入位置：
    - `Assets/Game/Scripts/RedTip/RedTipConst.cs`：红点常量声明脚本；
    - `Assets/Game/Scripts/RedTip/RedTipMain.cs`：红点主入口脚本；
    - `Assets/Game/Scripts/RedTip/`：各系统模块都应在此目录下有对应系统目录，并在其中放对应红点脚本；
    - `Assets/Game/Scripts/Script/`：当前 UI 创建工具默认生成的界面逻辑脚本目录；若界面逻辑在此目录下，需要监听红点激活事件并做对应显示；
- `AudioToolkit`
  - 在 UI 内负责界面音效、背景音乐与表现层常用音效播放。
  - 读取：优先看当前文档。
  - 接入提示：默认不主动新增音效接入；仅当需求明确包含按钮音效、背景音乐或表现层音效时，再读取 `Assets/Game/Settings/AudioToolkit/` 与实际调用点。
- `Event`
  - 在 UI 内负责界面状态同步、跨模块通知与交互事件派发。
  - 读取：查看 `framework.md` 中的 Event 说明。
  - 接入位置：
    - `Assets/Game/Scripts/Event/`：项目自定义事件声明与业务事件入口。
  - 接入提示：`Assets/Game/Scripts/Event/EventConst.cs` 当前是占位空类；新增业务事件时在这里补充。框架内置事件名需查看 `EventBase.Frame` 对应的 `Assets/DCFrame/Modules/Event/EventFrame.cs`。
- `Localize`
  - 在 UI 内负责界面文案、图片与多语言资源接入。
  - 读取：查看 `localization.md`。
  - 接入位置：
    - `Assets/Game/Localize/`：本地化资源存放位置。
    - 界面文本来源优先联动 `table` 与现有本地化入口。
  - 接入提示：若需求首次涉及资源本地化，按 `localization.md` 中 `LocalizeRules` 的初始化流程执行，再继续资源映射和代码接入。
- `Table`
  - 在 UI 内负责展示配置、文案来源与查表逻辑支持。
  - 读取：查看 `table.md`。
  - 接入位置：
    - `Assets/Game/Scripts/Table/`：生成代码与查表入口；
- `Addressable`
  - 在 UI 内负责资源加载路径、资源组织与打包规则联动。
  - 读取：查看 `framework.md` 中的 Addressable 说明。
  - 接入位置：
    - 读取 `Assets/DCFrame/Modules/Addressable/Asset.cs`，按现有封装生成资源地址。
  - 接入提示：UI 预制体默认通过 `Asset.GetPrefabPath(AssetPath + \"/\" + AssetName)` 生成地址；默认前缀是 `Assets/Game/Prefabs/`。若读取设置资源等非 UI 预制体资源，需显式传入对应 `PrefixPath`，不要手写拼接路径。
- `Cache`
  - 在 UI 内负责本地保存、账号维度状态与设置记忆类需求。
  - 读取：查看 `framework.md` 中的 Cache 说明。
  - 接入位置：业务侧缓存初始化与相关接入优先放在 `Assets/Game/Scripts/Cache/`。
- `TextFilter`
  - 在 UI 内负责输入框、昵称、聊天等用户可输入内容的敏感词处理。
  - 读取：查看 `framework.md` 中的 TextFilter 说明。
  - 接入位置：
    - `Assets/DCFrame/Modules/TextFilter/TextFilter.cs`：仅在涉及相关功能时，再读取该脚本；

## 业务开发顺序

1. 按照 UI 联动模块内容，从策划案中拆出对应的功能需求；
2. 查看配置数据 `Table` 是否已经处理好；未处理好则跳转到 `table.md` 文档内处理；
3. 查看本地化数据 `Localize` 是否已经处理好；未处理好则跳转到 `localization.md` 文档内处理；
4. 若需要新增本地缓存，则创建对应功能的 `Cache`。
5. 若需要新增红点，先补项目侧常量、树结构和入口映射，再接入界面显示逻辑；不要直接改红点底层。
6. 当联动模块都处理完后，若需要处理界面逻辑，优先由 AI 处理界面脚本，以及对应联动模块的调用；界面预制体的具体拼装、层级摆放和最终表现校验由开发者手动处理。
   - `Event`、`TextFilter`、`Addressable`：这些模块需要在处理界面逻辑时同步考虑。

## 完成定义

- AI 完成：
  - 界面脚本已落到 `Assets/Game/Scripts/Script/` 或 `Assets/Game/Scripts/Mono/` 的对应位置。
  - 界面涉及的 `Table`、`Localize`、`Event`、`RedTip`、`Cache` 等代码接入已补齐。
  - 若存在可自动执行的生成步骤，已执行或已说明未执行原因。
- 开发者完成：
  - 预制体拼装、层级摆放、Inspector 引用绑定、最终表现验收。
  - 需要在 Unity 内手动确认的界面开关、资源引用与视觉效果。
- 判定标准：
  - 界面打开链路、脚本落点与依赖模块入口明确；
  - 人工处理项已单独列出，不与 AI 已完成内容混写。

