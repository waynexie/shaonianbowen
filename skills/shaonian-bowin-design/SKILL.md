---
name: shaonian-bowin-design
description: 查询、生成、调整、发散探索或检查「少年博闻」移动端设计稿时使用。适用于基于 Figma 文件
  oULxBlEvFNkWGGVaJ0ClEz 创建或修改 390x844
  移动端页面、复用变量与组件、完成生产级局部改造、页面设计、多方案探索，以及沉淀用户反馈为设计规则。
metadata:
  version: "2026.11.01.2"
  execution_target: codex-local
  source_execution_target: cloud
  display_name: Bowin Design
  author: 腾讯新闻设计中心Waynexie
  maintainer: Waynexie
  copyright: Copyright © 2026 Tencent
---
# 少年博闻设计 Skill

服务少年博闻移动端 Figma 的查询、局部改造、新页面探索、组件设计与验收。默认画布为 390×844；已有源屏按真实尺寸处理。当前回合要求决定目标，同一对话续改优先复用已核验节点、截图、组件和 session，只补查新增依赖。

## 规则归属

机器可读规则以 `references/metadata/*.yaml` 为唯一权威；Markdown 解释判断与操作，运行时 JSON 是派生索引。发生冲突时按对应权威小节执行；live Figma 提供当前节点、组件、变量与渲染事实。

| 领域 | 权威位置 |
| --- | --- |
| 任务路由、速度层、质量档、模式、文件与写入范围、画布排布 | `task-routes.yaml` |
| 必需证据、通过条件、阻断与交付检查 | `validation.yaml` |
| 场景入口、实例及展板关系 | `scene-index.yaml` |
| 源组与素材注册、失效记录 | `source-registry.yaml` |
| 可展示屏幕、状态与体验 profile | `source-frames.yaml` |
| 组件母版定位、属性、复用与结构风险 | `components.yaml` |
| 变量与样式 | `tokens.yaml` |
| 最近核验的页面与组件库存 | `live-inventory.yaml` |
| 截图缓存匹配、新鲜度与显式刷新 | `visual-cache.yaml` |
| 中英术语 | `glossary.yaml` |

页面体验经验由 `references/screen-patterns.md` 维护，装配方法由 `references/page-recipes.md` 维护。具体节点数据通过索引读取；专题文档按任务需要加载。

通用设计取舍与新功能接入分别由 `design-decision-matrix.md`、`feature-insertion.md` 解释；常规看图与失败诊断分别由 `design-quality.md`、`visual-failures.md` 负责。指南不另设参数表或必填报告。Token 绑定统一读取 `validation.yaml > minimum_token_binding_check`；任务字段共用 `pre_generation_checks.decision_records.evidence_reuse_contract` 定义的记录。

## 最小读取入口

命令相对本 Skill 根目录执行。依赖见 `requirements.txt`，运行时不临时联网安装。

本机安装已配置独立 Python 环境：下文和引用文档中的 `python3` 命令使用 `~/.codex/skill-runtimes/shaonian-bowin-design/bin/python` 执行，或在当前 shell 先运行 `source ~/.codex/skill-runtimes/shaonian-bowin-design/bin/activate`。不要使用缺少 PyYAML 的系统 Python；环境缺失时报告依赖问题。本地适配仅调整入口格式与解释器位置，设计规则及授权范围不变。

1. 语义先行：用户查既有内容时只读；已有上下文变化走局改；组件结构走组件 route；新页面或明确重设计走探索 route。普通查询找不到不能自动生成。
2. 首次读取一个执行配置：`python3 scripts/read_execution_profile.py tier|quality|profile|route <名称> --compact`。路由、速度层与质量档分别判断；不因关键词出现“正式稿”就把查询改成写入。
3. 需要定位时：`python3 scripts/query_runtime_index.py "<精确目标>" --intent locate --compact`；明确要图片或准备写入，直接选 `--intent visualize` / `--intent write`。仅精确唯一目标使用 `--limit 1`，宽泛场景保留候选。
4. 即将写入、证据陈旧或存在歧义时，用 `python3 scripts/read_metadata_section.py <metadata.yaml> <section.path>` 定点读权威小节；必读集合由 `validation.yaml > metadata_authority_gate_check` 和所选 route profile 决定。权威读取失败时不写入。
5. 记录 route 所需最小证据；字段从 `task-routes.yaml > route_profiles`、`turn_intent_contract` 和 `validation.yaml > figma_design_judgment_check` 取得。执行细节按需读 `references/figma-workflow.md` 对应小节。

