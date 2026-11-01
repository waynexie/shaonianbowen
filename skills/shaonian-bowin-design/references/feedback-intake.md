# Feedback Intake

用户反馈是 skill 生长来源，但不能原样堆进文档。先分类，再转为规则、反例、验收门禁或回归测试。

本文件仅在反馈沉淀或 Skill 维护时读取。先检索是否已有同义规则：有则更新原权威定义和引用，只新增独有的案例或回归；不得为了强调一条要求，同时在入口、模块指南和验收配置各写一套。日常设计记录共用 `validation.yaml > pre_generation_checks.decision_records.evidence_reuse_contract`，本流程不要求重复提交已有截图或判断。

## Trigger

采用双触发机制：

1. User explicit trigger: 用户明确说「记住」「反哺」「沉淀」「下次避免」「写进 skill」时，必须启动反馈入库流程。
2. Agent suggested trigger: 即使用户没要求沉淀，只要反馈暴露可泛化失败，Agent 必须主动判断并建议是否沉淀。

Agent suggested trigger 适用于：

- 同一问题在一轮里修了两次仍未解决。
- 问题属于基础质量门槛：裁切、遮挡、重叠、异常 padding、对齐漂移、文字不可读。
- 用户反馈指出 mode 错误：要求发散却近似复刻，或要求局部生产改造却重做整页。
- 同类问题跨任务重复出现。
- 组件/变量/源节点规则导致输出明显变差。

普通一次性偏好不自动写入 skill，除非它暴露可泛化失败。

## Feedback Levels

- `observe`: 当前任务内记录，不写文件。用于一次性偏好、尚不确定的问题。交付报告里写入 `known_failure_checks`。
- `capture`: 写入轻量反例或观察，通常进入 `visual-failures.md`、`feedback-intake.md` 或页面相关 reference。基础质量问题可由 Agent 主动 capture。
- `promote`: 升级为硬规则或流程规则，进入 `validation.yaml`、`screen-patterns.md`、`task-routes.yaml` 或 `SKILL.md`。会显著限制未来生成自由度时，应先向用户确认。

## Feedback Types

- `visual_failure`: 不好看、裁切、padding、拥挤、比例不舒服。
- `layout_failure`: 对齐、栅格、Auto Layout、信息分组错误。
- `mode_failure`: 应该发散却近似复刻，或应该生产维护却过度发散。
- `component_failure`: 组件没用、用错、手画替代、组件约束误导生成。
- `style_language_gap`: 不像少年博闻、太营销、太游戏、太成人化。
- `content_hierarchy_gap`: 主次不清、弱信息抢权重、核心任务不明显。

## Intake Steps

1. Capture: 摘要用户反馈，不复制情绪化原句。
2. Classify: 标注 feedback type、feedback level 和影响页面/组件。
3. Generalize: 写成可执行检查，而不是审美口号。
4. Store:
   - `observe` -> 交付报告的 `known_failure_checks`，不改文件。
   - `capture` visual/layout -> `visual-failures.md`。
   - `capture` page pattern -> `screen-patterns.md` 或 `page-recipes.md`。
   - `promote` validation gate -> `metadata/validation.yaml`。
   - `promote` route/source/component policy -> `metadata/task-routes.yaml` 或 `components.yaml`。
   - `promote` workflow-level policy -> `metadata/task-routes.yaml`；`SKILL.md` 只更新导航，操作解释更新 `figma-workflow.md`。
5. Regress: 重要反馈生成一个小型回归任务，说明通过标准。
6. Report: 在交付中列出 `feedback_rules_applied`、`known_failure_checks`、`feedback_intake_decision`。

## Autonomy Policy

Agent should not stay silent about reusable feedback.

- Agent may automatically `observe` any feedback.
- Agent may automatically `capture` objective quality failures such as clipping, overlap, alignment drift, abnormal padding, unreadable text, or metadata-only validation misses.
- Agent should ask before `promote` when the rule would constrain future creative direction, component policy, or page patterns broadly.
- Agent should not auto-capture one-off subjective preferences such as “I personally prefer this button on the left” unless they repeat or reveal a broader hierarchy issue.

## Rule Writing Format

Prefer:

- symptom
- root_cause
- required_check
- repair_strategy

Avoid:

- 「做得更好看」
- 「注意细节」
- 「高级一点」
- 只记录某次坐标或一次性方案名

## Promotion Policy

- 同类问题出现 1 次：`observe`，或对客观基础质量问题直接 `capture`。
- 同类问题出现 2 次：`capture` 到反例/页面模式，并建议是否升级。
- 同类问题出现 3 次以上：`promote` 到 validation 或 SKILL 工作流。
- 被新规则覆盖的旧反馈要合并，避免文档膨胀。

## Regression Seeds

- 重新设计付费弹窗，只改版式：必须不是三卡近似变体；套餐区有明确栅格；关键区域无裁切。
- 设置页新增功能：必须走 production_mode，进入 row/block 体系，不新增大卡片。
