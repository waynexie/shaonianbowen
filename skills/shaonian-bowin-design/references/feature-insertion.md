# Feature Insertion

Use this file before adding any new feature, entry, or channel element to an existing Shaonian Bowen mobile screen. The goal is to preserve page hierarchy: a new feature must first be classified by product role, then placed into the nearest existing page pattern and component family.

本文件只补充既有页面接入新功能的判断。通用主任务、容器和视觉权重见 `design-decision-matrix.md`；页面体验见匹配的 `screen-patterns.md` profile。枚举以 `task-routes.yaml > global_defaults.presence_role_taxonomy` 为准，门禁与字段以 `validation.yaml > feature_insertion_check`、`presence_role_fit_check` 为准；下表是选型解释，不额外建立记录表。

## Core Rule

New features are not designed from a blank canvas. Before drawing UI, decide what role the feature plays in the current page task hierarchy. If the role is unclear, do not create a new card, new component family, new color treatment, or new visual style.

## Role Matrix

| Feature role | User meaning | Preferred placement | Visual weight | Typical components |
| --- | --- | --- | --- | --- |
| Primary task | The main reason the user opens this page | Main content region or primary card area | High | `NewsCard`, article content, primary `ButtonApp` |
| Browsing decision | Helps decide whether to open/read/listen/comment | Inside feed card or list item | Medium-high | `NewsCard`, `CellReadingHistory`, media cover, tags, stats |
| Frequent support action | Used often but supports the main task | Same module as related content | Medium | row/cell, inline action, secondary button |
| Low-frequency utility | Useful but not central to reading/writing | Weak entry in existing profile/settings group | Low | `SettingsRow`, profile secondary entry, subtle row |
| Paid entry / subscription | Unlocks Plus or paid feature from a contextual touchpoint | Weak entry in profile, badge in card, or modal over current context | Medium in modal, low in page content | `Plus Badge`, `App Button`, subscription bottom sheet |
| Account operation | Changes user/session/account state | Separate account operation group | Medium-low | `SettingsRow` pattern, separated from normal settings |
| Risk or exit action | Destructive, irreversible, logout, privacy-sensitive | Bottom separated danger/action area | Special, isolated | `ButtonApp` danger/neutral pattern |
| Top-level channel | A peer of Home/Profile/Video | Full page with source bottom-navigation language | High at navigation level, normal in content | `HomeHeaderBar`, `TabBar`, preserved source bottom-navigation wrapper, feed/card patterns |
| Immersive audio task | Listening, AI radio, podcast, speaking/practice | Full-screen focused surface | High in current task, quiet elsewhere | `IconButton`, audio controls, dialogue bubbles |

## Presence Role

After choosing the product `feature_role`, choose how the new UI exists on the page. This is not a component-specific rule; it applies to entries, states, floating controls, sheets, progress, media, AI tools, and any ongoing task UI.

| Presence role | Meaning | Attention budget | Default state |
| --- | --- | --- | --- |
| `primary_surface` | Owns the current user task | High | Expanded |
| `inline_entry` | Embedded entry inside existing content or a list item | Medium/low | Inline or collapsed |
| `contextual_state` | Local status inside an existing component | Low/minimal | Inline |
| `persistent_companion` | Long-lived or cross-page control that stays reachable while another task remains primary | Low/minimal | Collapsed or hidden until triggered |
| `transient_feedback` | Short-lived feedback after an action | Minimal/low | Hidden until triggered |
| `modal_decision` | Focused or blocking decision surface | High/medium | Expanded |

`feature_role` says why the feature exists; `presence_role` says how loudly it may exist. A frequent support action can still be a `persistent_companion`, and then its default visible state must stay low weight.

## Attention Budget

- High: may become the viewport focus when it is the current task.
- Medium: visible and easy to find, but secondary to the main content.
- Low: reachable and legible without pulling focus from the main task.
- Minimal: background or brief signal only.

