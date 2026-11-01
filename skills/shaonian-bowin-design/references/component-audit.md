# Component Audit

本文件解释组件复用与结构审计方法。每个组件的状态、节点、变体、slot、尺寸和风险只在 `metadata/components.yaml` 对应条目维护；当前事实在写入前定点核验 live 母版。

## Reuse Decision Tree

1. 由场景和运行时索引定位最近语义组件族及源实例。
2. 定点读取组件条目的 `component_status`、`construction_status`、`required_instance`、fallback、slot 和 resizing 约束。
3. 在 live Figma 核对节点实际类型与母版关系。分类 Frame、场景卡片和展板不是可实例化母版。
4. 使用实例、现有变体或同族扩展；属性修改后保留实例关系。已登记组件族不能以手画结构、拆出的子层或图片替代。
5. 尚未组件化的局部模式按已登记 recipe 处理并报告缺口；缺失母版按该条目 fallback 执行。

## Status And Construction

选用状态及 fallback 定义见 `components.yaml > component_audit_contract`。结构状态是另一个维度：稳定组件仍需核对实际 slot；带约束组件要检查长文字、固定宽度、绝对定位和替换行为；依赖 recipe 的组件需在真实页面中验收。

风险检查按组件族读取：导航关注返回路径、Header 变体与安全区；音频关注时长、进度、标题截断和脚本遮挡；评论关注昵称、长正文、回复层级、输入框 padding 与动作区；弹层关注依附、锚点、遮罩、尺寸和内容滚动。具体方法见相应 `component-navigation.md`、`component-audio.md`、`component-comments.md`、`component-overlays.md`。

## Known Source Gaps

组件状态通过目录查询，避免在这里再维护一张库存表。已有 BottomBar 外壳、设置行、付费套餐等是否可实例化，分别检查最近条目的正式母版与 fallback；历史 Frame 和弱命名节点只作线索。

同语义成熟组件优先，例如专家观点与普通评论分开、“查看全部文章”使用链接入口、详情辅助音频不升级为沉浸播放器。页面装配由 `page-recipes.md` 负责。

## Missing Icon Resolution

1. 查询 `metadata/components.yaml > components.Icon16`、`components.Icon20` 或 `components.Icon24`，在 live 母版检查当前语义是否已有可用变体；fallback 以对应条目为准。
2. 没有匹配变体时，从 `metadata/source-registry.yaml` 的 `use_for=icon_candidate` / `iconsax_candidate` 定位已登记候选，结合截图核对语义、线性/填充风格和尺寸，不仅看名称。
3. 候选使用前必须按目录规则核验并沉淀所需尺寸，保留来源和实例关系。正式图标库写入受 `task-routes.yaml > global_defaults.persistent_write_scope` 限制；普通产出授权不等于正式入库授权。
4. 库内没有合适候选时报告具体缺口。仅在用户明确允许外部查找时获取同风格素材；需要正式库维护则先取得相应范围授权。没有可用候选或写入权限时停止该依赖，不手绘替代，也不把候选冒充正式组件。

## Audit Evidence

证据字段来自 `validation.yaml > registered_component_family_gate_check` 与 `component_construction_check`，包括源组件、交付实例、属性变化和目标截图。草稿同样执行正式组件族门禁。

普通任务只报告需要整理的组件缺口。明确正式组件维护时才按 `formal_component_maintenance_check` 和精确 allowlist 整理母版，通过实例替换与截图验收后回写目录；发布不自动执行。
