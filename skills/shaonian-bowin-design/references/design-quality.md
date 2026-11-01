# Design Quality

本文件提供截图判断方法，不增加独立门禁或交付表。适用质量档、通过条件和字段以 `metadata/validation.yaml` 为准；症状已明确时，转到 `visual-failures.md` 对应小节诊断与修复。

## Tier Interpretation

先读取 `universal_basic_visual_qa_check`、`registered_component_family_gate_check` 和当前任务适用的检查。Token 绑定引用 `minimum_token_binding_check`，其他生产缺口引用 `production_gaps_check`。不能把可延期的工程完整度与不可接受的视觉缺陷混为一谈。

以下问题帮助发现风险，不要求逐题写报告。按 `pre_generation_checks.decision_records.evidence_reuse_contract` 共用截图与记录。

## Focus And Weight

缩小整屏或眯眼观察：最先看到的内容是否对应当前用户任务？标题、标签、统计、音频和按钮不能同时争夺焦点。

- 信息流：标题与封面帮助选内容，来源提供可信度，统计与动作保持辅助。
- 个人中心：身份和历史不能被新工具或付费入口盖过。
- 付费弹层：可以聚焦购买决策，但不能让入口状态也变成促销海报。

页面顺序读取匹配的 `screen-patterns.md` profile；新增入口的存在方式读取 `feature-insertion.md`，不在此重设权重枚举。

## Grouping And Rhythm

看相邻关系和共同容器，而不只看单个元素：相关信息是否形成一个对象？组内距离是否比组间更近？重复项是否像同一种对象？

- 同一条新闻的来源、标签和动作不能拆成几个独立浮卡。
- 设置行、个人工具和筛选项属于同一任务时共享分组。
- 密集卡片后保留列表节奏；不要再接一排同样拥挤的筛选和操作。
- 同类标签与卡片继承一致的尺寸、轮廓和选中逻辑；差异必须有语义理由。

如果页面仍碎，先移除重复容器或弱信息，再调整间距。诊断见 `visual-failures.md > Density And Utility Weight`。

## Alignment And Readability

同时看整屏和密集区放大图。标题、说明、价格、右侧值是否共享可解释的边界与基线？换成长文案后，哪些容器会增高、换行或截断？

- 新设置行与最近同级源行比较，不凭视觉近似另设行高和文字位置。
- 协议、时长、评论昵称、回复和按钮文字是优先检查区。
- 图片上的文字需要源认可的对比处理，不能直接压在明亮复杂的画面上。
- 选中态、文字行动和图标行动能否被识别，不依赖说明文字解释“这里能点”。

参数取自 tokens 和组件目录。具体修复见 `Clipped Helper Text`、`Abnormal Padding`、`Alignment Drift` 等失败类型，不在本文件维护尺寸表。

## Context And Safety

局改用修改前后截图比较目标区之外，而不是只检查新增区域。正文、背景、导航、底栏和已有文案是否仍符合锁定范围？临时浮层是否意外挤动主内容？

固定控制区不能遮住正文、评论输入、脚本、协议或 CTA。源页面宽度、安全区、组件边界和浮层锚点要一起看；规则值与检查范围见 `layout_check`、`context_integrity_gate_check` 及对应模块检查。

## Product Fit And Maturity

判断结果是否是少年博闻的完成态视觉初稿，而不只是字段齐全的线框图。

- 媒体、组件状态和文案有真实来源，不用抽象矩形填满内容。
- 新频道沿用熟悉的导航和控件，让用户只学习必要的新内容模式。
- 外部参考被转译为层级、操作和状态表达，不直接带入其他产品的导航、图标体系或娱乐语气。
- 一屏只引入必要的新视觉概念，避免新导航、新图标和新卡片语法同时出现。

## Option Differentiation

把方案并排看，能否用不同的产品理由解释选择？一种可以先呈现身份，另一种可以先呈现任务；只换色、文案、阴影或极小间距不能构成新方向。

实际差异轴、记录和通过条件读取 `multi_solution_check`、`divergence_contract_check`，不另建方案验收表。

## Figma Self-Critique Gate

完成截图后，用以上方法检查适用区域，将结论写入 `figma_design_judgment_check` 定义的 `self_critique_result`。引用已有整屏、局部截图和组件证据，说明具体问题及修复结果，不重复填写一套通用问卷。

修复后更新受影响截图；声明为正式稿前仍需通过适用的完整 route 验收。辅助脚本只核对其声明的证据范围，不代替看图。
