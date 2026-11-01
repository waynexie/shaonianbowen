# Component Content Modules

## Source Scope

- 正式 Master：`components.FeatureCover`、`components.RecommendationTicker`、`components.LearningModuleCard`、`components.ExpertOpinionCell`。
- 正式组件页按 `components.yaml` 中各组件的 family 和 live locator 解析。
- 尺寸、完整属性/slot 清单、当前结构状态只在 `metadata/components.yaml` 对应条目维护；本文件保留选型理由、组合边界和扩展判断。

## Classification Rule

- 按组件职责、内容骨架、交互方式和 resizing 归类，不按页面或业务场景归类。
- 只有语义职责相同、主要图层骨架相同、尺寸行为相近的组件才能进入同一 Variant Set。
- 场景组合写入 `page-recipes.md`；组件自身规则写在本文件和 `metadata/components.yaml`。
- 只有一个真实形态时保持单 Component。出现第二个已确认形态后再组合为 Variant Set，不创建占位变体。

## Feature Cover

**Function**

- 单一主内容的沉浸式首屏封面，承载全宽媒体、标题、可选推荐信息和可选主操作。
- 可用于每日主题、专题推荐、课程主题或其他需要首屏聚焦一个内容对象的页面。

**Construction Contract**

- 封面媒体、标题、推荐信息和主操作按叠层构图；尺寸和属性查 `components.FeatureCover`。
- Header、状态栏和后续正文不属于 Feature Cover。
- 推荐信息是否已嵌套独立实例，查目录的 `known_construction_limits` 并核验 live 结构；视觉相同不能证明实例关系。

**Variant Guidance**

- 单一已确认形态不强行包装成单成员 Variant Set；当前结构状态以目录为准。
- `Show Recommendation`、`Show Audio` 使用 Boolean；音频组件使用 INSTANCE_SWAP，不为显示与否创建变体。
- 只有出现结构明确不同且已确认的封面形态时，才扩展 `Layout`；Light/Dark 由变量模式处理，不创建主题变体。

**Do**

- 保持标题和主操作在不同封面素材上均可读。
- 每次只聚焦一个主主题，并保留媒体替换能力。
- 页面使用时实例化 Master，不从图片、矩形和文字重画。

**Don't**

- 不用作多条内容 Feed 卡、营销 Hero 或普通文章缩略图。
- 不把状态栏、页面 Header、正文或 BottomBar 包进组件。
- 不为了新封面内容创建页面专属平行 Hero 家族。

## Recommendation Ticker

**Function**

- 带来源身份的横向推荐信息条，用于封面或内容上下文中的专家推荐、编辑推荐或来源背书。
- 它是内容归因组件，不是营销标签、Toast 或 Anchored Popover。

**Construction Contract**

- 横向 Hug Auto Layout，保持单行；可替换内容和属性见 `components.RecommendationTicker`。
- 容器负责水平移动和裁切；运动方向、速度属于 motion recipe，不属于视觉变体。
- 跨场景复用独立 Master；升级 Feature Cover 内部结构前检查目录记录的嵌套限制，保护既有属性覆盖。

**Variant Guidance**

- 当前保持单 Component。只有出现已确认的静态短条、双行归因等不同骨架后，才评估 `Layout` 变体。
- 头像显示使用 Boolean，不创建 `WithAvatar/WithoutAvatar` 平行组件。

**Do**

- 保持来源身份与推荐语层级清楚，长内容按横向移动处理。
- 在其他专题、课程或文章封面需要来源推荐时复用。

**Don't**

- 不换行撑高封面，不静止遮挡标题或主操作。
- 不当作品牌营销角标、普通标签或解释气泡。
- 不把动画状态拆成多个视觉组件。

## Learning Module Card

**Function**

- 正文中的结构化学习模块，用于互动提问或阶段总结；按内容职责选择 `Type=Question` 或 `Type=Summary`。
- 两种 Type 可以同时出现在同一页面，它们不是流程前后状态，也不是页面专属组件。

**Construction Contract**

- 纵向 Auto Layout、内容驱动高度；尺寸及各 Type 的完整属性清单见 `components.LearningModuleCard`。
- Question 承载提问与选项，Summary 承载总结、步骤与解释；示例属性只用于说明两类内容的不同职责。
- 组件集会暴露两种 Type 的属性并集；实例先选择 `Type`，再只填写当前 Type 对应属性。另一 Type 的属性不可作为当前实例的可见内容依赖。
- 长问题、长选项、长总结和长解释均通过 Auto Layout 增高，不使用固定高度压缩内容。

**Variant Guidance**

- 组件集轴固定为 `Type=Question/Summary`；Question 与 Summary 是内容骨架类型，不命名为 `State`。
- Question 的选中、作答、结果等真实交互状态出现后，再增加独立 `State=Default/Selected/Answered` 轴；不要把状态塞进 `Type`。
- `Show Illustration` 使用 Boolean；不得为有无插画创建平行 Variant。
- 新正文模块只有在共享学习模块职责、宽度和主要 resizing 契约时才允许加入 `Type`；资讯、评论、付费、纯展示卡必须进入各自组件族。

**Do**

- 先选 `Type`，再替换该 Type 的有效文本、Boolean 和 slot。
- Question 用于判断、单选、理解检查或思考触发；Summary 用于总结句、步骤路径和解释信息。
- 新题型或新总结骨架先评估同族轴扩展，不复制页面专属卡片。

**Don't**

- 不把 Question/Summary 称为前后 `State`，也不同时显示两类互斥骨架。
- 不替代 News Card、Impact Card、Comment Cell 或付费权益卡。
- 不用固定高度裁切内容，不缩小核心字号迁就长文案，不把 Callout 箭头拆成漂移装饰。
- 不把视觉相似但职责、slot 或 resizing 不同的卡强行加入本组件集。

## Expert Opinion Cell

- 正式组件集为 `components.ExpertOpinionCell`，按同一内容骨架使用 `Size=Compact/Default/Long`。
- `Size=Compact` 用于横向浏览；尺寸和行数限制查目录 `resizing_guidance`，超长先编辑摘要。
- `Size=Default` 与 `Size=Long` 用于标准内容列；Size 表达密度和占用尺寸，不表达页面场景。
- Do：按内容密度选 Size。Don't：为首页、详情或其他场景创建平行 Expert Card 家族。

## Validation

- Master ID、实例关系和组件属性在移动/重命名后保持有效。
- 长问题、长选项、长总结和长 Callout 无裁切、重叠或异常 padding。
- Feature Cover 在不同媒体上保持标题和主操作可读。
- 页面截图中使用正式实例；旧名称只用于兼容查询，不作为新组件命名。
