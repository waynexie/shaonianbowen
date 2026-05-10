# Comment System Module

模块名称：评论系统  
模块类型：高复用业务模块  
依赖：`../mvp-design-system-v0.1.md`  
适用范围：新闻详情页、话题页、活动页、个人动态、学习讨论、任何需要用户表达观点的内容场景。

## 1. 模块定位

评论系统不是单个 `CommentItem` 组件，而是一套完整的互动功能模式。它包含输入、评论列表、回复、点赞、展开、空态、加载、异常和未登录引导。

评论系统的设计目标：

- 鼓励青少年围绕新闻表达观点。
- 保持讨论区轻量、清晰、可阅读。
- 支持从详情页自然下滑进入讨论。
- 为后续话题页、活动页、学习讨论页复用。

## 2. 适用场景

默认适用：

- 新闻详情页底部评论区。
- 学习内容下的讨论区。
- 话题或活动页面。
- 个人中心的“评论”历史列表。

谨慎适用：

- 首页信息流，不建议直接展开完整评论区。
- 内容卡片内，不展示完整评论，仅展示评论数或入口。
- 强任务流程中，不应打断主操作。

## 3. 模块结构

标准结构：

```txt
CommentSection
  CommentInput
  CommentList
    CommentItem
      ReplyList
  LoadMoreReplies
  EmptyState
  LoadingState
  ErrorState
```

组成说明：

| 部分 | 用途 | 说明 |
| --- | --- | --- |
| `CommentInput` | 发表看法 | 可内嵌在详情页，也可进入独立输入页 |
| `CommentList` | 评论列表容器 | 控制加载、分页、空态 |
| `CommentItem` | 单条评论 | 头像、昵称、分数/等级、正文、地点、时间、操作 |
| `ReplyList` | 回复列表 | 最多展示两层关系，深层回复转为展开入口 |
| `EmptyState` | 无评论 | 使用轻量引导，例如“说点什么吧～” |
| `LoadingState` | 加载中 | 使用列表骨架 |
| `ErrorState` | 加载失败 | 提供重试 |

## 4. 操作路径

必须支持：

- 查看评论。
- 发表评论。
- 回复评论。
- 点赞或取消点赞。
- 展开更多回复。
- 加载更多评论。
- 未登录时引导登录。

可选支持：

- 删除自己的评论。
- 举报不当评论。
- 按热度/时间排序。
- 评论审核中状态。

## 5. 状态模型

| 状态 | 触发条件 | 设计要求 |
| --- | --- | --- |
| `empty` | 无评论 | 展示输入引导和空态文案 |
| `loading` | 首次加载 | 使用评论骨架，保留头像和文本节奏 |
| `loadingMore` | 加载下一页 | 列表底部显示轻量加载 |
| `error` | 加载失败 | 显示重试，不清空已有评论 |
| `unauthenticated` | 未登录操作 | 输入区变为登录引导 |
| `normal` | 有评论 | 列表自然阅读 |
| `withReplies` | 有回复 | 回复缩进展示 |
| `collapsedReplies` | 回复较多 | 显示“展开 N 条回复” |
| `submitting` | 发送中 | 输入区禁用或显示发送中 |
| `submitFailed` | 发送失败 | 保留输入内容，提供重试 |

## 6. 视觉与交互规则

视觉规则：

- 评论区左右边距遵循页面主边距 `20px`。
- 评论项不要做重卡片，优先使用留白和分割建立层级。
- 头像尺寸建议 `32px`，回复内头像可更小。
- 作者、时间、地点为辅助信息，使用 `Text 文本/T2 二级文本` 或 `Text 文本/T3 三级文本`。
- 正文使用 `Body/Primary` 或 `Body/Secondary`，保证可读行高。

交互规则：

- 回复最多展示两层视觉层级。
- 超出两层的回复进入展开列表或独立回复页。
- 点赞反馈必须即时，但失败时回滚或提示。
- 未登录用户可以浏览评论，但发表、回复、点赞时需要登录引导。
- 评论输入不应遮挡底部导航，需考虑安全区。

## 7. 嵌入兼容性

支持三种接入方式：

| 接入方式 | 场景 | 规则 |
| --- | --- | --- |
| 内嵌区块 | 新闻详情页 | 默认方式，放在正文和学习模块之后 |
| 半屏抽屉 | 首页卡片快速查看评论 | 适合轻量查看，不承载复杂回复链 |
| 独立页面 | 大量评论或话题讨论 | 适合排序、搜索、审核等高级能力 |

接入限制：

- 首页卡片内不直接放完整评论列表。
- 详情页评论区不应抢占正文和学习模块主层级。
- 半屏抽屉必须有明确关闭和返回路径。

## 8. 数据要求

最小数据：

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
  likeCount?: number;
  replyCount?: number;
  replies?: CommentData[];
}
```

模块级数据：

```ts
interface CommentSectionData {
  targetId: string;
  targetType: 'article' | 'topic' | 'activity' | 'profile';
  totalCount: number;
  comments: CommentData[];
  currentUser?: {
    id: string;
    name: string;
    avatarUrl?: string;
  };
  permissions: {
    canComment: boolean;
    canReply: boolean;
    canLike: boolean;
  };
}
```

## 9. 工程映射

建议组件：

- `CommentSection`
- `CommentInput`
- `CommentList`
- `CommentItem`
- `ReplyList`
- `CommentEmptyState`
- `CommentSkeleton`
- `CommentErrorState`

实现规则：

- `CommentSection` 负责数据状态和列表结构。
- `CommentItem` 只负责单条评论展示和局部操作。
- 回复展开逻辑不要写死在页面里，应作为模块能力。
- 未登录、禁言、审核中等状态由模块处理，页面只传入权限和用户状态。

## 10. 审核清单

设计审核：

- 是否覆盖空、加载、异常、未登录、发送失败。
- 回复层级是否清晰且不过深。
- 评论区是否没有压过正文主内容。
- 输入区是否考虑底部安全区。

产品审核：

- 评论是否适合该页面目标。
- 未登录引导是否自然。
- 是否需要举报、删除、审核中。
- 文案是否适合青少年表达场景。

工程审核：

- 是否可嵌入详情页、抽屉和独立页。
- 是否支持分页和回复展开。
- 是否保留失败重试和发送失败恢复。
- 是否没有把评论逻辑散落在页面组件里。
