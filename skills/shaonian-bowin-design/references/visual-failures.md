# Visual Failures

本文件用于已发现问题后的诊断与修复，不是日常任务的第二套检查表。常规截图检查见 `design-quality.md`；是否阻断、适用质量档和证据要求以 `metadata/validation.yaml` 为准。只读取匹配症状，修复后复用任务证据并更新受影响区域截图。

## Lookup Becomes Generation

symptom: 用户问“某页面/组件/状态长啥样、看一下、查询、有没有”，输出却生成或改造了一张新稿，并且把头像、IP、标签文案、卡片内容或布局改掉。

root_cause: 没有做语义意图分类，只靠关键词或对象名路由；把只读查询误判成设计生成，或把缺失状态自动当成探索任务。

required_check: 检查 `semantic_intent` 是否为 `lookup_existing`，`task_route_type` 是否为 `existing_source_or_state_lookup`；检查是否只读查询了源文件、组件库、产品页，以及用户明确要求时的旧历史输出；确认没有写入 Figma 或本地生成冒充源稿。

repair_strategy: 撤回生成结论；返回已查源节点和候选截图。若没有找到，明确 `not_found_in_source`，等待用户明确说“生成/设计/出一版/做一个”后再进入设计流程。

## Variable Mode Preview Reconstruction

symptom: 用户查询夜间/暗色/dark mode，输出却新建 `Render / ... / dark preview` 或本地预览 Frame，并且状态栏、导航、返回按钮、图标或页面 chrome 与源稿不一致。

root_cause: 把变量模式截图查询误当成暗色设计生成；为获得预览重建了页面结构，或在任一 Figma 文件中留下临时渲染节点。

required_check: `task_route_type` 必须是 `existing_source_or_state_lookup` + `variable_mode_visual_lookup`；检查目标节点是否为源 `screen_frame` 或组件节点；检查 `temporary_render_cleanup_status` 和 `chrome_component_integrity_status`。

repair_strategy: 删除持久预览节点；重新用同一源节点做变量模式截图。若工具无法在不留下持久节点的情况下渲染，返回 `variable_mode_preview_unavailable`，不要生成近似暗色稿。

## Source Context Reconstruction Drift

symptom: 用户只要求在已有页面、模块或组件语境中新增/修改局部状态，但结果像从空画布重建，导致背景、导航、标题、列表、卡片、底栏、文案或组件样式漂移。

root_cause: 输出缺少完整源截图锁定上下文，或目标区之外被重新构建。

required_check: 检查 `task_route_type`、`source_frame_id`、`source_screenshot_evidence`、`task_id` 和 `task_container_id`；对比源 Frame 与输出 Frame 的非目标区域截图。

repair_strategy: 按 `task-routes.yaml > global_defaults.context_strategy_routing` 恢复上下文。局部视觉草稿使用源截图锁定目标外区域；正式稿或完整原生编辑要求使用原生结构，不能用截图底图补救。完成后对照整屏与锁定区。

## Locked Context Mutation

symptom: 局部引导、局部状态、浮层或入口修改导致非目标区域被移动、改色、改文案、改圆角、改背景或改组件结构。

root_cause: 没有明确 `locked_regions`，或把临时状态插入主内容 Auto Layout 栈，导致底层内容 reflow。

required_check: 写入前记录 `allowed_mutations` 和 `forbidden_mutations`；交付前逐项检查 locked regions 的位置、内容、样式、组件实例状态和截图表现。

repair_strategy: 只保留目标区域变化；临时浮层放到 topmost overlay layer；除非用户明确要求，背景、导航、标题、正文、列表、卡片、底栏和已有文案全部恢复源稿。

## Style Token Escape

symptom: 核心背景、标题栏、卡片、按钮、标签、底栏或文字层级脱离少年博闻变量/组件语义，出现看似“新设计”的外来视觉。

root_cause: 生成时绕过 `tokens.yaml`、text styles、effect styles 或组件实例；用 raw values 解决局部问题。

