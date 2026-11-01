# External Reference Patterns

Use this file only when Shaonian Bowen has the core component family but lacks the exact local state, content pattern, or visual treatment needed for the task, or when the user provides reference screenshots or asks for mature-product references.

External references are pattern research, not a substitute design system. They can inform information hierarchy, affordance, placement, density, state expression, and edge-case handling. They must not replace Shaonian Bowen source components, variables, text styles, icon language, navigation, or brand feeling.

Evidence is explicit: use `pattern_memory_reference` when only this file, product names, or general product knowledge were used; use `visual_reference_checked` only after actually inspecting a user screenshot, live page, or future external-library image; use `none` when no reference was needed. Never claim a product's latest design was checked without visual evidence.

## When To Use

Use this reference flow when any of these is true:

- The required core component exists, but the requested state or variant does not exist yet. Example: `NewsCard` exists, but video duration overlay is missing.
- The user attaches screenshots as reference.
- The user asks for "参考成熟产品", "找类似例子", "提升美感", "不要瞎发挥", or similar wording.
- A new local pattern is needed for a product surface and existing Shaonian Bowen source screens do not answer the detail.

Do not use this flow when a required ready-to-force component is missing. Missing `NewsCard`, `TabBar`, `NavigationBar`, `StatusBar`, `LinkEntryCell`, `CommentCell`, button families, icons, core variables or effect styles must fail through the design-system gate. `BottomBar` is a componentization gap: preserve its source wrapper rather than pretending a Master exists. New or modified text uses the MCP default text engine.

## Source Priority

1. User-provided screenshots or annotated references.
2. Closest Shaonian Bowen source screen or component family.
3. Mature external product patterns from a diverse but task-relevant set.
4. General design memory only when current screenshots are unavailable; report that the reference is pattern-level, not live UI verification.

## Breadth Control

Use broad categories for discovery, then narrow aggressively before design:

- Select no more than 3 relevant products by default; expand only for an explicit research request.
- Cover only categories that directly fit the task.
- Extract 1-3 reusable patterns.
- Convert to 1-2 Shaonian Bowen-native variants.
- Do not combine unrelated visual details from every reference.

Too many references are harmful when they produce mixed navigation, mixed icon styles, mixed density, or multiple competing affordances. If the reference set starts pulling in different product mental models, stop and choose the closest product task model.

## Reference Categories

Choose by task semantics, not popularity.

| Category | Use for | Example products |
| --- | --- | --- |
| Video | play affordance, duration, cover overlays, immersive controls | YouTube, TikTok, Bilibili, Vimeo |
| Social / community | comments, reactions, follow, lightweight author signals | Instagram, Threads, X, Reddit |
| Image / lifestyle feed | cover-first cards, saved states, visual browsing | Instagram, Pinterest, Xiaohongshu |
| News / article | credibility signals, source/time, headline hierarchy | Apple News, Google News, The New York Times, Quartz |
| Education / learning | lesson progress, practice states, knowledge cards | Duolingo, Khan Academy, Coursera, Headway |
| Audio / podcast | playback states, duration, transcript, queue | Apple Podcasts, Spotify, Pocket Casts, Audible |
| Reading / knowledge | long-form reading, highlights, related entries | Kindle, Medium, Readwise, Notion |
| Kids / youth learning | friendly onboarding, low-pressure feedback | Khan Academy Kids, Epic, Duolingo ABC |

Avoid choosing only entertainment apps for Shaonian Bowen learning surfaces. A video or audio pattern may borrow affordance clarity from entertainment products, but the final result must remain credible, calm, and learning-oriented.

## Pattern Extraction Template

Before writing to Figma, record:

```yaml
external_reference_used:
  needed: true
  reason: <missing local state or user reference request>
  reference_evidence_level: <pattern_memory_reference | visual_reference_checked>
  reference_visual_sources: <screenshot id / Figma node / live page evidence, required only for visual_reference_checked>
  user_reference_screenshots: <list or none>
  categories_checked:
    - <category>
  products_checked:
    - <product>
  pattern_takeaways:
    - <placement / hierarchy / affordance / density rule>
  shaonian_bowen_translation:
    - <how it maps to existing components variables styles>
  not_copied:
    - <foreign chrome, icon style, color, density, or brand detail not copied>
```

If external reference is not needed, record `external_reference_used: none` and `reference_evidence_level: none`.

## Shaonian Bowen Translation Rules

- Keep the closest Shaonian Bowen component as the parent. Add only the smallest local state or variant needed.
- Use Shaonian Bowen variables, text styles, radius, spacing, and icon sizes.
- Preserve page track and feature role from `feature-insertion.md`.
- Preserve youth-news learning tone: credible, calm, readable, not entertainment-first.
- Keep one new concept per screen. If the reference introduces a new navigation model and a new content model, keep only the content state.
- For multiple variants, vary one meaningful design axis: affordance strength, placement, information hierarchy, or disclosure level.

## Common Local State Patterns

### Video cover state

Useful sources: YouTube for duration clarity, Instagram/TikTok for play affordance visibility, Apple News/Google News for editorial restraint.

Translate to Shaonian Bowen:

- Parent remains `NewsCard` or source cover component.
- Duration uses text-on-image token such as `Text 文本/T4 压图` and a quiet dark chip or overlay.
- Play icon uses existing `Icon16/Icon20/Icon24` style, not a foreign glyph.
- Overlay should not cover the article subject, title, metadata, tags, or card actions.
- Prefer bottom-right duration for low emphasis; use a small play affordance only when video recognition needs to be stronger.

### Audio or listen state

Useful sources: Apple Podcasts, Spotify, Pocket Casts, Headway.

Translate to Shaonian Bowen:

- Use existing audio controls and script/transcript components first.
- Keep learning context visible; do not make the page feel like a music player unless the task is immersive audio.
- Use progress and duration as supporting information, not as the primary visual object unless listening is the main task.

### Social discussion state

Useful sources: Threads, Reddit, Instagram comments, X replies.

Translate to Shaonian Bowen:

- Use `CommentCell`, reply hierarchy, and source discussion styles.
- Keep credibility and learning context stronger than vanity metrics.
- Reactions should be quiet support actions, not gamified reward UI.

### Education progress state

Useful sources: Duolingo, Khan Academy, Coursera, Headway.

Translate to Shaonian Bowen:

- Use progress to clarify learning continuation, not to create heavy game mechanics.
- Keep success/feedback friendly and low-pressure.
- Do not introduce badges, streaks, or reward-heavy framing unless the product requirement explicitly asks for it.

## Validation

Pass when the quality-tier rules and registered component-family gate in `metadata/validation.yaml` are satisfied. Draft tiers report target-region Token, Auto Layout, Dark Mode, and unregistered new componentization gaps in `production_gaps`; source-shell protection, registered component reuse, and universal basic visual QA remain active.

- The closest Shaonian Bowen component family remains visible and structurally intact.
- The external reference is summarized as a pattern, not copied as visual styling.
- The output uses Shaonian Bowen current-file tokens and styles.
- The screenshot still reads as Shaonian Bowen when foreign product labels are ignored.
- The design quality audit confirms hierarchy, readability, alignment, and youth-product fit.

Fail if:

- The output copies the visual identity of a single external product.
- External product navigation, tab style, icon style, color system, or entertainment chrome replaces Shaonian Bowen system language.
- Multiple product references create a mixed visual language.
- A missing ready-to-force component is justified by external reference.
