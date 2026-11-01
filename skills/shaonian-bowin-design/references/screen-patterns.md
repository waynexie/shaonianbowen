# Screen Patterns

本文件是页面体验与扩展经验的唯一权威源。按 `profile_id` 读取当前任务对应小节；不要为一个任务加载全部 profile。节点定位见 `source-frames.yaml`，生产装配见 `page-recipes.md`，组件结构见对应 `component-*.md`。

每个 profile 只描述可迁移的体验目标、视觉节奏、Surface 语法和扩展判断，不记录节点 ID、逐像素尺寸、完整 token 值或组件内部结构。具体状态继承页面家族，只在 `State Deltas` 记录变化与锁定项。

## Home Feed

`profile_id: home_feed`
`status: confirmed`

- **Experience Goal**：让用户低压力地理解今日内容，并快速决定先读哪一条。
- **Visual Thesis**：轻背景承托清晰内容单元，资讯判断始终强于功能入口和运营提示。
- **Cognitive Flow**：日期/问候 → 今日上下文 → 内容标题与封面 → 来源/推荐信号 → 次要统计与动作。
- **Focus Curve**：首屏先建立“今天有什么”，随后进入稳定扫描节奏；列表中不要反复制造新主视觉。
- **Surface Grammar**：独立资讯使用内容卡；连续上下文和轻提醒优先无框、信息条或弱 surface，不再套一张大卡。
- **Module Roles**：Header 提供频道位置感，音频/日期建立当日上下文，News Card 承担内容决策，BottomBar 负责顶级导航。
- **Extension Heuristics**：新增模块先判断是否帮助选内容；高频连续任务放在首屏上下文区，单条内容动作进入卡片，低频工具进入弱入口。
- **State Deltas**：`base` 保持完整信息流；`empty` 保留页面骨架并将焦点收束为说明与下一步；`scrolled` 只改变滚动关系和头部显隐，不重绘组件。
- **Must Keep**：今日内容优先、稳定列表节奏、Header/BottomBar 语义、来源可信度。
- **Can Vary**：内容分组、主题聚类、轻提醒位置、当日上下文承载方式。
- **Avoid**：营销 Hero、通用新闻墙、每个功能独立浮卡、提醒模块抢过资讯标题。

## Article Detail

`profile_id: article_detail`
`status: confirmed`

- **Experience Goal**：让用户不被工具打断地完成阅读，并在需要时进入音频、学习和讨论。
- **Visual Thesis**：正文是连续主表面，辅助能力沿阅读路径逐级出现，不与标题和正文争夺首要注意力。
- **Cognitive Flow**：标题/来源 → 正文阅读 → 音频或解读 → 学习模块 → 相关内容/观点 → 评论。
- **Focus Curve**：标题区建立判断，正文维持稳定低噪声；学习与评论只在阶段节点提高视觉重量。
- **Surface Grammar**：正文无框连续；摘要、影响解释和学习模块可有容器；相关入口使用 Cell；评论形成独立尾部区域。
- **Module Roles**：导航保证返回，正文承载主任务，音频提供替代消费方式，学习工具深化理解，观点和评论提供外部视角。
- **Extension Heuristics**：新增功能先判断是否改变阅读、解释内容或触发讨论；阅读内辅助贴近相关段落，完整工具进入独立功能层，弱入口不得插断正文。
- **State Deltas**：`base` 保持完整阅读流；`empty` 保留导航与恢复路径；`no_comments` 只替换评论区；`comment_input_single/comment_input_multi` 只改变输入层；分享和词条等浮层保留底层上下文。
- **Must Keep**：正文连续性、原导航与标题层级、辅助功能次于阅读、评论边界。
- **Can Vary**：学习模块顺序、弱 metadata 折叠、观点与相关入口组织。
- **Avoid**：为新增入口重排整页、用 Feed 卡表达链接、浮层挤动正文、功能控件持续遮挡阅读。

## Article Learning Function

`profile_id: article_learning_function`
`status: confirmed`

