# 版本说明

- 请查看工程 Docs\Standard 文件版本说明；

# 0.1.0 

- 工程目录：
  - DCDrame ：框架内容
  - Docs ：工程文档说明
  - Game ：游戏工程内容
  - Plugins ：插件内容
- 导入包：
  - UniTask ：异步工具
  - Addressable ：AA包工具
- 功能：
  - AA包新增资源配置、资源导入设置功能；
    - 工程目录：Assets\DCFrame\Modules\Addressable
    - 文档：[链接](https://spirite12.github.io/post/frame/25.0115_addressable/)
  - 新增空文件夹检测、生成空文件夹占位文本代码；

# 0.2.0 

- 功能：
  - 接入 UIMgr 界面打开管理功能；
    - 工程目录：Assets\DCFrame\Modules\UIManager
    - 支持：预制件生成对应脚本、预制件引用标记、界面层级排序、ESC关闭界面、多分辨率显示、队列显示界面等等；
    - 文档：[链接](https://spirite12.github.io/post/23/23.01_uimgr/)
- 完善
  - AA包资源配置数据、完善资源导入标记AA功能；

# 0.3.0

- 功能：
  - 接入 Event 事件系统：
    - 工程目录：Assets\DCFrame\Modules\Event
    - 支持：按模块申明事件、事件最多支持4个参数，
    - 文档：[链接](https://spirite12.github.io/post/24/24.04_eventmanager/)
  - 接入 RedTip 红点系统：
    - 工程目录：Assets\DCFrame\Modules\RedTip
    - 支持：红点树管理、红点树查看器
    - 文档：[链接1](https://spirite12.github.io/post/24/24.05_redtip/)、[链接2](https://spirite12.github.io/post/24/24.06.07_redtip/)、[链接3](https://spirite12.github.io/post/24/24.06.29_redtip/)

# 0.4.0

- 功能
  - 新增 TextFilter 屏蔽词库；
    - 工程目录：Assets\DCFrame\Modules\TextFilter
    - 支持：读取屏蔽词库文件、判断与过滤屏蔽词汇
  - 新增 Cache 本地缓存功能；
    - 工程目录：Assets\DCFrame\Modules\Cache
    - 支持：根据账号类型读取、保存本地数据；
    - 文档：[链接](https://spirite12.github.io/post/22/22.08_cache/)
  - 新增动画优化脚本：AnimationOpEditor.cs；
- 导入包：
  - DoTween : 动效插件
