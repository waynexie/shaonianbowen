# Figma Workflow

本文件负责操作顺序与案例。路由和写入范围读取 `metadata/task-routes.yaml`；门禁和证据字段读取 `metadata/validation.yaml`。按所选 profile 读取本文件相关小节。

## Source Priority

复用本轮已核验的精确源节点与 session；写入前对新增依赖或可能失效证据做定点 live 核查。产品语境由 `source-frames.yaml` / `source-registry.yaml` 定位，母版由 `components.yaml` 定位。变量、母版和源屏当前事实以 live Figma 为准。产出页仅在查询产出或续改时作为目标；查询缓存只提供预览。

## Lookup Fast Path

1. 按入口脚本选 `lookup_profile` 和 `locate` / `visualize` 意图，返回少量相关候选。命中场景后使用源屏或母版 ID；索引缺失、歧义、失效时才搜索相关组件族。
2. 视觉查询复用本轮精确画廊图片，或校验同节点、同状态、同模式的缓存。最新请求和无有效缓存的情况定点查 live Figma。
3. Dark 查询按 `routes.existing_source_or_state_lookup.variable_mode_visual_lookup` 对同一节点临时应用模式，截图核验后恢复。不可用时返回专属状态。
4. 交付图片按 `global_defaults.visual_query_delivery` 持久化、取得平台 URL、通过附件校验并实际嵌入。普通查询不自动更新缓存。
5. 素材名称弱或缺失时结合父级、节点类型、尺寸、缩略图及真实使用判断，方法见 `source-index.md > Project Asset Lookup Sources`。

## Before Write

1. 用当前需求确定语义 route、质量档与速度层；记录 `turn_intent_contract`，明确用户排除项、目标区域和锁定项。
2. 定点读取 `metadata_authority_gate_check` 与所选 profile 指向的必要小节。明确普通产出、正式组件维护或场景维护的写入范围；工具要求的文件 session 和设计系统预检照常执行。
3. 将同一源 Frame 的尺寸、目标区、截图能力，以及触及组件的母版类型、变体、属性、slot、变量、响应式信息合并读取。查询结果中的容器或展板不能直接实例化为母版。
4. 组件通过 `components.yaml` 对应条目与 `registered_component_family_gate_check` 核验；选型和结构风险见 `component-audit.md`。核心变量按质量档处理，正式组件复用在所有档位执行。
5. 按 `global_defaults.context_strategy_routing` 选构建方式。设计判断使用 `figma_design_judgment_check` 的精简记录；只有结构、信息层级或状态模型变化时再读匹配的页面体验 profile。

## Existing Context Local Mutation Flow

适用于既有页面的局部可见草稿。正式稿或完全原生可编辑要求转入 Productionization。

1. 锁定有效的精确源 Frame、当前要求的模式、完整截图与 `target_region`。目标外全部作为锁定上下文。
2. 在独立输出 Frame 中放置完整源截图，只在目标区内覆盖源匹配背景并创建可编辑原生层；已登记组件仍使用实例、变体或同族扩展。
3. 文案、图标、组件状态通过可编辑属性或同族结构修改，使用 MCP 默认文本引擎。覆盖假文字、打散组件和手画平行家族不能代替实例变更。
4. 临时弹层保持 Overlay 关系；用户要求内联展开时，仅在事先明确的目标区域中调整直接受影响的内容流。范围不足时先解析新的目标边界。
5. 按 Task-Scoped Atomic Output 完成落位。检查目标区、整屏安全边界及锁定区，与源截图对照；证据和草稿缺口按选定 profile 返回。

### 同文件底图复用

live Figma 已解析精确源 Frame、模式和目标区后，若文件内有候选 IMAGE 图层及 `imageHash`，用同尺寸、同变量模式、相同隔离渲染参数重截源 Frame，比较 PNG 或解码像素。匹配后可在原子写入中复用同文件 `imageHash`。候选名称不能证明身份；下载结果为空时核对类型与字节，工具支持时用内联 PNG。无匹配或必要能力不可用时报告具体阻断。

## New Context And Exploration

新页面直接构建原生 Frame，复用正式组件、变量和 Auto Layout。已有上下文的多方案草稿沿用局改的源截图锁定方法。独立顶层临时元素是否可用 `screenshot_overlay` 由 `global_defaults.context_strategy_routing` 决定。

