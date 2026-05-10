# 少年博文 Figma-to-Code Rules v0.1

用途：指导前端或 AI coding agent 将 Figma 设计稿转成工程页面。  
当前状态：项目尚未沉淀成熟前端组件库，本文件先提供映射建议，不强行写入 `AGENTS.md` 或具体框架配置。  
来源：`mvp-design-system-v0.1.md`、Figma `给开发` 页面节点 `66:4169`。

相关模块规格：

- 评论系统：`modules/comment-system.md`
- 音频控件：`modules/audio-player.md`

## 1. 基本原则

- Figma 输出是设计参考，不是最终代码结构。
- 工程实现优先抽象稳定组件，不逐层复刻散乱 Frame/Group。
- 颜色必须使用语义 token，不直接硬编码 `.base_color 基础色`。
- 页面状态必须显式建模：正常、空、加载、异常。
- 评论、音频等复杂能力必须按模块实现，不散落到页面组件里。
- 长文内容不能固定高度，必须允许自然流式排版。
- 图标字体字符需要替换为工程可维护的图标组件或 SVG 资产。

## 2. 推荐目录结构

如果项目使用 React / Vue / 小程序等框架，可按类似结构沉淀：

```txt
src/
  components/
    ui/
    content/
    navigation/
    feedback/
  pages/
    home/
    article-detail/
    profile/
  styles/
    tokens.css
    typography.css
```

如果当前项目还没有前端代码，先使用此结构作为后续初始化建议，不需要现在强行创建。

## 3. 设计 token 映射

### 3.1 CSS 变量建议

将 Figma `Color_Token 颜色语义` 映射为 CSS 变量：

```css
:root {
  --color-brand-primary: #9ae600;
  --color-brand-primary-text: #75ce00;
  --color-brand-primary-bg: #f4f7f0;
  --color-brand-soft-bg: #e7f9c2;

  --color-text-t1: #333333;
  --color-text-t2: #5c5c5c;
  --color-text-t3: #999999;
  --color-text-t4: #ffffff;
  --color-text-t5: #ffffff;
  --color-text-green: #75ce00;

  --color-bg-page-green: #f4f7f0;
  --color-bg-page-grey: #f5f5f5;
  --color-bg-page-white: #ffffff;
  --color-bg-block: #f7f7f7;
  --color-bg-card: #ffffff;
  --color-bg-audioplay: #171717;
  --color-bg-placeholder: #f5f5f5;

  --color-border-default: #e6e6e6;
  --color-divider-thin: #f0f0f0;
  --color-divider-strong: #f5f5f5;
  --color-divider-vertical: #b7b7b7;
  --color-brand-green: #9ae600;
  --color-white: #ffffff;
  --color-black: #121212;

  --color-success-text: #75ce00;
  --color-success-bg: #e9f9e5;
  --color-success-border: #69b900;
  --color-info-text: #2f80ed;
  --color-info-bg: #eaf4ff;
  --color-info-border: #9eceff;
  --color-warning-text: #ed4d20;
  --color-warning-bg: #fff6c8;
  --color-warning-border: #feba0e;
  --color-danger-text: #e6526d;
  --color-danger-bg: #ffecf0;
  --color-danger-border: #ff4a71;
  --color-disabled-text: #a9a9a9;
  --color-disabled-bg: #f5f5f5;
  --color-disabled-border: #e6e6e6;
  --color-overlay-mask: #121212;
}

[data-theme="dark"] {
  --color-brand-primary: #9ae600;
  --color-brand-primary-text: #75ce00;
  --color-brand-primary-bg: #111a08;
  --color-brand-soft-bg: #18240d;

  --color-text-t1: #ffffff;
  --color-text-t2: #a9a9a9;
  --color-text-t3: #696969;
  --color-text-t4: #ffffff;
  --color-text-t5: #ffffff;
  --color-text-green: #75ce00;

  --color-bg-page-green: #111a08;
  --color-bg-page-grey: #171717;
  --color-bg-page-white: #1f1f1f;
  --color-bg-block: #2b2b2b;
  --color-bg-card: #2b2b2b;
  --color-bg-audioplay: #292929;
  --color-bg-placeholder: #171717;

  --color-border-default: #303030;
  --color-divider-thin: #292929;
  --color-divider-strong: #121212;
  --color-divider-vertical: #474747;
  --color-brand-green: #9ae600;
  --color-white: #ffffff;
  --color-black: #121212;

  --color-success-text: #75ce00;
  --color-success-bg: #111a08;
  --color-success-border: #69b900;
  --color-info-text: #9eceff;
  --color-info-bg: #102033;
  --color-info-border: #9eceff;
  --color-warning-text: #fec925;
  --color-warning-bg: #2b2208;
  --color-warning-border: #feba0e;
  --color-danger-text: #ff4a71;
  --color-danger-bg: #2a1218;
  --color-danger-border: #ff4a71;
  --color-disabled-text: #999999;
  --color-disabled-bg: #171717;
  --color-disabled-border: #5c5c5c;
  --color-overlay-mask: #121212;
}
```

