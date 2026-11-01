# Component Overlays

本文件统一描述少年博闻跨页面复用的弹出层模式，不替代页面 recipe。页面 recipe 决定当前任务为什么需要弹出层；本文件决定弹出层依附哪里、应该是哪一类、怎么扩展、怎么验收。

## Source Scope

产品页用于判断真实场景，组件库页用于确认正式组件、变体和复用入口。

- 产品语境按 `source-frames.yaml` 的 `home_feed`、`article_detail`、`profile` 与 `source-registry.yaml use_for=paywall_interaction` 解析。
- 组件库页：`13 Overlays - Sheets & Pickers`，以及相关按钮、图标、导航、音频组件页。
- Paywall examples: `source-registry.yaml use_for=subscription_modal` and `use_for=subscription_plan`.
- Floating examples: resolve `source-frames.yaml use_for=settings_sheets`, `use_for=article_function_sheet`, or the nearest matching live source state.
- Anchored examples: 正文词条解释气泡、文笔风格/深度版等控件锚定菜单，以 live Figma 中真实页面截图和同类节点为准。
- Ordinary Floating Sheet source: 字体、语言、普通选择等设置类 Sheet 先查 `source-index.md`、live Figma 同类页面和 `13 Overlays - Sheets & Pickers`，复用或扩展最近的源实例/组件变体；不得本地手画整张 Sheet。
- 组件复用适用于 `inspiration_draft`、`precision_draft` 和 `production`。`source_locked_visual_draft` 负责锁定背景，目标区弹层继续使用 `SheetPicker`、已有变体或最近同类源 Floating Sheet。
- 交付记录包含源组件/实例节点、交付实例/同族扩展节点、变体或属性修改以及弹窗态截图。

本文件解释弹层语义、接入关系和独有风险，不再单独要求一份报告；复用任务证据。尺寸约束以 `metadata/validation.yaml > bottom_sheet_type_check`、`anchored_popover_check` 为准，响应式解释集中在本文件 Responsive Adaptation 小节。

## Overlay Decision

先判断弹出层依附哪里，再判断视觉形态。

- `Paywall Half Sheet`: 付费、权益、解锁、购买、订阅、强转化。依附当前页面上下文，但以底部半屏承载购买决策。
- `Floating Sheet`: 普通选择、日历、分享、身份选择、字体选择、登录提示、轻确认、详情页轻量扩展。依附当前页面任务，以底部悬浮容器承载。
- `Definition Bubble`: 正文高亮词、概念解释、阅读辅助。依附文本锚点，必须贴近词条，不脱离阅读上下文。
- `Option Popover`: 小范围选项切换、下拉菜单、轻量设置。依附控件锚点，强调“这里有几个可选项”，不是一个独立任务面板。
- `Light Feedback`: Toast、短提示、临时反馈。只作为未来扩展边界，本轮不展开组件化细则。

不要因为内容较多就自动升级为 Paywall；内容多时先调整 Floating Sheet 高度和内部层级。不要因为用户要求“重新设计付费弹窗”就弱化为轻 picker；付费/解锁语义仍保持 Paywall Half Sheet，只发散套餐区、信息架构和决策路径。

## Paywall Half Sheet

用于付费权益、解锁、购买、订阅、强转化。

### Construction Contract

- 遮罩 + 贴屏底部半屏 Sheet。
- Sheet 左右贴屏，底部贴安全区，顶部大圆角，高度跟随源组件与内容；跨设备宽度见 Responsive Adaptation。
- 关闭按钮固定在右上角，尺寸、点击区、边距稳定；不得随内容漂移。
- 内部使用纵向 Auto Layout：标题/解锁理由、IP/权益区、套餐区、按钮区、协议/续费说明。
- 关闭按钮、Plus/IP、主按钮、协议说明是稳定 slot；套餐区允许本地重组。
- 主按钮唯一且强；取消、协议、续费、隐私为弱层级。
- Resizing: 套餐区价格、折算说明、协议文字、关闭按钮和底部安全区是重点检查区域。

### Style Contract

- 视觉重量高于 Floating Sheet，但仍保持冷静、产品原生，不做营销落地页。
- 可以使用 Plus/IP/权益插画，但服务购买决策，不做强促销装饰。
- 颜色、圆角、阴影、描边优先引用 `tokens.yaml`，不要复制全量 token。

