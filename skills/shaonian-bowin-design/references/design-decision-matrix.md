# Design Decision Matrix

生成或修改 Figma 前先完成本矩阵。它用于提高设计取舍质量，避免只按组件机械堆叠。

## Step 1: Classify Page Type

| Type | User Task | Surface | Required Source |
| --- | --- | --- | --- |
| `feed` | 浏览和选择多条内容 | 浅绿页面 + 白卡列表 | `source-frames.yaml use_for=home_feed` |
| `modal` | 上下文选择或解锁 | 遮罩 + 底部 Sheet | Subscription sources, Sheet & Picker |
| `profile` | 查看身份和历史 | 白底/Profile block | `source-frames.yaml use_for=profile` |
| `settings` | 配置和账号操作 | 白底 + Block rows | `source-frames.yaml use_for=settings` |
| `onboarding` | 选择身份/年龄/难度 | IP + 轻量选项 + App Button | Cold start sources |
| `immersive` | 听、说、沉浸学习 | 全屏舞台 + 音频控件 | AI radio sources, Media Audio |

## Step 2: Pick User Main Task

只选一个主任务：

- `choose_content`: 选择一篇/一个话题进入。
- `read_understand`: 阅读并理解内容。
- `learn_apply`: 提炼考点、写作素材、观点。
- `discuss`: 发表/阅读评论或观点。
- `listen_speak`: 听音频、对聊、跟读。
- `configure`: 修改设置、身份、账号。
- `unlock`: 解锁付费内容。

主任务决定视觉权重。不是主任务的入口必须降级。

## Step 3: Extract Turn Intent Contract

从 `metadata/task-routes.yaml > turn_intent_contract` 提取当次要求、排除项、范围和差异要求。用户约束先于默认组件字段；复用实例时通过属性或同族变体满足要求。证据字段由所选 route profile 决定。

## Step 4: Information Priority

按匹配的 `screen-patterns.md` profile 读取 Cognitive Flow、Must Keep 和 State Deltas，不在此维护第二套页面优先级。新页面没有已确认 profile 时，围绕 Step 2 的主任务说明假设与取舍；空间不足先移除弱信息，不压缩主要内容。

## Step 5: Choose Container

| Need | Container |
| --- | --- |
| Repeated content decision | `News Card`, `Article Preview Cell`, `Comment Cell` |
| Quiet settings utility | Settings row pattern in Block surface |
| Contextual unlock | Bottom Sheet |
| Full-screen listening/speaking | Immersive stage + audio components |
| Related low-frequency entry | Weak row or inline strip, not standalone hero card |
| Top-level channel | Header + category/tabs + feed + BottomBar |

## Step 6: Choose Visual Weight

- `high`: page title, main content title, primary action for current task.
- `medium_high`: feed card action, audio entry, expert/source signal.
- `medium`: filters, tabs, secondary actions.
- `low`: utilities, helper text, metadata, weak cancel.
- `isolated`: logout, risk action, destructive action.

Do not promote low-frequency utilities or paid hints to `high` unless the user explicitly asks for a paywall or conversion screen.

## Step 7: Presence And Design Thesis

新增功能的存在角色、注意力预算与默认展开方式按 `feature-insertion.md` 判断。低频入口保持弱权重，当前主任务才能占用主视觉焦点。

每个探索方案用一句话连接用户任务、少年博闻气质和组件策略。例如：

- 视频卡片：让读者识别短视频并判断是否打开；保留新闻卡组件，仅在封面扩展克制的时长状态，焦点仍是选题。
- 设置入口：让低频账号操作容易找到；使用原设置行与分组，避免抢占普通设置任务。

设计前检查：布局是否有产品原因、外部参考是否已转译、装饰是否压过任务、局改是否超出边界。认知负担与单一视觉概念见 `design-quality.md`。

## Design Record

只使用 `metadata/validation.yaml > figma_design_judgment_check` 的设计判断记录；探索另按 `divergence_contract_check` 记录差异。这里的矩阵是判断辅助，不增加第二套必填字段或额外交付表格。