注意：

- `Text 文本/T1 一级文本`、`Text 文本/T2 二级文本`、`Text 文本/T3 三级文本` 已改为引用标准灰阶原子，替换前需保证色值完全一致。
- `Text 文本/T5 半透明白` 和 `.base_color 基础色` 中的 `White_80 白色80`、`E6_80 灰E6_80` 在 Figma 读取中显示为带 alpha 的 hex，工程侧应保留透明度语义。
- 暗色模式中的品牌/功能色背景保留色相，不使用纯灰替代，例如 `--color-brand-primary-bg`、`--color-info-bg`、`--color-warning-bg`。

### 3.2 Typography token 建议

目标字体为 `HYZhengYuan`：

- `95W` 只用于页面级标题。
- `85W` 为全局加粗体。
- `55W` 为全局常规体。

```css
:root {
  --font-family-brand: "HYZhengYuan", "Noto Sans SC", sans-serif;
  --font-family-fallback: "Noto Sans SC", sans-serif;

  --font-weight-page-title: 950; /* HYZhengYuan 95W */
  --font-weight-bold: 850;       /* HYZhengYuan 85W */
  --font-weight-regular: 550;    /* HYZhengYuan 55W */

  --font-size-10: 10px;
  --font-size-12: 12px;
  --font-size-14: 14px;
  --font-size-16: 16px;
  --font-size-18: 18px;
  --font-size-20: 20px;
  --font-size-22: 22px;

  --line-height-12: 12px;
  --line-height-14: 14px;
  --line-height-16: 16px;
  --line-height-20: 20px;
  --line-height-22: 22px;
  --line-height-26: 26px;
  --line-height-30: 30px;

  --text-page-title-size: 22px;
  --text-page-title-line: 22px;
  --text-article-title-size: 22px;
  --text-article-title-line: 30px;
  --text-section-title-size: 20px;
  --text-section-title-line: 20px;
  --text-card-title-size: 18px;
  --text-card-title-line: 26px;
  --text-article-body-size: 18px;
  --text-article-body-line: 30px;
  --text-comment-body-size: 16px;
  --text-comment-body-line: 26px;
}
```

工程注意：

- 如果 Web/CSS 无法表达 `850`、`950` 的真实字重，需要通过 font-face 映射到具体字体文件。
- 不要把页面级 95W 用到卡片标题、正文、音频标题或 tabs。

### 3.3 尺寸 token 建议