每版用一句主张说明用户任务、产品适配和组件策略，并选择真实的信息层级、承载模型或操作路径差异。品牌与视觉判断见 `design-language.md` / `design-quality.md`，页面体验与装配分别按 profile / recipe 读取。外部参考只在存在明确模式缺口或用户要求时加载。

## Continuation Iteration

先核对上一轮输出 Frame、截图资产、组件母版与真实 session，复用仍有效证据。直接在上一轮产出处理请求增量；新增页面、组件族、源依赖或生产要求时才补充对应预检。每个改变的方案重新截整屏，并检查改变区域、锁定区域及安全边界。

## Productionization

从已核验的正式组件、变量、Auto Layout 和默认文本引擎直接构建原生输出。已有上下文保持源语义、锁定区域外观及明确的修改范围；草稿截图用于对照，不作为正式稿的不可编辑底层。

按 `quality_tier_routing.tiers.production` 和对应 route 检查实例来源、属性、Token、Auto Layout、适用的 Dark 与响应式行为。整屏及关键密集区域放大检查均有真实证据，缺口解决后才能报告正式交付。

## Component And Scene Maintenance

组件任务默认输出 `output_only` 草稿。明确要求正式组件库维护时，记录精确母版 Page / 源 Frame allowlist，按 `formal_component_maintenance_check` 创建或扩展同族组件；通过结构、实例替换、响应式与截图检查后更新组件登记。发布仍为人工动作。

场景索引维护使用 `persistent_write_scope.scene_index_maintenance_scope` 的精确范围，仅组织入口、实例与链接。母版留在类型分类页；展板不承担响应式验收。场景屏幕字段通过 `source-frames.yaml` 引用，不再复制身份、尺寸、状态和组件族清单。

## Task-Scoped Atomic Output

普通产出和产出页审核预览执行 `global_defaults.task_atomic_output` 与 `canvas_placement_policy`：一次 `use_figma` 调用内读取最新子节点，创建唯一任务容器、复用或创建当日唯一日期分隔、建立全部方案并计算真实边界。已有长屏使用真实宽高，新增方案依权威间距落位。任务名不含日期前缀。

碰撞只移动当前批次；并发重复日期分隔只清理本次创建的副本。返回前核对所有创建、修改、删除节点的写入范围，越界或碰撞按契约回滚。正式组件或场景维护使用各自 allowlist；产出页的任务容器规则仅用于其审核预览。

## Validation And Delivery

按 `validation.yaml > pre_generation_checks`、所选 route profile 与实际触及区域选择检查，不重复填写第二套通用清单。顺序为：

遵守 `pre_generation_checks.decision_records.evidence_reuse_contract`：同一目标、状态、模式和版本的证据写一次，由适用检查共用。多方案各保留真实 Frame 与截图关联；改动后更新相应证据，不把旧截图用于新状态。

1. 核对持久写入范围、上下文策略、实例来源、属性变化及画布碰撞。
2. 实际查看每个方案整屏截图，核对目标区、锁定区与安全边界。发现基本视觉问题或正式组件替代错误时，仅按权威修复次数处理受影响区域并重截。
3. 正式稿补齐完整设计系统与响应式检查；草稿记录允许的生产缺口，已登记组件缺失不能作为草稿缺口放行。
4. 质量脚本只核对 `quality_evaluator_contract` 声明的证据范围。它不读取像素，也不替代 Agent 的全部门禁；最终交付仍按 `generated_output_delivery_check` / `visual_query_delivery_check` 验收。
5. 逐方案返回真实节点及整屏截图，说明实际完成状态和缺口。仅有索引、结构信息、临时图片或配置保存不能证明设计交付完成。

## Route Examples

- “有没有正式稿”：查询已有状态，生产关键词本身不构成生成授权。
- “个人中心夜间模式长啥样”：查询同一屏在 Dark 变量下的效果，截图后恢复现场。
- “在头像旁加一个等级提示”：精确源屏局部草稿，只重建头像目标区域，检查相邻内容与安全边界。
- “重新设计付费弹窗三版”：先判定是否依附已知源屏；保留该上下文，改变弹窗内部承载方式并逐版交付。
- “把 B 做成可上线正式稿”：复用已选方向与源证据，重新构建完整原生结构并执行生产门禁。
