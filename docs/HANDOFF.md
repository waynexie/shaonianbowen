# 少年博文项目交接摘要

最后更新：2026-05-11

## 项目入口

- GitHub 仓库：https://github.com/waynexie/shaonianbowen
- Figma 文件：https://www.figma.com/design/mSPWVxdH0hfmkEZInx4vNg/%E5%B0%91%E5%B9%B4%E5%8D%9A%E6%96%87
- 重点页面：
  - `给开发`
  - `组件`
  - Variables 面板里的 `Base Color 基础色`、`Color Token 语义色`

另一台电脑继续时，先 clone：

```bash
git clone https://github.com/waynexie/shaonianbowen.git
```

然后在 Codex 里打开 clone 下来的项目目录。

## 当前状态

这个仓库主要保存项目文档和设计系统说明。Figma 画布、变量、组件改动已经写入 Figma 云端文件，不会通过 Git 保存；另一台电脑登录同一个 Figma 账号打开上面的 Figma 链接即可。

Codex 对话历史可能不会跨设备完整同步。另一台电脑如果没有这条历史，把本文件内容贴给 Codex 即可接续。

## 已完成的 Figma 工作

### 变量绑定整理

- 对 `给开发` 页面做过一轮样式变量绑定整理。
- 原则：
  - 只绑定本文档里的变量和样式。
  - 不绑定外部组件库变量。
  - 不为了绑定而绑定，数值和属性必须匹配。
  - 无样式的元素不凭空添加样式。
- 清理过临时变量：
  - 删除过 `Auto 本页/*`
  - 删除过 `Comment 评论/Icon/*` 里的颜色变量
  - 删除过 `Typography 字体`
- 图标颜色不单独建变量，直接使用现有语义色或功能色。

### 标签玻璃背景

- 标签背景新增并使用：
  - `Gray 灰度/ABABAB 40%`
- 值：
  - `#ABABAB`
  - alpha `40%`
- 用途：
  - 图片上的标签背景
  - 配合 `Background blur = 20`
- 注意：
  - 标签背景不要使用 `T4/T5` 文字色。

### 组件页变量绑定

- 对 Figma 节点 `66:4011` 所在的 `组件` 页面做过变量绑定。
- 只绑定已有样式和精确匹配变量。
- 修正过图标矢量误绑：
  - 不应把图标黑色误绑到 `Bg 背景/Audio 音频播放`
  - 不应把图标黑色误绑到 `Line 线条/Border 描边`
  - 应按语义使用 `Text 文本/T1 主要`

### 给开发页组件替换

在 `给开发` 页面，把明确对应已有组件的普通 Frame/Group 替换为组件实例：

- 12 个首页信息流卡片替换为 `NewsCard` 实例。
- 14 个播放条替换为 `AudioPlayerBar` 实例。
- 1 个下载 PDF 底栏替换为 `tabbar / DetailActionBar` 实例。

替换原则：

- 有明确现成组件才替换。
- 匹配不确定的区域暂时不动。
- 不新建组件。
- 替换后复查过，剩余明确可替换候选为 0。

注意：

- `NewsCard` 实例文本覆盖时，Figma API 无法加载 `HYZhengYuan 55W/85W`，曾使用 `Noto Sans SC` 作为可写入 fallback。
- 如果后续需要严格恢复字体，建议在 Figma UI 中手动确认字体可用性。

### NewsCard 新变体

`NewsCard` 组件集里新增过一个专家推荐卡。

- 原默认名：`State=State6`
- 已改名：`State=ExpertRecommend`

当前 `NewsCard` 状态变体大致包括：

- `NoRecommend`
- `SingleRecommend`
- `FewRecommends`
- `Read`
- `Loading`
- `ExpertRecommend`

命名规则：继续使用 `State=<EnglishState>`。

### Accent 彩色变量扩展

在 `Color Token 语义色 / Accent 彩色` 下扩展了标准色和浅色变量。

已有并补齐 Code syntax：

- `Green 绿色`
- `Blue 蓝色`
- `Yellow 黄色`
- `Red 红色`
- `GreenSoft 浅绿色`
- `BlueSoft 浅蓝色`
- `YellowSoft 浅黄色`
- `RedSoft 浅红色`

新增色相：

- `Orange 橙色`
- `OrangeSoft 浅橙色`
- `Cyan 青色`
- `CyanSoft 浅青色`
- `Purple 紫色`
- `PurpleSoft 浅紫色`
- `Pink 粉色`
- `PinkSoft 浅粉色`

规则：

- 标准色使用基础色 `500`
- Soft 浅色使用：
  - light -> `50`
  - dark -> `900`
- 全部通过 alias 指向 `Base Color 基础色`，不要写死孤立值。

新增或补齐的基础色阶：

- `Orange 橙色/900`
- `Cyan 青色/50`
- `Cyan 青色/500`
- `Cyan 青色/900`
- `Purple 紫色/50`
- `Purple 紫色/500`
- `Purple 紫色/900`
- `Pink 粉色/50`
- `Pink 粉色/500`
- `Pink 粉色/900`

### Code syntax

已经补齐：

- `Base Color 基础色`
- `Color Token 语义色`

审计结果：

- 颜色变量缺失 Code syntax 数量：0

命名模式：

- WEB：`--color-accent-green-soft`
- Android：`colorAccentGreenSoft`
- iOS：`colorAccentGreenSoft`

示例：

- `Accent 彩色/Orange 橙色`
  - WEB `--color-accent-orange`
  - Android/iOS `colorAccentOrange`
- `Accent 彩色/OrangeSoft 浅橙色`
  - WEB `--color-accent-orange-soft`
  - Android/iOS `colorAccentOrangeSoft`

## 后续工作注意事项

- 修改 Figma 前先检查已有变量、组件和命名规则。
- 不要新增临时变量，除非用户明确要求。
- 新增变量时：
  - 放到正确 collection/group。
  - 设置 light/dark。
  - 优先 alias 到基础色。
  - 设置合理 scopes。
  - 同步补 Code syntax。
- 替换页面元素为组件时：
  - 只替换确定匹配的结构。
  - 不确定则保持原样。
  - 替换后检查文本、图片、尺寸和主组件引用。
- Figma 文件是云端真源，Git 仓库只负责项目文档和本地协作资料。