required_check: 检查核心可见节点的 bound variables、effect style 和组件来源。

repair_strategy: 先恢复正确的源变量、样式与组件语义，再按 `metadata/validation.yaml > minimum_token_binding_check` 区分来源无法核验和节点绑定未完成。绑定缺口按质量档处理，不自行设无条件停止规则；草稿也不能绕过正式组件复用、源稿保护或基本视觉质量检查。

## Component Substitution Drift

symptom: 组件可用或源结构存在时，输出仍用本地 Frame/Text/Vector 画了一个相似控件，后续改文案、改状态或截图时变形。

root_cause: 把“视觉相似”当作“组件复用”；没有通过 `ready_to_force` 实例门禁。

required_check: 检查 required component region 是否为 `INSTANCE` 或同族 variant；出现本地覆盖层、伪组件、source-compatible local 标记即失败。

repair_strategy: 使用本地源组件实例、源实例复制或同族 variant；不可用时报告 blocker，不用 primitives 兜底。

## Clipped Helper Text

symptom: 价格折算、协议、按钮文案或列表辅助文字被裁切、贴底、缺少下半部。

root_cause: 容器高度不足、源 Auto Layout hug 行为被拉伸后回弹、只看 metadata 没看截图。

required_check: 整屏截图 + 密集区域放大/裁切截图；检查文字 descender、底部 helper、协议换行。

repair_strategy: 增加容器高度或改 Auto Layout；按当前组件约束调整输出卡片；必要时重建局部结构。

## Abnormal Padding

symptom: 卡片内出现过大空白、文字贴边、按钮和协议间距失衡。

root_cause: 复用源节点后改变尺寸但没有重算内部节奏；把旧组件当自由容器。

required_check: 比较同组元素上下内边距、行距和视觉重心。

repair_strategy: 先定义栅格和行高，再放内容；不要依赖肉眼挪动。

## Alignment Drift

symptom: 左边标题/说明不在同一列，右边价格不共享右边界，文本看似居中漂移。

root_cause: 文本框过宽且继承居中对齐，或不同 row 独立绝对定位。

required_check: 记录左列 x、右列右边界、基线关系；截图放大看视觉对齐。

repair_strategy: 使用 Auto Layout row 或明确列栅格；文本框宽度贴近内容，避免无意居中。

## Near-Replica Redesign

symptom: 用户要求重新设计/发散，但结果仍像原版，只是卡片大小、颜色或排列有变化。

root_cause: recipe 和组件复用权重过高，未按 `divergence_contract_check` 确定真实差异。

required_check: 生成前声明信息架构、承载方式、决策路径或视觉组织的变化；交付时说明差异。

repair_strategy: 至少改变一种核心组织方式，例如卡片陈列 -> 无框清单/分段控件/权益摘要。

## Metadata-Only Pass

symptom: XML/结构看似正确，但截图中存在裁切、错位或视觉不成熟。

root_cause: 把 metadata 当作视觉验收。

required_check: 最终交付前必须查看截图；密集区域不能只看整屏缩略图。

repair_strategy: 修复后重新截图；最终报告写明 `screenshot_regions_checked`。

## Detached Popover Arrow

symptom: 锚点气泡的箭头和 surface 分离、悬空、错位，或箭头没有明确指向触发词/按钮。

root_cause: 把箭头和气泡作为独立绝对定位元素手动摆放；没有把气泡当作一个 overlay 组件/同族结构验收。

required_check: 放大截图检查 arrow tip、arrow base、锚点中心或边缘三者关系；检查 surface + arrow 是否作为同一 top-level overlay 单元或同族组件实例交付。

repair_strategy: 优先使用 `AnchoredPopover` / `GuideBubble` 组件或同族变体；没有正式组件时，至少用同一个 overlay Frame 承载 surface 与 arrow，并按 anchor side 重新定位。

## Overlay Reflow Mutation

symptom: 气泡、Toast、Popover 等临时浮层把页面主内容往下/往旁边挤，或打开状态改变了背景、导航、音频条、列表等无关区域。

