# Component Comments

评论组件承载少年博闻的讨论和表达。它不是普通 row/cell，也不是强社交动态流。

## Source Scope

- 组件库页：`04 Inputs - Comment`、`08 Data Display - Cards/Cells/Covers/Avatars`。

## Selection Rule

- 评论入口：使用 `CommentInputTrigger`。
- 普通评论：使用 `CommentCell Level=Root`。
- 回复：使用 `CommentCell Level=Reply` 或源组件嵌套结构，不手画缩进。
- 语音评论：使用 `VoiceCommentCell`。
- 专家观点使用 `ExpertOpinionCell`，不要混成用户评论。

## Construction Contract

尺寸、完整状态和 slot 以 `metadata/components.yaml` 中对应组件为准，写前核验 live 母版；本文不维护另一份参数表。

- `CommentInputTrigger`: 头像和输入气泡共同表达发言入口；长 placeholder 检查右侧 padding。
- `CommentCell Root`: 承载独立评论；正文为主，meta/回复为弱层级，头像与右侧内容保持稳定关系。
- `CommentCell Reply`: 表达对上一层评论的回应；层级由变体或同族嵌套结构承载，不靠手动 x 偏移伪造。
- `VoiceCommentCell`: 将身份、语音气泡、波形、时长与互动作为一个评论单元，不能只塞进一个播放按钮。
- 列表容器必须使用 Auto Layout；root gap、reply stack gap、divider 位置稳定。
- Resizing: 长昵称、长正文、长 meta、无点赞、无回复、语音时长变化都要做截图检查。

## Style Contract

- 评论保持低压学习讨论感：白底或轻 block、弱 meta、适度互动。
- 点赞/回复是次级动作，不能挤满 footer。
- 回复 block 可使用浅绿/浅灰背景，但不能像营销卡或设置 row。

## Variant Guidance

- 用 Root/Reply 变体表达层级。
- 语音评论用 `VoiceCommentCell`，不要把语音波形塞进普通 `CommentCell`。
- 新增评论状态优先扩展现有 comment family；只有结构语义变化才考虑新组件。

## Allowed Local Layout

- 允许本地重组：评论区标题、列表父容器、加载/展开更多、局部排序说明。
- 必须实例化：`CommentInputTrigger`、`CommentCell`、`VoiceCommentCell`。
- 修改评论功能时锁定正文、导航、底栏和页面背景，除非用户明确要求整页改版。

## Interaction Handoff

本文件只定义评论场景的交互意图，不维护动效参数。

- 评论输入触发、发送按钮、回复/点赞/更多属于基础点击反馈语境。
- 新评论、展开回复、加载更多、局部成功状态属于内容更新语境。
- 字段提示、发送成功/失败提示属于临时反馈语境。
- 评论详情或用户资料等跳转属于二级页面导航语境。
- 输入面板若以底部 Sheet 出现，按 `component-overlays.md` 判断 Floating Sheet 语境。
- 如需表达交互状态，静态设计稿只记录触发入口、状态变化、组件语境和视觉约束。

## Validation

- `comment_component_check`: 记录输入、root、reply、voice 是否使用组件。
- 检查评论列表 Auto Layout、回复缩进、divider、头像/昵称/正文/meta/动作对齐。
- 密集区必须放大截图：输入区、首条评论、回复 stack、语音评论。
- 长文本替换后不得裁切、覆盖头像、挤压 like 或错位。
- `interaction_state_scope_check`: 需要表达交互状态时，记录评论交互语境、触发入口和状态节点。

## Anti-Patterns

- 把评论做成普通设置 row 或 feed card。
- 手画回复缩进和语音波形。
- 动作、统计、标签挤满评论 footer。
- 专家观点和用户评论混用同一组件。
- 评论区改动顺手重做正文、导航或底栏。
