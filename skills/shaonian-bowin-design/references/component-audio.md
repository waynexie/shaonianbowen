# Component Audio

## Source Scope

- 组件库页：`14 Media - Audio`，依赖 `IconButton`、`Icon16/20/24`。

## Selection Rule

- 文章详情音频：使用 `AudioPlayerBar`，作为阅读辅助，不抢正文。
- 普通按钮或营销 CTA 不能替代音频组件。

## Construction Contract

参数、完整变体和可编辑属性只读取 `metadata/components.yaml` 的对应条目，写前核验 live 母版。本节解释组合与内容风险。

- `AudioPlayerBar`: 将播放动作、主题和时长作为一个阅读辅助单元；通过实例属性替换标题和时长。
- `ArticleSummaryAudio`: 内容摘要音频入口，放在详情内容流中，权重低于标题/正文。
- `AudioProgressControl`: 固定宽度和绝对定位风险见目录的 `known_construction_risks` / `resizing_guidance`；放入沉浸页时先验证时间标签和进度轨道，不直接拉伸。
- `UserAnswerBubble`: 对话气泡，不替代评论 cell。
- `AudioScriptParagraph`: 脚本文段，必须保持可读行高和足够对比。
- Resizing: 长标题优先压缩文案或截断，不挤压播放按钮、进度条和 duration。

## Style Contract

- 使用现有深色音频条、绿色播放强调和 `Icon16/20/24`。
- 沉浸页背景可以发散，但脚本、进度、播放控制必须有足够对比。
- 控制区不使用娱乐播放器皮肤、强霓虹、游戏化奖励或营销按钮样式。

## Variant Guidance

- `AudioPlayerBar` 按首页或详情语境、播放或暂停状态选择目录已登记的变体；不能把首页每日音频入口误作详情 AI 摘要。
- 播放/暂停只替换图标状态，不重画按钮。

## Allowed Local Layout

- 全新沉浸探索页允许本地重组：全屏背景、中心 IP、舞台构图、大播放控制外层、脚本容器位置。
- 必须保留：音频进度语义、播放控制语义、脚本文字可读性、底部安全区、导航返回路径。

## Interaction Handoff

本文件只定义音频场景的交互意图，不维护动效参数。

- 播放/暂停、进度拖动、脚本展开、音频入口点击属于基础点击反馈或局部内容更新语境。
- 播放状态、脚本段落、高亮字幕、评论/回答插入属于内容更新语境。
- 音量、倍速、字幕、更多设置等面板按 `component-overlays.md` 判断是否为 Floating Sheet。
- 字段提示、拖动数值气泡、播放状态 Toast 属于临时反馈语境。
- 从列表进入 音频详情属于二级页面导航语境。
- 如需表达交互状态，静态设计稿只记录触发入口、状态变化、组件语境和视觉约束。

## Validation

- `audio_component_check`: 记录音频语境、正式组件复用、所选完整状态屏，以及局部源模式没有被误报为组件。
- 检查进度、时间、播放按钮、字幕/脚本不裁切、不重叠。
- 音频页面必须检查底部安全区和控制区，不覆盖脚本。
- 深色背景上检查文字对比。
- `interaction_state_scope_check`: 需要表达交互状态时，记录音频交互语境、触发入口和状态节点。

## Anti-Patterns

- 只画一个大播放按钮，没有主题、脚本、进度或安全区。
- 在需要旧式进度语法的页面手画进度条替代 `AudioProgressControl`。
- 音频入口做成营销 CTA。
- 控件压住字幕、脚本或底部导航。
- 音频页面变成娱乐音频 App 皮肤。