root_cause: 把临时浮层插入页面内容 Auto Layout 栈，或在 production_mode 局部状态里没有锁定底层页面区域。

required_check: 对比源稿和输出稿的关键模块坐标/背景节点；检查浮层是否位于页面内容之上的 top-level overlay，而不是主内容栈成员。

repair_strategy: 将临时浮层移到 topmost overlay layer；仅允许新增/修改浮层和必要锚点高亮，底层页面背景、导航、内容模块和底栏保持源稿组件、变量与位置。

## Primitive Status Bar

symptom: 状态栏由本地 Text/Rectangle/Ellipse/Vector 拼出，或被命名为某种“source-compatible/local approximation”。

root_cause: 把“看起来接近源文件”当作可交付，而没有通过 ready-to-force 组件实例门禁。

required_check: 检查状态栏节点类型必须是 `INSTANCE` 或源同族组件变体；出现本地时间、电量、信号、Wi-Fi primitives 即失败。

repair_strategy: 复用本地源状态栏实例；不可用时停止报告 `primitive_substitution_hard_fail`，不要交付近似重绘。

## Component Text Overlay

symptom: 已有按钮、Row、Cell 或 Sheet 组件上方叠加本地 Frame/Text 改文案，形成视觉覆盖层而不是组件内部状态。

root_cause: 没有修改组件实例属性/可编辑文本，也没有扩展同族变体，而是用覆盖层伪装成组件状态。

required_check: Button/AppButton/Cell/Row/Sheet 的文字变更必须发生在实例内部、组件属性或同族变体中；组件上方出现覆盖文案、遮罩或本地替代标签即失败。

repair_strategy: 修改实例文本或暴露属性；不可编辑则创建同族 variant 或报告阻塞，不用本地覆盖层。

## Hand-Drawn Floating Sheet

symptom: 普通字体/语言/选择弹窗由本地 Sheet header、选项列表和 option row Frame 拼出，选项区贴底、错位或裁切。

root_cause: 未复用 `Sheet & Picker` 或源 Floating Sheet 实例，且没有按弹出层规范做 Auto Layout 和局部截图检查。

required_check: 普通设置类 Floating Sheet 先查 `source-index.md`、live Figma 最近同类源节点和 `13 Overlays - Sheets & Pickers`；交付必须是实例/同族扩展，或明确报告组件缺口。

repair_strategy: 从最近同类源 Floating Sheet 或 `Sheet & Picker Type=FontPickerSheet/OptionPickerSheet` 出发替换文案和选项；选项列表使用 Auto Layout，保留底部呼吸空间，并做放大截图。

## Density And Utility Weight

symptom: 标题、来源、统计、标签、音频和按钮同权重，或低频设置/付费入口压过身份与阅读任务。

root_cause: 默认完整字段被当作用户要求，未判断当前主任务与存在角色。

required_check: 对照当前显式约束、页面体验 profile 与主焦点，检查字段必要性和容器分组。

repair_strategy: 保留核心信息和一个明确动作，优先移除重复弱信息；设置入口归入既有行/分组，付费入口按触点控制权重。

## Wireframe And Product Copy Leakage

symptom: 结果仍是占位矩形、抽象媒体块或弱选中态，产品 UI 中出现方案名和设计解释。

root_cause: 将布局完成误当视觉完成，混淆 Frame 命名与产品可见文案。

required_check: 检查源风格媒体、真实组件状态及产品文字；方案名只在 Frame 名称或交付说明中出现。

repair_strategy: 使用可追溯的源素材与正式组件完成目标区，移除产品内设计说明并重截整屏。

## Layout Container Misuse

symptom: 列表或重复行用 Group 和自由坐标拼装，替换文案后挤压、错位。

root_cause: 未用可调整布局容器表达分组和重复结构。

required_check: 检查主容器、列表、模块区和重复行的 Auto Layout、尺寸与换行行为。

repair_strategy: 在授权目标区改为原生布局容器，保留源组件关系，并用长文案和目标宽度复核。
