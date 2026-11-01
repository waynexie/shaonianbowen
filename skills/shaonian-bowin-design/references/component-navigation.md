# Component Navigation

导航组件决定页面身份、返回路径和安全区。它是跨端基础设施，不能手画平行家族。

## Source Scope

- 产品语境按 `source-frames.yaml` 的 `home_feed`、`article_detail`、`profile` 和 `source-registry.yaml use_for=paywall_interaction` 解析。
- 组件库页：`05 Navigation - Headers/Bars/Tabs`，依赖 `IconButton`、`Icon16/20/24`。

## Selection Rule

- 详情页、设置页、二级页：使用 `NavigationBar`。
- Full-screen sheet：使用 `NavigationBar Type=FullScreenSheetHeader`。
- 音频沉浸页：可使用轻导航或 `IconButton` 组合，但必须保留安全区、返回路径和关键标题/控制。
- 状态栏属于导航和安全区基础组件。只要页面需要展示状态栏，必须复用本地源状态栏实例或源同族变体；不得用 `Time`、`Battery`、`Wi-Fi`、`Service` 等 text/rectangle/ellipse/vector 本地重绘。

## Construction Contract

组件尺寸、当前可用性和完整状态读 `metadata/components.yaml` 对应条目；写前定点核验母版，不把本指南当实时库存。

- `HomeHeaderBar`: 左侧身份/标题区，右侧控制区，服务顶级频道定位。
- `NavigationBar`: 服务返回和当前页面标题；左右动作使用 `IconButton`，不能手画图标按钮。
- `BottomBar`: 外壳、安全区和阴影与内部选中项共同构成底部导航；可否新建实例及缺失时的处理按目录 fallback，不只复制 TabBar 后丢弃外壳。
- `TabBar`: 根据当前频道选择已登记状态；新频道先评估同族扩展，不按文案数量重建导航。
- `StatusBar`: 实例覆盖当前源页面宽度；不得用本地文本或图形拼出信号、电量和时间。
- Resizing: 标题区可替换文案，但长标题要缩短、换语义或截图检查，不让右侧控制被挤出。

## Style Contract

- 使用 `tokens.yaml` 中的文字、背景、阴影、圆角和 line tokens。
- 既有底部导航容器保留源阴影和顶部圆角；不要给普通 header 添加额外描边/投影。
- 右侧控制保持 IconButton 视觉和点击区，不使用字符、emoji 或临时图标。

## Variant Guidance

- 新顶级频道先扩展 `TabBar` active state；若需要独立复用底部外壳，先补齐正式组件，不创建本地平行家族。
- 沉浸页只允许弱化承载方式，不允许丢失导航语义。

## Allowed Local Layout

- 页面背景、顶部 mask、沉浸页浮层位置可以本地重组。
- Header、NavigationBar、TabBar、IconButton 必须实例化或扩展变体；既有 BottomBar 外壳必须来自完整源 Frame，不得手画。

## Interaction Handoff

本文件只定义导航组件和页面层级语义，不维护动效参数。

- 一级进入二级、详情、设置子页、账号子页、音频页面详情属于二级页面导航语境。
- 底部 Tab、频道切换、分段内容切换属于顶级内容切换语境，不等同于二级页面 push。
- 返回按钮、右侧 IconButton、Tab、Chip 属于基础点击反馈语境。
- 如需表达页面状态，静态设计稿只记录页面层级、进入入口、返回路径、选中态和关键状态节点。

## Validation

- `navigation_component_check`: 记录导航类型、源组件、active tab、是否有安全区。
- 状态栏实例检查（`registered_component_family_gate_check`）: 状态栏必须是组件实例或源同族变体；出现 `Source-compatible local`、`Time` + `Battery/Wi-Fi/Service` primitives、或本地绘制状态图标即失败。
- 顶级页必须检查 BottomBar 是否遮挡内容，主内容/CTA 至少在 BottomBar 上方留出安全距离。
- 详情/设置页检查返回按钮、标题、右侧控制是否对齐。
- 沉浸页检查导航和背景对比，不被舞台元素吞掉。
- `interaction_state_scope_check`: 需要表达页面状态时，记录导航交互语境、进入入口和状态节点。

## Anti-Patterns

- 手画标题栏、返回按钮或右侧 icon。
- 手画状态栏，或用命名为 `Source-compatible local` 的近似结构冒充状态栏组件。
- 在已有 BottomBar 外壳的源页面中删除外壳、只留下 TabBar。
- BottomBar 覆盖正文、评论输入、播放控制或 CTA。
- 产品 UI 中出现方案说明、组件名或设计解释。