When a full source component exceeds the selected attention budget, reuse its semantics rather than its full visual form: keep tokens, icon language, state meaning, title/progress semantics, and extend the nearest family with a compact/collapsed state. Do not draw an unrelated substitute just to make it smaller.

## Page Track Matrix

先确定页面所属任务，再读取 `screen-patterns.md` 匹配 profile 的 Surface Grammar 和 Extension Heuristics，不在此重复页面表。新功能不能因为“新”而借用更强的页面表达，例如设置项变成资讯卡、个人工具变成主内容模块。沉浸音频等未确认完整源屏的场景，只可使用已登记组件，不声称存在未核验的页面来源。

## Placement Rules

- Start with the closest source page and find the nearest existing group.
- Insert into the existing group when the feature shares the same task.
- Create a separate group only when the feature changes task type, such as account operations versus ordinary settings.
- Use group spacing larger than row spacing; read the actual tokens from the source sibling and `metadata/tokens.yaml > spacing`.
- Keep group-internal items visually connected by shared surface, auto layout, divider, or proximity.
- Do not make each new row an independent floating card when the source page groups rows.
- A low-frequency utility must not compete with the main page object.
- Risk/exit actions must be isolated from normal and account actions.

## Visual Weight Rules

- New features default to inherited typography, radius, fill, spacing, and icon size from the nearest sibling.
- If a feature needs an unavailable icon, follow `component-audit.md > Missing Icon Resolution`, which resolves the catalog fallback and registered candidate source; do not draw a temporary substitute.
- A `persistent_companion` must be quieter than the page primary content in its default state; stronger or full controls belong to a user-initiated expanded state.
- Default visible states must match the selected `attention_budget`; do not use a full component form when the role calls for a compact, collapsed, or inline state.

## Examples

### Settings: switch account

- Role: account operation.
- Track: settings.
- Placement: a separate account operation group between ordinary settings and logout, or a clearly separated row above logout.
- Component: `SettingsRow` pattern.
- Weight: medium-low. It is more important than ordinary preference rows, but less visually forceful than the isolated logout action.
- Failure mode: placing it as a primary full-width CTA or merging it with logout makes the action hierarchy unclear.

### Profile: skin and benefits center

- Role: low-frequency utility.
- Track: profile.
- Placement: weak entry or grouped subtle utility row below identity/profile content, not equal to the main content/history module.
- Component: profile secondary entry pattern or nearest row/cell family.
- Weight: low. It should be discoverable without taking over the page.
- Failure mode: giving each utility a large standalone card makes the page fragmented and reduces content density.

### Subscription modal

- Role: paid entry/subscription.
- Track: overlay/sheet over the current touchpoint.
- Placement: use modal only after a paid trigger; page-level paid entry remains weak.
- Component: `Plus Badge`, `App Button`, `Sheet & Picker / Type5` or source subscription modal.
- Weight: modal is focused once opened; paid entry inside Profile/Home is lower than primary content.
- Failure mode: turning a profile paid entry into a full-page paywall or using aggressive sales styling.

### Cold start age choice

- Role: primary setup task.
- Track: cold start.
- Placement: one age-choice module with four option rows and a primary continue button.
- Component: StarBaby/IP avatar, age option row pattern, `App Button`.
- Weight: one focused decision; no extra feature cards.
- Failure mode: adding a marketing hero, reward framing, or multiple competing setup modules.

## Pre-Design Questions

在通用设计判断之外，重点想清楚三个接入问题：

1. 新功能帮助当前主任务，还是应放入更弱的入口？
2. 源组件的完整形态是否超出注意力预算，需要同族紧凑或折叠状态？
3. 接入后会影响哪些相邻内容，影响是否在授权区域内，如何用截图证明？

## Delivery Notes

按所选 route profile 及 `validation.yaml > feature_insertion_check`、`presence_role_fit_check` 取必要字段，写入同一份任务证据。已记录的设计判断、组件来源和截图直接引用，不重复填写；`Pre-Design Questions` 只是思考提示，不是额外必填交付表。面向用户说明新增功能的位置、理由、结果与未解决问题即可。
