# Figma Source Guide

本文件保留源资料的使用解释。节点清单通过运行时索引和权威 metadata 查询，避免手工再维护一套目录。

| 需求 | 读取 |
| --- | --- |
| 场景入口、组件实例和展板 | `metadata/scene-index.yaml` |
| 有效源组、素材与失效节点 | `metadata/source-registry.yaml` |
| 可展示的具体源屏、状态与体验 profile | `metadata/source-frames.yaml` |
| 组件母版、属性与复用风险 | `metadata/components.yaml` |
| 页面和组件盘点快照 | `metadata/live-inventory.yaml` |

## Display Frame Resolution

源组用于导航；截图、导出与局改应解析到有效的 `screen_frame`，规则见 `source-frames.yaml > platform_display_contract`。失效节点只作历史线索。正式源稿是设计依据；产出页仅用于生成结果、续改或审核预览。

## Project Asset Lookup Sources

项目素材先使用 `query_runtime_index.py --intent locate --kind asset`，按 `source-registry.yaml` 的用途解析头像、StarBaby 2D/3D、图片、正式图标及图标候选。节点名称只是线索：结合父级、类型、尺寸、组件关系和截图扫描判断；语义弱匹配时返回带来源的少量视觉候选。外部素材仅在用户明确要求时查找。

## Variables

变量名称、取值、模式和绑定要求读取 `metadata/tokens.yaml`。写入前核验相关 live 变量；新增或修改文字执行 `typography.runtime_text_policy`。

## Component Catalog

目录读取 `metadata/components.yaml`，不在本文复制节点或状态。母版来源与响应式规则定点 live 核验；场景卡和展板只供定位对照。

## Local Visual Cache

资格和资产位置由 `metadata/visual-cache.yaml` 定义。匹配包括文件、节点、状态、模式和有效期；刷新须明确授权。缓存不能用于母版核验、生产验收或证明某状态不存在。

## Historical Context

以下仅保留历史人工盘点的独有线索，均需重新核验。历史产出 `4937:5749` 是内容组件分类预览，属于 output_only；不作为正式母版。日期分隔和场景索引节点统一从 `task-routes.yaml` / `scene-index.yaml` 读取。

旧版文字与效果样式记录如下，仅供识别源稿。当前新增文字使用默认文本引擎，效果值以 tokens 与 live 样式为准；历史记录不构成当前可用性证明。

## Text Styles

| Style | Font | Size / Line |
| --- | --- | --- |
| `Title/Article` | HYZhengYuan 85W | `22/30` |
| `Title/Page` | HYZhengYuan 95W | `22/22` |
| `Title/Section` | HYZhengYuan 85W | `20/20` |
| `Title/Card` | HYZhengYuan 85W | `18/26` |
| `Body/Article` | HYZhengYuan 55W | `18/30` |
| `Body/Comment` | HYZhengYuan 55W | `16/26` |
| `Body/Secondary` | HYZhengYuan 55W | `14/14` |
| `Caption/Default` | HYZhengYuan 55W | `12/12` |
| `Caption/Meta` | HYZhengYuan 55W | `10/10` |
| `Audio/Title` | HYZhengYuan 85W | `16/16` |
| `Tab/Label` | HYZhengYuan 85W | `18/18` |

本文件没有本地 paint styles，也没有本地 grid styles。颜色通过 variables 表达。

## Effect Styles

| Style | Effect |
| --- | --- |
| `PopoverMenu 弹出菜单` | `0 16px 32px #0000001F` |
| `Button 按钮` | `0 4px 4px #0000000A` |
| `BottomBar 底部栏` | `0 -4px 4px #0000000A` |
| `Card 卡片` | `0 4px 20px #0000000D` |
| `ImageTitle 图片标题` | `0 1px 2px #0000001F` |