```css
:root {
  --page-width-mobile: 390px;
  --page-padding-x: 20px;
  --content-width-mobile: 350px;
  --status-bar-height: 44px;
  --bottom-tab-height: 80px;
  --audio-player-height: 52px;
  --icon-button-size: 36px;
  --touch-target-min: 44px;

  --space-4: 4px;
  --space-6: 6px;
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-20: 20px;
  --space-24: 24px;
  --space-28: 28px;

  --icon-size-16: 16px;
  --icon-size-20: 20px;
  --icon-size-24: 24px;
  --icon-size-32: 32px;

  --avatar-size-24: 24px;
  --avatar-size-32: 32px;
  --avatar-size-40: 40px;
  --avatar-size-56: 56px;

  --button-height-32: 32px;
  --button-height-36: 36px;
  --button-height-44: 44px;
  --button-height-52: 52px;

  --news-card-width: 350px;
  --audio-player-button-size: 36px;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-pill: 999px;

  --stroke-border-none: 0;
  --stroke-border-hairline: 0.5px;
  --stroke-border-default: 1px;
  --divider-thin-height: 1px;
  --divider-strong-height: 8px;

  --opacity-disabled: 0.4;
  --opacity-read: 0.64;
  --opacity-pressed: 0.72;
  --opacity-overlay: 0.6;
  --opacity-image-mask: 0.36;
  --opacity-skeleton-low: 0.08;
  --opacity-skeleton-high: 0.16;

  --shadow-button: 0 4px 4px rgb(0 0 0 / 4%);
  --shadow-tabbar: 0 -4px 4px rgb(0 0 0 / 4%);
  --shadow-card: 0 4px 20px rgb(0 0 0 / 5%);
  --shadow-image-title: 0 1px 2px rgb(0 0 0 / 12%);
  --shadow-popover-menu: 0 16px 32px rgb(0 0 0 / 12%);
}
```

Figma 中对应变量集合为 `Size 尺寸`、`Stroke 描边`、`Opacity 透明度`。字体使用 Text Styles，投影使用 Effect Styles，不再拆成变量。

`Motion` 与 `z-index` 暂不进入 Figma 变量。工程实现时可按组件需要在代码层维护，避免 MVP 设计系统变量过细。

## 4. 组件映射

| Figma 概念 | 工程组件建议 | 说明 |
| --- | --- | --- |
| `NewsCard` | `NewsCard` | 首页信息流卡片组件集，含推荐数、已读、加载状态 |
| `top` / 顶部区域 | `TopBar` | 首页问候、详情返回/分享、个人中心头部 |
| `tabbar` | `BottomTabBar` | 一级导航，高度 80px |
| `AudioPlayerBar` | `AudioPlayerBar` | 音频播放入口和状态 |
| `title` | `SectionTitle` | 模块标题，可带图标或操作 |
| `tabs` | `SegmentTabs` / `FeatureGridItem` | 根据表现拆成切换 tab 和功能入口 |
| `评论` | `CommentItem` | 评论正文、回复、点赞、展开 |
| `EmptyPlaceholder` | `EmptyState` | 空内容、空评论、空收藏等 |
| 骨架图 | `SkeletonCard` / `SkeletonBlock` | 保持最终布局节奏 |
| `footer` | `ListFooter` | `已经到底啦～` |
| 图标字符 | `Icon` | 替换为 SVG 或统一图标库 |

模块级映射：

| 模块 | 工程模块建议 | 说明 |
| --- | --- | --- |
| 评论系统 | `CommentSection` | 统一处理输入、列表、回复、权限、加载、异常 |
| 音频控件 | `AudioPlayer` / `AudioPlayerBar` | 统一处理播放状态、进度、失败、互斥播放 |

## 5. 页面实现规则

### 5.1 首页

推荐组件树：

```txt
HomePage
  StatusBarSafeArea
  HomeTopBar
  AudioPlayerBar?
  SectionHeader
  GeneratePdfButton?
  NewsFeed
    NewsCard[]
    SkeletonCard[]
    EmptyState?
  ListFooter?
  BottomTabBar
```

实现要求：

- 列表数据应支持分页或下拉刷新预留。
- `NewsCard` 必须支持推荐人数不同状态。
- 生成 PDF 按钮是业务动作，不要和普通筛选按钮混用。

### 5.2 详情页

推荐组件树：

```txt
ArticleDetailPage
  DetailTopBar
  ArticleHero
  AudioPlayerBar
  ImpactSummaryCard
  SegmentTabs or FeatureGrid
  ArticleModuleContent
  CommentSection
  BottomTabBar or DetailActionBar
```

实现要求：

- 正文内容自然流式排版，不限制固定高度。
- 文笔年龄段、字数、模块 tab 需要由数据驱动。
- 评论区可懒加载，但空态必须完整。
- 上滑后顶部吸附态应作为滚动状态处理，不复制另一个页面。

### 5.3 个人中心

推荐组件树：

```txt
ProfilePage
  ProfileHeader
  LearningStats
  ProfileContentTabs
  ProfileArticleList
  EmptyState?
  BottomTabBar
```

