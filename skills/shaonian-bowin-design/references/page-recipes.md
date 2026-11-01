# Page Recipes

页面配方只负责生产装配、组件复用和 Auto Layout 结构。页面体验、视觉节奏和探索边界读取每节指向的 `screen-patterns.md` profile；没有匹配时根据 `design-decision-matrix.md` 判断并报告 `recipe_gap`。

## Shared Layout Rules

- Page frame defaults to `390x844`; main content column uses `20px` side padding and `350px` content width.
- Use independent cards only for independent browsing objects such as news stories, reading history items, or article segment cards.
- Use one larger container with dividers or internal spacing for related settings rows, profile utilities, filter sections, short action groups, and grouped controls.
- Same list, same gap. Repeated cards usually use `16px`; major page regions use `20px` or `24px`.
- If one viewport has more than four independent white cards, check fragmentation and merge related controls into a parent block.
- New setting rows, profile feature groups, tabs, filter rows, repeated lists, sheet stacks, and modal content stacks should be Auto Layout Frames.
- `Group` cannot be used as a new layout container. It is tolerated only inside source components or existing historical source nodes.
- BottomBar or action bars must not cover primary text, CTA, card footers, transcripts, comments, or protocol text; keep at least `16px` visible gap above fixed bottom controls.
- When content is too dense, remove weak metadata before shrinking primary text.

## Home Feed

Experience profile: `screen-patterns.md > profile_id: home_feed`.

production_recipe:

- Source, only when task explicitly targets Home Feed: `source-frames.yaml use_for=home_feed`; component `NewsCard`.
- Must use: `状态栏`, `Home Header Bar`, `News Card`, `Footer`, `Tab Bar`, and the source-matched bottom-navigation container.
- Navigation: follow `component-navigation.md`; preserve the locked source navigation context and use the correct `TabBar` state.
- Local layout: light mint background/top mask, list wrapper, scroll spacing.
- Auto Layout: card list vertical, gap `16`, main column `350`.

## Article Detail

Experience profiles: `screen-patterns.md > profile_id: article_detail`; article function layers additionally read `profile_id: article_learning_function`.

production_recipe:

- Source: `source-frames.yaml use_for=article_detail`; function sheets use `use_for=article_function_sheet`; no-comment state uses `use_for=article_detail_no_comments`.
- Must use: `Navigation Bar`, `Audio Player Bar`, `Impact Card`, `Function Tab`, `Comment Input Trigger`, `Comment Cell`, `Footer`.
- Navigation: follow `component-navigation.md` for detail header and safe area.
- Audio: follow `component-audio.md` for `Audio Player Bar` usage.
- Comments: follow `component-comments.md` for input, root/reply, and voice comment areas.
- Auto Layout: function grid, comment list, section stack.
- Article function sheets use overlay, white full-screen sheet from near the top, `20px` top radius, `Navigation Bar`, horizontal `Function Tab`, context row, and readable segment cards.

## Comment Area

Experience profile: inherit the containing page; article comments default to `profile_id: article_detail`.

production_recipe:

- Must use: `Section Title`, `Comment Input Trigger`, `Comment Cell`, `Voice Comment Cell` if voice.
- Component pattern: `component-comments.md`.
- Auto Layout: comment list vertical; root/reply spacing consistent.
- Lock article title, metadata, body, navigation, bottom bar, background, and unrelated modules unless explicitly targeted.

## Profile / Mine

Experience profile: `screen-patterns.md > profile_id: profile_mine`.

production_recipe:

- Source: `source-frames.yaml use_for=profile` for profile/mine states.
- Must use: `User Card`, `Article Preview Cell` or `Reading History Cell`, `Empty Placeholder`, `Plus Badge` when paid, `Tab Bar`, and the source-matched bottom-navigation container.
- Navigation: follow `component-navigation.md`; preserve the source bottom-navigation container and `TabBar` state.
- Auto Layout: related profile utilities share a vertical group; history and interaction lists retain the selected profile's state model.

## Settings

Experience profile: `screen-patterns.md > profile_id: settings`.

production_recipe:

- Source: resolve `source-frames.yaml use_for=settings` to the concrete settings `screen_frame`; state sheets use `use_for=settings_sheets`.
- Must use: `Navigation Bar`, `SettingsRow` instances, and `App Button` when action exists. Resolve the row variant from `components.yaml` and verify it live; local layout is limited to parent grouping, not replacing a registered row.
- Navigation: follow `component-navigation.md` for `Navigation Bar` and right/left controls.
- Bottom sheets: ordinary setting pickers use `component-overlays.md > Floating Sheet`.
- Auto Layout: settings group vertical, row horizontal, group gap larger than row gap.
- Visual check: no standalone feature card for low-frequency settings.
- Account operations use a separate group; risk/exit actions stay isolated from ordinary settings.

## Cold Start / Identity Or Age

Experience profile: `screen-patterns.md > profile_id: cold_start_identity`.

production_recipe:

- Source: `source-frames.yaml use_for=cold_start_identity_context` is the active identity-selection baseline. For age or interest steps, reuse its decision grammar and report a component/profile gap when no matching confirmed source state exists.
- Must use: StarBaby/IP asset, `App Button`, status bar.
- Bottom sheets: identity/age selection sheets use `component-overlays.md > Floating Sheet` unless the task explicitly asks for a full-screen onboarding redesign.
- Auto Layout: option list vertical, action pinned above weak skip/safe area.
- Option rows/cards follow the source quiet geometry: about `64px` height and `12px` vertical rhythm unless source updates prove otherwise.

## Subscription Modal

Experience profile: `screen-patterns.md > profile_id: commerce_and_feedback`.

production_recipe:

- Source: `source-registry.yaml use_for=subscription_modal` and `use_for=subscription_plan`; component family `components.SheetPicker`.
- Component pattern: `component-overlays.md > Paywall Half Sheet`.
- Must keep: overlay/mask,贴屏底部半屏 Paywall Sheet, Plus/IP identity, `App Button`, close `Icon Button`/source close, weak protocol/helper.
- Local layout: plan area, IP zone, renewal/privacy helper until componentized.
- Auto Layout: sheet vertical, plan selection area, helper/action stack.