- **Experience Goal**：在保留文章上下文的前提下，让用户聚焦一种阅读或学习工具。
- **Visual Thesis**：一个功能层只服务一个学习任务，工具控制轻，内容结果清楚且可持续阅读。
- **Cognitive Flow**：功能定位 → 模式/版本选择 → 内容结果 → 局部辅助 → 返回原文。
- **Focus Curve**：导航和模式控件快速完成定位，视觉注意力随后让给结果内容；图片、PDF 或双语文本成为当前唯一主对象。
- **Surface Grammar**：功能层使用连续内容面；模式切换使用 Tab/Popover；段落、双语对照和图片按内容结构分隔，不卡片化每一段。
- **Module Roles**：Navigation Bar 维持上下文，Function Tab 表达工具模式，内容区承载结果，Popover 只处理短选项或解释。
- **Extension Heuristics**：新增工具必须说明它改善速度、理解、语言或材料获取中的哪一项；若需要长流程，应成为独立功能页而不是塞进 Popover。
- **State Deltas**：`speed/deep` 改变内容密度；`speed_with_image/deep_with_image` 增加媒体但不改变阅读层级；`bilingual` 保持双列/逐段关系；`image_preview/pdf` 聚焦媒体。
- **Must Keep**：单一工具任务、原文章上下文、可读内容结果、明确返回。
- **Can Vary**：模式选择方式、图文比例、段落组织、辅助说明显隐。
- **Avoid**：工具首页化、多个模式同时抢焦点、每段独立大卡、Popovers 承载长内容。

## Profile / Mine

`profile_id: profile_mine`
`status: confirmed`

- **Experience Goal**：让用户确认身份，并查看与自己相关的阅读、互动和历史内容。
- **Visual Thesis**：身份与个人内容稳定居前，工具和付费入口保持低调，不把“我的”做成运营宫格。
- **Cognitive Flow**：身份 → 当前内容分类 → 历史/互动列表 → 空态或登录动作 → 工具与付费入口。
- **Focus Curve**：头部身份建立归属感，主体进入稳定列表；只有登录或空态时才收束为单一行动。
- **Surface Grammar**：身份区可形成一个主 block；相关工具合并分组；历史与互动使用 Cell/List；低频动作不独立做大卡。
- **Module Roles**：User Card 表达身份，Tab/分类切换内容域，列表承载历史，Empty Placeholder 表达状态，Plus 只作弱权益信号。
- **Extension Heuristics**：新增内容先判断属于身份、历史、互动、成长还是工具；前四类进入主内容路径，工具进入分组，商业入口不得越过身份和历史。
- **State Deltas**：`normal/vip` 只改变身份与权益信号；`comments/liked` 切换列表内容；`empty` 保留分类与身份；`guest` 以登录行动替换个人内容，不重做页面骨架。
- **Must Keep**：身份优先、个人内容优先、列表一致性、BottomBar 位置感。
- **Can Vary**：内容分类、成长反馈、历史组织、工具分组。
- **Avoid**：运营宫格、付费入口成为首要焦点、每个工具单独浮卡、状态切换重绘整页。

## Settings

`profile_id: settings`
`status: confirmed`

- **Experience Goal**：让用户低成本理解并修改配置，同时清楚识别账号和风险操作。
- **Visual Thesis**：稳定导航、分组 Row 和克制反馈构成工具型页面，不引入内容卡或装饰性叙事。
- **Cognitive Flow**：返回/标题 → 常用设置 → 阅读与身份设置 → 账号信息 → 风险或退出动作。
- **Focus Curve**：页面整体低强度；仅当前选择、确认动作和风险动作获得局部强调。
- **Surface Grammar**：相关设置共享 block，Row 内左文右值；Picker 使用 Floating Sheet；风险动作独立分组。
- **Module Roles**：Navigation Bar 定位，Settings Row 承载配置，右侧值表达当前状态，Sheet 完成短选择。
- **Extension Heuristics**：新增设置按账号、阅读、通知、身份或关于归组；有即时结果用 Row，需选择用 Sheet，复杂流程跳转独立页面。
- **State Deltas**：`base` 是分组列表；`identity_sheet/font_sheet` 只增加 Floating Sheet，底层设置页保持原布局和层级。
- **Must Keep**：稳定 Row 栅格、分组关系、当前值可见、风险动作隔离。
- **Can Vary**：分组顺序、说明显隐、选择控件类型、弱反馈方式。
- **Avoid**：低频功能大卡化、Sheet 推挤底层、退出与普通设置混排、装饰抢过配置任务。

## Cold Start / Identity

`profile_id: cold_start_identity`
`status: confirmed`