实现要求：

- `学习天数`、`阅读文章数` 应为独立数据字段。
- `看过`、`评论`、`赞过`、`收藏` 使用同一 tabs 组件。
- 每个分类都需要空态。

## 6. 状态数据模型建议

### NewsCard

```ts
type NewsCardState = 'default' | 'read' | 'loading';

interface NewsCardData {
  id: string;
  title: string;
  source: string;
  publishedAt: string;
  location?: string;
  topic?: string;
  coverUrl?: string;
  recommenders?: string[];
  recommendCount?: number;
  state?: NewsCardState;
}
```

### ArticleDetail

```ts
type ArticleModuleKey =
  | 'original'
  | 'examPoints'
  | 'writingQuotes'
  | 'opinions'
  | 'bilingual'
  | 'dailyPaper';

type ReadingLevel = 'under10' | 'age11To14' | 'age15Plus';

interface ArticleDetailData {
  id: string;
  title: string;
  source: string;
  publishedAt: string;
  location?: string;
  distanceText?: string;
  audio?: {
    title: string;
    duration: string;
  };
  impactSummary?: string;
  readingLevel?: ReadingLevel;
  modules: ArticleModuleKey[];
}
```

### Comment

```ts
interface CommentData {
  id: string;
  authorName: string;
  avatarUrl?: string;
  score?: number;
  content: string;
  location?: string;
  dateText: string;
  liked?: boolean;
  replies?: CommentData[];
}
```

这些类型是工程建议，不是已经存在的公共 API。落地到实际项目时，应按项目框架和数据接口调整命名。

## 7. Figma MCP 实现流程

当 AI coding agent 从 Figma 实现页面时，必须按以下流程：

1. 使用 Figma MCP 读取目标节点的设计上下文和截图。
2. 判断目标节点属于首页、详情页、个人中心或局部组件状态。
3. 查阅 `mvp-design-system-v0.1.md` 和本文件。
4. 将设计拆成工程组件，而不是逐层复刻 Figma Frame。
5. 将颜色替换成 CSS variables 或项目 token。
6. 下载并保存必要图片资源；如果 Figma 返回可用 asset URL，不使用占位图替代。
7. 实现正常态、空态、加载态、异常态。
8. 本地运行页面并做截图检查。

## 8. 不允许的实现方式

- 不允许把 Figma 的 `Group 6`、`Frame 13` 等临时名称直接作为组件名。
- 不允许把 `#9AE600`、`#333333` 等颜色散落在业务组件里。
- 不允许通过绝对定位复刻整页布局，除非是图标内部或不可避免的视觉层。
- 不允许为每个新闻状态写一个独立组件。
- 不允许在工程里继续使用图标字体乱码字符作为语义图标。
- 不允许只有正常态，没有空、加载、异常态。

## 9. 接入 Code Connect 的建议

后续 Figma 组件库整理后，可建立以下映射：

| Figma Component | Code Component |
| --- | --- |
| `NewsCard` | `src/components/content/NewsCard` |
| `AudioPlayerBar` | `src/components/content/AudioPlayerBar` |
| `TopBar` | `src/components/navigation/TopBar` |
| `BottomTabBar` | `src/components/navigation/BottomTabBar` |
| `SectionTitle` | `src/components/ui/SectionTitle` |
| `SegmentTabs` | `src/components/ui/SegmentTabs` |
| `CommentItem` | `src/components/content/CommentItem` |
| `EmptyState` | `src/components/feedback/EmptyState` |
| `SkeletonCard` | `src/components/feedback/SkeletonCard` |

建议顺序：

1. 先整理 Figma Component Set。
2. 再建立工程组件。
3. 最后补 Code Connect 映射。

## 10. 验收清单

实现完成后必须检查：

- 首页、详情页、个人中心三个 MVP 场景均可用。
- 页面宽度 `390px` 下视觉与 Figma 方向一致。
- 所有颜色来自 token。
- 所有内容状态完整。
- 长标题、长正文、长评论不溢出。
- 底部导航不遮挡内容。
- 图标有可维护来源和可访问名称。
- 没有把 Figma 临时 Frame 名称泄露到公开组件 API。