索引脚本按源摘要检查并重建派生 JSON。质量辅助命令 `evaluate_quality_gate.py route "<需求>" [--intent <语义>]` 仅建议分档，不能授予写入权限；混合或不明确意图保持只读，由 Agent 结合上下文解决。`validate <evidence.json>` 只核对其声明范围内的证据，不能代替实际截图和完整 route 验收，范围及输入见 `validation.yaml > quality_evaluator_contract`。

## 查询与展示

普通查询只读 `lookup_profile` 和匹配索引，不加载整套指南。查询、Dark 同节点预览、缓存资格与图片交付按 `references/figma-workflow.md > Lookup Fast Path` 执行；缓存不能证明当前母版有效，查询不到不能自动生成。页面数量区分业务屏幕与 Figma 技术 Page，读取 `global_defaults.semantic_ambiguity_routing`。

## 设计执行边界

- 普通设计只写 `task-routes.yaml > global_defaults` 指定的固定产出页；明确授权的正式组件库维护、场景索引维护分别执行 `persistent_write_scope` 的精确 allowlist。授权维护与普通输出各走自己的范围检查。
- 已有页面的局部视觉草稿使用 `source_locked_visual_draft`：精确源 Frame 的完整截图锁定目标区之外，只重建目标区。新页面、正式稿和完整原生可编辑产出使用 `direct_native_construction`；策略细则见 `global_defaults.context_strategy_routing`。草稿底图不能作为生产稿底层。
- 已登记组件族在所有质量档都复用正式实例、现有变体或同族扩展。写前定点核验 live 母版、属性、slot、变量与响应式规则；记录来源、交付实例和属性变化。场景示例和展板只作定位，不代替母版或响应式验收。
- 新增、修改文字使用 MCP 默认文本引擎；未触及的正式源文字保持原样。弹窗先按语义选 Overlay 家族。
- 普通产出在一次 `use_figma` 调用中读取最新产出页子节点，使用唯一 `task_id` 完成任务容器、当日分隔、全部方案、落位与碰撞复核。具体排布值从 `global_defaults.canvas_placement_policy` 读取。
- 结构化标注按 `global_defaults.structured_annotation_routing` 解析 fileKey、nodeId、surface 与坐标；目标冲突时停止依赖该目标的写入。
- 所有档位实际检查每个方案整屏截图、锁定区和组件实例。草稿的允许缺口记录为 `production_gaps`；正式稿补齐 Token、Auto Layout、适用的 Dark 和响应式检查。失败处只做对应修复与复查。
- 每个交付方案返回真实 Frame ID 和整屏截图，按 `global_defaults.generated_output_delivery` 逐帧交付；不把工具探测、索引命中或配置保存当作设计完成。

## 专题读取

| 任务需要 | 读取 |
| --- | --- |
| 操作步骤、局改、续改、原子落位、验收衔接 | `references/figma-workflow.md` 的匹配小节 |
| 设计取舍、主任务、视觉权重、方案主张 | `references/design-decision-matrix.md` |
| 品牌语言与截图审美判断 | `references/design-language.md`、`references/design-quality.md` |
| 页面体验 / 页面装配 | `references/screen-patterns.md` 的匹配 profile / `references/page-recipes.md` 的匹配 recipe |
| 新功能插入已有页面 | `references/feature-insertion.md` |
| 组件任务 | `references/component-audit.md` 与相关 `component-*.md` |
| 外部模式研究 | `references/external-reference-patterns.md` |
| 项目素材、源导航说明 | `references/source-index.md` |
| 反馈沉淀或重复失败 | `references/feedback-intake.md`、`references/visual-failures.md` |

## Skill 维护

修改规则先定位权威文件，指南只保留解释和独有示例。相同规则更新原定义，不再复制一段；组件参数只在目录维护。节点身份放 metadata；场景通过源屏 ID 引用，运行时负责解析。删除文件或章节同步迁移全部引用；改脚本契约同步入口和回归用例。保持写入范围、正式组件复用和真实截图门禁。反馈维护时才加载 `references/feedback-intake.md`，性能基准和发布记录不属于日常设计必读。

完整自检入口为 `python3 -m unittest discover -s scripts -p 'test_*.py'`；派生索引生成/检查为 `python3 scripts/build_runtime_indexes.py [--check]`。维护时按当前任务授权执行，不在普通设计查询中自动运行整套测试。版本更新记录见 `RELEASE_NOTES.md`。