## Floating Sheet

默认基础弹窗。普通、非强转化、非特殊强调的底部弹层都走它，包括但不限于普通选择、日历、分享、身份选择、字体选择、登录提示、轻确认、详情页轻量扩展。

### Construction Contract

- 遮罩 + 四周留边的浮动底部 Sheet。
- 四周保留呼吸感，四角圆角完整；宽屏底部居中，不随屏幕无限拉伸，尺寸关系见 Responsive Adaptation。
- Root 使用纵向 Auto Layout，高度由内容驱动；紧凑选项较低，登录/身份/详情扩展可更高。
- 内容 slot 可为列表、宫格、单选项、分享入口、简单说明、轻确认动作。
- 字体、语言、身份、普通选项等已有源参考时，必须从 `Sheet & Picker` 组件或最近同类源 Floating Sheet 实例出发替换文本/选项；不得用本地 Frame 加多个 option row 近似拼出。
- 问候语、地区、语言、身份、字体和其他设置项统一按普通选择语义处理，从 `Sheet & Picker` 或最近同类源 Floating Sheet 扩展内容 slot。
- 选项列表使用纵向 Auto Layout；选项行共享左列文字起点、右侧状态/勾选区和稳定行高；最后一项下方保留底部呼吸空间，不贴底、不溢出。
- Resizing: 长选项、长说明、带主按钮状态和底部安全区必须检查。

### Calendar Sheet

- 日历属于 Floating Sheet，不因内容较多升级为 Paywall。
- 日历外层遵循 Floating Sheet 规则，内部 7 列网格保持紧凑，不为填满容器强行拉宽日期 cell。
- 日期 cell 建议保持约 `36-40px` 的视觉节奏；列间距可轻微变化，但不要横向拉大日期格子去填满宽屏。
- 宽屏时让日历内容居中，而不是拉伸网格。

## Anchored Popover

Anchored Popover 是跟随触发词或控件出现的锚点浮层。它不是底部 Sheet，也不是营销卡片；核心判断是“用户刚刚点了哪里，浮层是否仍然和这个锚点保持清楚关系”。

### Shared Construction Contract

- 必须记录并呈现清晰锚点：文本高亮词、按钮、标签、segmented control、icon control 等。
- Popover 优先贴近锚点，上/下/左/右根据可用空间选择；靠边时翻转或偏移。
- 与屏幕边缘保持至少 `20px` 安全边距。
- 不遮挡锚点本身；不得覆盖用户下一步必须阅读或点击的关键路径。
- 宽度不随屏幕无限拉伸。正文解释气泡最大不超过正文内容列宽或安全内容区；选项 Popover 按内容 hug，但保证可点击宽度。
- 内容放不下时，优先翻转方向、缩短高度或折行；仍不合适时改用 Floating Sheet。
- Root 使用 Auto Layout；不要用 Group 或绝对定位硬堆文本和箭头。
- 气泡 surface 和箭头/尖角必须构成一个视觉整体：优先放在同一个 top-level overlay Frame 内，或使用同一个已验证组件/同族变体；不得把箭头和气泡作为两个彼此漂移的独立元素交付。
- 箭头 tip 必须指向锚点中心或可解释的锚点边缘，箭头 base 必须贴合气泡边缘；截图中看起来分离、悬空或错位即失败。
- Anchored Popover 是覆盖层状态，必须置于页面内容之上；不得插入页面主内容 Auto Layout 栈、不得把音频条/正文/卡片往下挤，也不得改变底层页面模块位置。
- production_mode 的局部气泡状态只能新增/修改 popover overlay 及必要的锚点高亮；页面背景、导航、音频、内容列表、底栏等未被点名区域是 locked regions，必须保持源稿变量、组件和位置。
- 如果同类气泡会反复使用，应沉淀为 `AnchoredPopover` / `GuideBubble` 组件或同族变体，暴露 `slot/Title`、`slot/Body`、`slot/Arrow`、`AnchorSide`、`Tone` 等属性；在正式组件缺失前，可按本规则做 source pattern，但必须通过截图门禁。
- 可以有箭头、尖角或视觉连接符，但不能为了装饰破坏阅读和点击。

