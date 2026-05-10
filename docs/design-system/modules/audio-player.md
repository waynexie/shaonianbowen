# Audio Player Module

模块名称：音频控件  
模块类型：高复用业务模块  
依赖：`../mvp-design-system-v0.1.md`  
适用范围：首页速听、详情页听全文、学习跟读、迷你播放器、底部或吸附播放状态。

## 1. 模块定位

音频控件用于降低青少年阅读新闻的进入门槛，让用户可以先听摘要、听全文或进行中英跟读。它不是普通按钮，而是带播放状态、进度、失败处理和场景兼容性的业务模块。

模块目标：

- 让用户快速理解内容。
- 在首页和详情页都保持一致的播放体验。
- 支持播放、暂停、加载、失败、完成等状态。
- 为后续跟读、后台播放、迷你播放器预留扩展。

## 2. 适用场景

默认适用：

- 首页：今日大事速听。
- 详情页：听全文、速听新闻。
- 中英对照：跟读或听句子。
- 生成内容：播放生成后的简报。

谨慎适用：

- 新闻卡片列表中不建议每张卡片都放完整播放器。
- 表单或设置页只放音频开关，不放播放条。

## 3. 模块结构

标准结构：

```txt
AudioPlayer
  PlayButton
  Title
  Duration
  Progress
  Waveform or ProgressBar
  ErrorMessage
```

v0.1 形态：

- `AudioPlayerBar`：内嵌在首页或详情页的横向播放条。
- `InlineListenButton`：学习模块中的跟读/听句子入口。
- `MiniPlayer`：后续可扩展的吸附或底部迷你播放器。

## 4. 状态模型

| 状态 | 触发条件 | 设计要求 |
| --- | --- | --- |
| `idle` | 未播放 | 展示播放入口、标题和时长 |
| `loading` | 请求音频或缓冲 | 播放按钮进入加载态，保留条高度 |
| `playing` | 正在播放 | 展示暂停入口和进度 |
| `paused` | 暂停 | 保留当前进度 |
| `ended` | 播放完成 | 进度到末尾，可重新播放 |
| `error` | 音频加载失败 | 显示重试或轻提示 |
| `disabled` | 无音频 | 不展示或展示不可用说明 |

## 5. 视觉与交互规则

已观察到：

- `AudioPlayerBar` 常见尺寸为 `350px x 52px`。
- 背景使用 `Bg 背景/Bg_Audioplay 音频播放`。
- 文案包括 `听全文`、`速听今日大事`、`08:00`。

视觉规则：

- 横向播放条宽度跟随主内容宽度 `350px`。
- 高度默认 `52px`。
- 背景使用深色，与白卡片区分。
- 播放按钮必须醒目，但不抢过新闻标题。
- 时长和进度信息使用清晰短文本。

交互规则：

- 点击播放按钮切换播放/暂停。
- 加载中禁止重复触发。
- 失败后提供重试，不让整页进入错误态。
- 详情页滚动时可选择保持原位或升级为迷你播放器。
- 同一页面同时只能有一个主音频处于播放中。

## 6. 嵌入兼容性

| 接入方式 | 场景 | 规则 |
| --- | --- | --- |
| 内嵌播放条 | 首页、详情页 | 默认形态，占据主内容宽度 |
| 行内听句子 | 中英对照、跟读 | 用小按钮，不使用完整播放条 |
| 迷你播放器 | 滚动或跨页面播放 | 后续扩展，需处理底部导航安全区 |
| 底部吸附 | 长文阅读 | 不遮挡评论输入和底部导航 |

兼容限制：

- 首页信息流中避免多个完整播放器连续出现。
- 评论输入、底部导航和迷你播放器不能互相遮挡。
- 播放器失败不应影响正文阅读。

## 7. 数据要求

最小数据：

```ts
interface AudioSourceData {
  id: string;
  title: string;
  durationText: string;
  src?: string;
  transcriptId?: string;
  available: boolean;
}
```

播放状态：

```ts
type AudioPlayerState =
  | 'idle'
  | 'loading'
  | 'playing'
  | 'paused'
  | 'ended'
  | 'error'
  | 'disabled';
```

模块配置：

```ts
interface AudioPlayerConfig {
  variant: 'bar' | 'inline' | 'mini' | 'sticky';
  source: AudioSourceData;
  state: AudioPlayerState;
  progress?: number;
  errorMessage?: string;
}
```

## 8. 工程映射

建议组件：

- `AudioPlayerBar`
- `InlineListenButton`
- `MiniPlayer`
- `AudioProgress`
- `PlayPauseButton`

实现规则：

- 播放状态应由统一音频控制层管理，不散落到每个页面。
- 页面只传入音频 source 和展示 variant。
- 播放失败只影响音频模块，不影响正文内容。
- 如果存在全局播放能力，页面内播放器需要和全局播放器同步状态。

## 9. 审核清单

设计审核：

- 是否覆盖 idle、loading、playing、paused、error。
- 是否不遮挡底部导航、评论输入或正文。
- 是否在浅色页面中有足够对比。
- 是否区分完整播放条和行内跟读按钮。

产品审核：

- 该场景是否真的需要音频。
- 播放内容是摘要、全文还是句子。
- 是否需要 transcript、跟读或下载能力。

工程审核：

- 是否有统一播放状态。
- 是否处理同时播放多个音频的冲突。
- 是否有失败重试和无音频 fallback。
- 是否能兼容详情页滚动和后续迷你播放器。