- **Experience Goal**：让首次用户用最少理解成本完成一个必要身份选择。
- **Visual Thesis**：一次一个决策，IP 提供陪伴和情绪缓冲，选项与主行动保持直接。
- **Cognitive Flow**：欢迎/角色 → 选择原因 → 选项 → 主行动 → 弱跳过或说明。
- **Focus Curve**：首屏焦点固定在选择任务；插画提供情绪但不能成为需要阅读的功能说明。
- **Surface Grammar**：选项共享同一列表或选择容器；主按钮独立；说明与跳过降权。
- **Module Roles**：IP 建立陪伴，标题解释任务，Option Row 表达选择，App Button 完成闭环。
- **Extension Heuristics**：新增步骤只有在确实影响后续内容时才允许；能放进一次选择的问题不要拆成营销式多页 onboarding。
- **State Deltas**：`identity_selection` 只处理身份；未来年龄或兴趣状态继承相同决策语法，不复制一套欢迎页。
- **Must Keep**：单一决策、清晰选项、主行动、低压陪伴感。
- **Can Vary**：IP 姿态、选项组织、说明长短、欢迎节奏。
- **Avoid**：功能宣传轮播、多个主按钮、IP 遮挡选项、为了活泼增加游戏奖励感。

## Commerce And Feedback

`profile_id: commerce_and_feedback`
`status: confirmed`

- **Experience Goal**：让用户理解为什么付费、如何选择，并明确知道结果成功或失败。
- **Visual Thesis**：决策信息清楚强于促销气氛；付费 Sheet 可以有重量，反馈必须短且不篡改底层页面。
- **Cognitive Flow**：触发上下文 → 解锁理由 → 套餐/金额选择 → 主行动 → 协议说明 → 结果反馈。
- **Focus Curve**：理由和选择建立主焦点，主按钮完成决策；协议降权但可读；结果 Toast 只短暂接管注意力。
- **Surface Grammar**：付费使用 Paywall Half Sheet；普通日期选择仍是 Floating Sheet；套餐共享决策栅格；反馈使用轻量 overlay。
- **Module Roles**：Plus/IP 表达身份，套餐区支持比较，App Button 完成购买，协议解释边界，Toast 表达结果。
- **Extension Heuristics**：新增商业模块必须服务理解、比较、行动或反馈之一；没有改变决策路径时，不用新卡片包装同一信息。
- **State Deltas**：`entry` 仅表达弱入口；`paywall/recharge` 承担决策；`success` 保持短确认；`failure` 提供原因和可恢复动作，不重做页面。
- **Must Keep**：一个主行动、价格与协议可读、关闭入口稳定、底层上下文不变。
- **Can Vary**：套餐承载、权益顺序、默认推荐、成功反馈视觉。
- **Avoid**：促销海报、三卡仅改色的近似方案、协议裁切、普通日历误用 Paywall。

## Contextual Overlay

`profile_id: contextual_overlay`
`status: confirmed`

- **Experience Goal**：在不离开当前任务的情况下完成短解释、短选择、分享或轻确认。
- **Visual Thesis**：浮层的形态由依附关系和任务长度决定，始终保持底层上下文可辨认且不参与布局。
- **Cognitive Flow**：触发锚点 → 浮层内容 → 选择/理解 → 关闭并回到原任务。
- **Focus Curve**：浮层短暂成为局部焦点；遮罩和阴影只建立层级，不把它做成第二张页面。
- **Surface Grammar**：锚点解释/选项使用 Popover；普通底部选择使用 Floating Sheet；分享可用轻 Sheet；复杂长内容升级为独立页面。
- **Module Roles**：Anchor 解释来源，箭头表达关系，内容区承担短任务，关闭/选择结束临时状态。
- **Extension Heuristics**：先判断是否依附具体锚点；再判断内容能否在短列表或短说明内完成；超出时升级 Sheet 或页面，不强塞。
- **State Deltas**：`definition` 优先避让阅读路径；`option` 强调当前项；`share` 保持入口清晰；`calendar` 使用紧凑网格；`identity_sheet/font_sheet` 保持设置页锁定；底层页面全部锁定。
- **Must Keep**：明确锚点或底部依附、顶层 overlay 层级、边缘避让、内容不裁切。
- **Can Vary**：出现方向、短内容布局、选项形式、轻反馈样式。
- **Avoid**：浮层进入 Auto Layout 推挤页面、箭头分离、无锚点漂浮卡、短选择做成营销 Sheet。

## Maintenance Rule

- 新 Frame 属于既有认知流程和 Surface Grammar 时，只登记 `state_role` 与状态差异，不新增 profile。
- 只有认知流程或 Surface Grammar 明显不同，且设计已确认，才新增 `confirmed` profile。
- 未确认设计只能使用 `provisional`；不能作为生产化权威经验。
- 用户确认新方案后，先更新源节点和组件事实，再提炼跨内容、跨状态仍成立的经验；具体文案和偶然布局不得进入本文件。