### Definition Bubble

用于正文高亮词解释、概念说明、阅读辅助。

- 必须贴近正文词条锚点，保持“解释这个词”的关系。
- 可用品牌绿或浅绿强调，但不能像付费权益卡或营销卡。
- 内容短而集中：词条名、1-2 行解释、必要时一个弱动作。
- 优先不遮挡后续正文阅读路径；如果遮挡不可避免，应放在锚点上方/下方更少干扰的位置。
- 解释内容过长、包含列表、需要多步阅读或操作时，转为 Floating Sheet，不强塞进气泡。

### Option Popover

用于文笔风格、深度版切换、小范围选项菜单和轻量设置。

- 跟随控件锚点，用户能一眼看出菜单属于哪个控件。
- 白底、轻阴影、`20px` 圆角，视觉轻于 Floating Sheet。
- 当前项高亮，未选项保持安静；选项文字左对齐，行高和点击区稳定。
- 宽度按内容 hug，但不要小到点击困难；长选项优先换行或改用 Floating Sheet。
- 选项超过一屏、包含复杂说明或需要确认按钮时，不再使用 Option Popover。

## Light Feedback

Toast、短提示、临时反馈属于 Light Feedback。本轮只定义边界：

- 用于系统状态、操作结果、短时提醒。
- 不承载选择、不解释复杂内容、不替代 Sheet 或 Popover。
- 静态设计只记录触发入口、出现位置和状态语义；运行时动效参数不在本 skill 维护。

## Responsive Adaptation

不同设备适配先看弹出层语义，再看内容舒适宽度。

Paywall Half Sheet:

- 外层 Sheet: `width = 100vw`，左右贴屏，保持强承载和强转化语义。
- 内部内容: `max-width: 390-430px`，居中；套餐区、按钮和协议说明不因屏幕变宽而无限拉伸。
- 宽屏时优先增加两侧空白或内容居中，不改变关闭按钮右上语义位置。

Floating Sheet:

- 默认外层: `width = min(100vw - 40px, 400px)`，底部居中，保留左右和底部呼吸感。
- 上式用于解释 `bottom_sheet_type_check` 的宽度约束，不另外维护逐设备尺寸表；特殊大屏组件需明确需求和源依据。
- 大屏上不要为了填满宽度而拉伸选项、图标宫格或日历网格；高级感来自居中、留白和克制宽度。

Anchored Popover:

- 优先以锚点中心或边缘定位；根据可用空间选择上/下/左/右。
- 保持至少 `20px` 屏幕边距。
- 放不下时翻转方向；仍放不下则改用 Floating Sheet。
- 宽屏上仍按内容和正文列宽决定尺寸，不变成居中大卡片。

## Variant Guidance

- 套餐区可以是横排卡片、无框价格清单、分段选择、推荐摘要、权益优先、单推荐 + 次级入口。
- 探索模式必须改变信息架构、承载方式、决策路径或视觉组织，不能只改卡片尺寸、颜色或间距。
- 普通选择优先列表或选项行，保持左列对齐和稳定行高。
- 分享类可用宫格或图标入口，但不要变成营销卡片。
- 登录提示可带主按钮，但视觉重量仍低于 Paywall Half Sheet。
- 高度增长时优先保持内部 Auto Layout 和安全区，不靠裁切、挤压或缩小关键文字解决。
- 宽度增长时优先使用 max-width 和内容居中；不要让 Floating Sheet 或日历/分享/身份选择无限拉伸。
- 新变体优先扩展 `Sheet & Picker` / source subscription structure / Anchored Popover source pattern，不创建平行 overlay family。
- 如果是语言/字体这类普通设置弹窗，优先复用最近同类源 Floating Sheet 或 `Sheet & Picker Type=FontPickerSheet/OptionPickerSheet`，再改文案和选项；不可创建 `Overlay / ... Floating Sheet` 本地平行家族。

## Resizing Risks

- 套餐价格和折算说明容易因为卡片宽度不足裁切。
- 协议/隐私/续费说明容易被按钮区挤压。
- Paywall 关闭按钮容易随内容漂移，必须固定在右上语义位置。
- Floating Sheet 长列表容易贴底或丢失底部呼吸感。
- Floating Sheet 在大屏上容易因全宽拉伸而显得空散，必须限制最大宽度。
- 日历网格容易被错误拉宽，导致日期 cell 空、散、难扫读。
- 普通选项行右侧值和左侧标签必须保持清晰列对齐。
- Definition Bubble 容易遮挡正文或脱离高亮词，必须检查锚点关系。
- Option Popover 靠近屏幕边缘时容易溢出或压缩选项，必须检查翻转/偏移。

## Interaction Handoff

本文件只定义弹出层的设计类型和状态语义，不维护动效参数。

- 交互语境沿用 Overlay Decision 的语义分类，不重复建立另一套类型。
- 如果任务要求表达交互状态，静态设计稿只记录触发入口、open/closed 状态、组件语境和视觉约束。
- 静态 Figma 可交付 open/closed、selected/unselected 等状态节点，但不要在组件文档或页面说明里复制 duration、easing、scale、translate、opacity 参数。

## Validation

交付前必须检查：

- 弹层类型与语义: 先记录弹出层类型和语义原因。
- `bottom_sheet_type_check`: 普通弹层是 Floating Sheet；付费/解锁/购买是 Paywall Half Sheet。
- `anchored_popover_check`: Definition Bubble / Option Popover 必须有清晰锚点、位置避让和边界检查。
- 边缘与留边: Floating Sheet 有左右和底部留边；Paywall Half Sheet 左右贴屏；Anchored Popover 保持 `20px` 屏幕边距。
- 响应式宽度（`responsive_layout_check`）: Paywall 外层可拉通但内容 max-width 居中；Floating Sheet 使用 max-width，不在大屏上无限拉伸；Popover 不变成大屏居中卡片。
- 关闭入口位置: Paywall 关闭按钮位置和尺寸稳定；Floating Sheet 只在需要时出现关闭入口。
- 内边距与裁切: 标题、价格、协议、按钮、选项行、气泡解释文本无裁切、异常 padding 或拥挤。
- 对齐栅格: 左列标签、右列价格/值、按钮和协议说明有清晰对齐关系。
- 组件实例来源（`registered_component_family_gate_check`）: 当源文件已有同类 Floating Sheet 或 `Sheet & Picker` 变体时，交付节点必须是组件实例、源实例复制后的同族扩展，或报告阻塞；本地 Frame 拼装视为失败。
- `interaction_state_scope_check`: 如需表达交互状态，记录对应 overlay 语境、触发入口和状态节点。
- 关键区域放大（`screenshot_visual_check`）: 全屏截图之外，必须放大检查价格/协议/关闭按钮/选项行/Popover 边缘和锚点关系。

## Anti-Patterns

- 把普通选择、字体、身份、分享等基础弹窗做成贴屏 Paywall Half Sheet。
- 把付费权益、解锁、订阅做成轻量 picker，削弱购买决策。
- 套餐列表每项都框起来但没有更清楚的决策路径。
- 关闭按钮随内容漂移，或点击区小于源组件语义。
- Floating Sheet 左右留边错、底部贴死、圆角不完整。
- 大屏上把 Floating Sheet、日历、分享、身份或字体选择完全拉通，导致内容空散。
- 日历日期格子横向拉宽以填满屏幕，而不是保持紧凑网格并居中。
- Popover 没有明确锚点，看起来像随机漂浮卡片。
- Definition Bubble 遮挡正文关键阅读路径，或解释内容过长导致裁切。
- Option Popover 做成底部 Sheet、营销卡片，或没有当前项高亮。
- 靠边 Popover 溢出屏幕、贴边小于 `20px`，或覆盖触发控件。
- 在设计组件文档里复制一套弹出层动效参数，导致与 motion skill 漂移。
- 价格、折算说明、协议文字、选项内容裁切或左右列不齐。
- 在产品 UI 中写入方案名、设计解释或组件类型标签。
- 源文件已有普通 Floating Sheet 时，仍用本地 `Sheet Header`、`Language Options`、`Option / ...` 等 Frame 拼完整弹窗。
- 普通设置类 Sheet 的最后一项贴底、选项列表被容器裁切、或底部安全区/呼吸空间消失。
