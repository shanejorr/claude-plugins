---
name: ui-style
description: "Shane's house UI style guide: editorial civic-warm aesthetic (Figtree sans display + Inter UI, warm burgundy/off-white palette, parent-friendly voice, small-caps metadata, hairline rules). Mirrors the Georgia Homeroom chatbot. User-invoked only; do not auto-apply."
disable-model-invocation: true
user-invocable: true
---

# UI Style Guide

My preferred visual style for web UIs. Apply these principles whenever you're designing or restyling a UI.

The aim is **editorial civic-warm**: the visual register of a modern, parent-facing civic publication. Trustworthy and legible without being stiff, warm without being bubbly. Think NYT Parenting, PBS Learning Media, modern family-facing government services done right. The opposite of bubbly SaaS pastel, heavy neumorphism, trendy glassmorphism, or stiff institutional gray.

The canonical implementation of this style is the **Georgia Homeroom standards chatbot** (`apps/standards-chatbot/frontend`). When two interpretations are defensible, prefer what that app does.

---

## Scope

This style applies to **editorial / civic / family-facing publishing web products** — apps where content is the product, the reader's trust matters, and readers may be skimming on a phone while doing something else. Parent guides, civic explainers, educational portals, research and reference tools, policy briefs, documentation.

It is **not** appropriate for games, consumer fitness apps, playful consumer brands, fintech that wants an approachable feel, or marketing sites for high-energy B2B SaaS. Those registers need different choices around saturation, typography, and density.

When in doubt: if the product wants to feel like a trustworthy family-facing publication or a serious civic tool, use this. If it wants to feel friendly-bubbly or high-energy, don't.

---

## Tech stack assumptions

Frontends using this guide assume this stack. Guidance references specific library/utility names.

- **Next.js (App Router) + React + TypeScript**, server components where possible.
- **Tailwind CSS v4** via `@tailwindcss/postcss`, plus the `@tailwindcss/typography` plugin. Tokens live in a CSS `@theme { … }` block in `globals.css` — **not** `tailwind.config.ts`. Utilities auto-generate from CSS variable names (`--color-brand-masthead` → `bg-brand-masthead`, `--text-h1` → `text-h1`, `--tracking-eyebrow` → `tracking-eyebrow`). Do not maintain a parallel `tailwind.config.ts` token table; the CSS block is the single source of truth.
- **react-markdown + remark-gfm** for rendering markdown; always wrap in `prose` classes customized per this guide.
- **isomorphic-dompurify** to sanitize any external HTML before `dangerouslySetInnerHTML`.
- **Playwright** for E2E including accessibility assertions.
- **Fonts** loaded via `next/font/google` with CSS variables (`--font-figtree`, `--font-inter`, `--font-jetbrains-mono`). Never use `<link>` tags for web fonts.

---

## Core principles

1. **Restraint over decoration.** Empty space, hairline rules, and typography do the work. No gradients as decoration, no fake depth, no drop shadows on text.
2. **Typography is the primary design element.** A warm humanist sans display face (Figtree) carries the brand. Body text is set carefully, not just "Inter at 16px."
3. **Muted, warm, matte.** Surfaces are warm off-white with a pink undertone, never pure `#fff`. Primary ink is never pure `#000` — always a tinted near-black.
4. **Content hierarchy is explicit.** Eyebrow → headline → deck → body. The reader never wonders what's important.
5. **Semantic color, not decorative color.** Each brand hue means something. Accent for interactive. Masthead for the brand. Gold for "featured / editorial" and active-streaming states. No rainbow pills.
6. **Plain-language, parent-facing voice.** Written for a real person reading on a phone between tasks. Warm, direct, specific. See **Voice and tone** below.
7. **Mobile is the main event.** Design the 375px layout first. Desktop is a wider version of the same idea, not a different product.

---

## Voice and tone

This guide assumes parent-facing, civic-educational copy. Voice and visual style are one system — the tone below is as much "the house style" as the palette.

### Register

- **Warm, concise, declarative.** A helpful experienced neighbor explaining something important, not a handbook, not a chatbot, not a brochure.
- **Second person singular.** "Your child." "You." Address one parent at a time.
- **Plain language, grade-school reading level.** Short sentences. Active voice. Concrete verbs.
- **No exclamation points. No emoji. No cutesy voice.** This is for adults who want straight answers.
- **No em-inflation.** "Important" beats "incredibly important." Avoid "unlock," "empower," "journey," "seamless," "delight," marketing cliches.

### Headlines

- **Sentence case, ending with a period.** Not title case, not a fragment.
- **An em-dash for a friendly aside reads warmer than a comma.** `Know what your child should be learning — and check that they are.`
- `text-balance` on display headlines and H1.

### Eyebrow labels (small-caps)

- **Descriptive, not promotional.** "A guide for Georgia parents." "What they should know." "Check their learning." "Help at home." Not "EMPOWERING FAMILIES" or "THE FUTURE OF EDUCATION."
- **Section eyebrows describe what the parent is trying to do.** "Ideas to get you started." "Three ways parents use this." "Subjects we cover."

### Microcopy

- **Explains, doesn't cheerlead.** "Pick your child's grade to get the right answers." "Tap one to ask." "Press Enter to send · Shift+Enter for a new line."
- **Status words stay short.** Single words work: `Connecting`, `Responding`, `Ready`.
- **Loading states name what's happening.** "Looking up what your child's grade is learning…" — not just "Loading…".
- **Error messages apologize briefly and offer a next step.** "We couldn't connect right now. Please try again in a moment." "Something didn't work. Please try again." Never blame the user.
- **Separator of choice is the middle dot** (`·`). Use for bilingual indicators (`English · Español`), keyboard hints, metadata lines. Never slashes, never parentheses.

### Long-form replies (chatbot / prose)

Copy rendered inside prose blocks follows the same register, plus:

- **Direct answer first, in one or two sentences.** Lead with what the reader needs to hear.
- **Cite specific, verifiable references** (standard codes, law sections, dataset IDs) verbatim — never invent, never compress a range with a dash.
- **Define jargon inline.** If you must use a term of art, define it in the same sentence.
- **End with one concrete, at-home/next-step suggestion** when the topic admits it.
- **Language mirroring.** Respond in the language the reader wrote in. For mixed English/Spanish, follow the dominant language of the latest message. Don't translate proper nouns, code identifiers, or official citations.

---

## Typography

### Typefaces

- **Display / headings: a humanist sans with personality.** **Figtree** is the house choice — round-ish geometric with humanist warmth, reads well from small metadata to large headlines. Acceptable alternatives: DM Sans, Inter Display, Plus Jakarta Sans. **Do not use a serif display face in this house style** — Fraunces, Crimson, Newsreader, Instrument Serif all fight the parent-facing warmth Figtree establishes.
- **UI / body: a neutral humanist sans.** **Inter** is the default. Acceptable fallbacks: Geist, IBM Plex Sans, system-ui. Avoid rigidly geometric sans (Futura, Poppins) — they feel too branded.
- **Numerics, IDs, dates, code: a mono.** **JetBrains Mono** is the house choice. Acceptable: Geist Mono, IBM Plex Mono. Use mono for anything tabular or data-flavored — grade codes, dates, counts, IDs, standards like `5.NR.1.2`.

Loaded in `layout.tsx`:

```tsx
import { Figtree, Inter, JetBrains_Mono } from "next/font/google";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });
const figtree = Figtree({ variable: "--font-figtree", subsets: ["latin"] });
const jetbrainsMono = JetBrains_Mono({ variable: "--font-jetbrains-mono", subsets: ["latin"] });

<html className={`${inter.variable} ${figtree.variable} ${jetbrainsMono.variable} h-full antialiased`}>
```

Mapped in `globals.css` `@theme`:

```css
--font-sans: var(--font-inter), ui-sans-serif, system-ui, sans-serif;
--font-display: var(--font-figtree), ui-sans-serif, system-ui, sans-serif;
--font-mono: var(--font-jetbrains-mono), ui-monospace, SFMono-Regular, monospace;
```

And exposed as a utility class (Tailwind v4 auto-generates `font-display` from the token, but an explicit rule keeps it robust across plugin updates):

```css
.font-display { font-family: var(--font-display); }
```

### Type scale

Sizes scaled with `clamp()` so they resize without breakpoints. Register in `@theme` so `text-display`, `text-h1`, `text-meta`, etc. become utilities.

| Role      | Approx size                            | Line-height | Usage |
|-----------|----------------------------------------|-------------|-------|
| Display   | `clamp(2.5rem, 5vw, 4.5rem)`           | ~1.05       | Landing hero headlines |
| H1        | `clamp(2rem, 3.5vw, 3rem)`             | ~1.1        | Detail-page titles |
| H2        | `clamp(1.5rem, 2.2vw, 2rem)`           | ~1.2        | Section headings |
| H3        | `1.25rem`                              | ~1.3        | Card titles, subsections |
| Deck      | `clamp(1.125rem, 1.6vw, 1.375rem)`     | ~1.45       | Hero decks, subtitles |
| Body      | `1rem`                                 | ~1.7        | Long-form prose |
| Small     | `0.875rem`                             | ~1.55       | Captions, footnotes |
| Meta      | `0.75rem`                              | ~1.4        | Eyebrows, timestamps — always `uppercase` with `tracking-smallcaps` or `tracking-eyebrow` |

Tracking tokens:

```css
--tracking-eyebrow:   0.18em;
--tracking-smallcaps: 0.12em;
```

### Typography rules

- **Every headline and deck uses `font-display` (Figtree).** This is the single most important type choice — it's what makes the surface feel warm rather than corporate. Display, H1, H2, H3, decks, card titles, prose `h1-h6`.
- **UI chrome (buttons, inputs, labels, nav, metadata, small-caps) uses `font-sans` (Inter).** Inter is the default body font; `font-sans` applies automatically.
- **Body copy uses `font-sans` (Inter).** Not Figtree — Figtree is for display only. Long-running paragraphs belong in Inter.
- **User-typed content** (chat messages, quoted user input) renders in `font-display` with `text-body leading-relaxed` — lets the parent's own words carry a little more warmth than generic UI text.
- **Blockquotes** use `font-display italic` with a 4px `border-l-brand-gold`. No bg tint.
- Body line-height is generous (~1.7). Tight line-height (`leading-[1.05]`, `leading-snug`) is only for display type.
- Tracking is `tracking-tight` on display, normal on body, `tracking-smallcaps` or `tracking-eyebrow` on small-caps.
- `text-balance` on display headlines and detail-page H1s — prevents orphaned last words.
- **Never use drop shadow on text.** Type stands on its own.

---

## Color

### Palette shape (per project / app)

Every UI has exactly this token set. Names are semantic, not descriptive. Don't invent `burgundy-2` — extend this vocabulary instead.

```
# Brand
masthead          # Masthead brand color — header, footer, slide-over nav
masthead-fg       # Text/icon on masthead — a warm near-white

# Interactive
accent            # Interactive — links, buttons, active tabs, streaming indicators
accent-strong     # Hover/active state — one stop darker than accent

# Surfaces
surface           # Page background — warm off-white (NOT pure white)
raised            # Card background — pure white or half-step from surface
muted             # Subtle tint for highlighted / featured content, chip bg
scrim             # Full-viewport overlay — near-black at ~40% alpha

# Text (ink)
ink               # Body text — near-black with a hint of the brand hue
ink-muted         # Secondary text — metadata, captions
ink-subtle        # Tertiary text — timestamps, hints, placeholder

# Structure
border            # Default hairline — warm-tinted, low-contrast
border-strong     # Emphasized hairlines (under mastheads, under input underlines)

# Editorial accent
gold              # Optional editorial accent — blockquote rules, active-streaming dot, featured marks

# Semantic state (never saturated)
success           # Muted forest green
warning           # Muted amber
danger            # Muted red (never stoplight-red)
```

**Naming note.** `masthead` is the brand color — the paper's nameplate. It is *not* the "primary button" color. Primary CTAs use `accent`. Keep the token name aligned to editorial semantics; button variants speak in product-UI language ("primary button = accent color").

**Multi-app projects.** If several apps share code but need to feel related-but-distinct, **shift the hue family per app, keep the token shape identical.** A shared component writes `bg-brand-masthead`; each app resolves it to its own hue. No per-app component variants.

### Palette values — Georgia Homeroom reference

Declared in `globals.css` `@theme`:

```css
/* Brand — masthead is the paper's nameplate color (deep burgundy) */
--color-brand-masthead:        #7a2d3b;
--color-brand-masthead-fg:     #faf2ed;

/* Interactive — mid-saturation berry red */
--color-brand-accent:          #a8344a;
--color-brand-accent-strong:   #7f2434;

/* Surfaces — warm off-white with a pink undertone */
--color-brand-surface:         #fbf3ef;
--color-brand-raised:          #ffffff;
--color-brand-muted:           #f4e3df;
--color-brand-scrim:           rgb(15 23 42 / 0.4);

/* Ink — near-black carries any hue */
--color-brand-ink:             #111827;
--color-brand-ink-muted:       #475569;
--color-brand-ink-subtle:      #64748b;

/* Structure — warm-pink hairlines */
--color-brand-border:          #ecd6d0;
--color-brand-border-strong:   #d7b9b2;

/* Editorial accent */
--color-brand-gold:            #a67c2e;

/* Semantic state */
--color-brand-success:         #166534;
--color-brand-warning:         #92400e;
--color-brand-danger:          #b91c1c;
```

### Palette values (guidance for a new app)

- **`masthead` is deep, warm, and slightly desaturated.** Burgundy with warmth mixed in — not a corporate navy. Same principle for green, teal, or indigo variants: warm them up.
- **`accent` is mid-saturation.** Reads as the brand color at a glance, but doesn't scream. One stop brighter than the masthead is a safe default.
- **`surface` is never `#ffffff`.** Always a warm off-white with a hint of the brand hue. Pink-warm: `#FBF3EF`, `#FAF2ED`, `#FAF7F2`. If shifting to a green or blue family, tint the surface with that hue too.
- **`ink` is never `#000`.** Near-black with hue: `#111827`, `#0F172A`.
- **`ink-muted`** ≈ slate-600 (`#475569`); **`ink-subtle`** ≈ slate-500 (`#64748B`).
- **`border`** is warm and low-contrast, one step from surface: `#ECD6D0`-ish. Hairlines should be felt, not seen.
- **`gold`** is muted editorial brass: `#A67C2E` territory. Use sparingly — blockquote rules, the streaming-status dot, rare feature marks.
- **`success` / `warning` / `danger`** stay muted and readable on `surface`. Good ranges: success `#166534`, warning `#92400E`, danger `#B91C1C`. For alert backgrounds: `bg-red-50` / `bg-amber-50` / `bg-green-50`.
- **`scrim`** is near-black at 40% alpha — declare it as a full rgb() value, not a runtime color-mix.
- **Focus ring** is `accent` at ~45% alpha using `color-mix(in srgb, var(--color-brand-accent) 45%, transparent)`. See **Micro-interactions**.

### Contrast

- **Body text on surface:** AA (4.5:1) minimum. `ink-muted` on warm off-white typically lands well above AA.
- **Accent on surface for links:** AA (4.5:1) minimum. **Always underline links in prose** (see Prose section) so color alone never carries the signal.
- **Masthead-fg on masthead:** 7:1+. Aim for a warm near-white.
- **Danger / warning / success** text colors on their pastel bg tints: verify AA per pair.

### What to avoid

- Saturated consumer colors (electric blue, neon green, hot pink).
- Multi-color gradients as brand identity.
- Full-color pill-tag swarms in different colors. Tags are small-caps text.
- Pure `#000` and pure `#fff`. Harsh on the warm palette.
- Status colors from the default Tailwind palette at 500+ saturation. Use the muted ranges above.
- Cool-grays on warm-pink surfaces — borders and muted tones need to stay in the warm family or the whole page fights itself.

---

## Elevation (shadow) scale

Four levels, no more.

```
elevation-0  none                 # Default — flat surfaces, hairline-defined
elevation-1  shadow-sm            # Cards at rest, inputs
elevation-2  shadow-md            # Cards on hover, dropdowns, popovers
elevation-3  shadow-xl            # Modals, slide-over panel, toasts
```

**Never use `shadow-2xl` or `drop-shadow-*`.** If something needs to appear "important," use color or a hairline rule.

---

## Radius scale

```
--radius-sm:    0.5rem   /* Small buttons, inline chips (rare) */
--radius-md:    0.75rem  /* Inputs, small cards */
--radius-card:  1.5rem   /* Standard cards, dialogs, modals */
rounded-full             /* Pill buttons, filter chips */
```

Declared in `@theme` so `rounded-card`, `rounded-md`, `rounded-sm` all work. Don't invent radii between these values.

---

## Spacing and z-index

**Spacing.** Tailwind's default 4px-based scale. Prefer the rhythm 4/8/12/16/24/32/48/64/96. Hero sections get `pt-12 pb-16` minimum. Cards use `p-6`. Section gaps ≥ 24px (`mb-6`).

**Z-index scale** — declare in `@theme`:

```css
--z-sticky:   30;   /* Sticky sub-nav, sticky cards */
--z-header:   40;   /* Main sticky header */
--z-dropdown: 45;   /* Dropdowns, popovers */
--z-overlay:  50;   /* Modals, slide-over, scrim */
--z-toast:    60;   /* Toasts above everything */
```

Never hand-pick `z-[999]`.

---

## Layout

### Surfaces and containers

- **Outer container** for page chrome is `mx-auto w-full max-w-6xl px-5 sm:px-8 lg:px-12`. Reading-focused content narrows to `mx-auto max-w-3xl` inside it.
- **Max-width is constrained.** Body text at `max-w-3xl` (~48rem). Grid layouts at `max-w-6xl`. Avoid full-width body text — unreadable over 80 characters.
- **Generous padding.** `py-12 sm:py-16` for heroes and sections.
- **Hairlines, not heavy borders.** 1px for `border`. 4px only for editorial accent rules (e.g., blockquote rule, feature cards).
- **No heavy drop shadows on containers.** `shadow-sm` at rest, `shadow-md` on hover. Anything heavier is a bug.
- **Corners:** rounded but not excessive. Cards at `rounded-card`. Inputs at `rounded-md`. Chips/badges fully rounded (pill).

### Editorial "information strip" pattern

A horizontal rule-bounded band for one or two interactive controls sitting between hero sections, reading like a form field set into a magazine page:

```tsx
<div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-3 border-y border-brand-border py-4">
  <span className="text-meta uppercase tracking-smallcaps text-brand-ink-subtle">
    Pick your child's grade to get the right answers
  </span>
  <GradeSelector ... />
</div>
```

Use this in place of a boxed form field on landing pages.

### Cards

Magazine article cards, not app tiles.

- `bg-brand-raised`, `border border-brand-border`, `rounded-card`, `p-6`, `shadow-sm`.
- On hover: `shadow-md` + `translate-y-[-2px]`. Subtle, not bouncy.
- **Featured / highlighted state:** `bg-brand-muted` + `border-l-4 border-brand-gold`. Don't use a full gold fill.
- **Suggestion-card variant** (clickable prompt tiles, no surrounding card chrome): eyebrow + Figtree headline + small-caps CTA with arrow, unbounded (no border, no padding box). See `ChatContainer.tsx` `SUGGESTIONS`.

### Grids

- `gap-x-8 gap-y-10` for card grids — columns breathe, rows breathe more vertically.
- 1 column on mobile, 2 at `sm:` or `md:`, rarely 3+. The chatbot uses `grid gap-x-8 gap-y-8 sm:grid-cols-2`.

### Rules and dividers

- Use `border-top` / `border-bottom` hairlines as section separators instead of `<hr>` or filled boxes.
- `divide-y divide-brand-border` is the go-to pattern for vertical lists (messages, definition lists, feature rows). Each row gets `py-4 first:pt-0`.
- **Filled gray info boxes are a smell.** Replace `bg-gray-100 rounded-lg p-6` with an eyebrow + prose block + hairline rule. Let the type carry it.

---

## Hero pattern

The canonical section pattern:

1. **Eyebrow** (meta, uppercase, `tracking-eyebrow`): a short descriptive label in `text-brand-accent`, `font-medium`. `A GUIDE FOR GEORGIA PARENTS`. `WHAT THEY SHOULD KNOW`.
2. **Headline** (`font-display` at `text-h1` or larger): one line, `text-balance`, `tracking-tight`. Sentence case with a period.
3. **Deck** (`font-display text-deck`, `text-brand-ink-muted`): one or two sentences that explain the headline without repeating it.
4. **Optional affordance:** information strip (see above), grade selector, or primary CTA.

Reference:

```tsx
<section className="mx-auto max-w-3xl">
  <p className="text-meta font-medium uppercase tracking-eyebrow text-brand-accent">
    A Guide for Georgia Parents
  </p>
  <h1 className="mt-4 text-balance font-display text-h1 leading-[1.05] tracking-tight text-brand-ink">
    Know what your child should be learning — and check that they are.
  </h1>
  <p className="mt-5 max-w-2xl font-display text-deck text-brand-ink-muted">
    See exactly what Georgia expects kids to learn in each grade…
  </p>
</section>
```

---

## Masthead (header)

Sticky at the top, minimal, uses the brand color as background.

- `sticky top-0 z-40 border-b border-brand-border-strong bg-brand-masthead text-brand-masthead-fg`.
- **Wordmark** is `font-display` at `text-xl sm:text-2xl`, `tracking-tight`. Clickable — serves as home / new-conversation. Single-line; **no** small-caps kicker beneath (keep the masthead uncluttered).
- **Right side: live status block.** Small-caps language indicator (`English · Español`), then a colored-dot + status word, with `aria-live="polite"`.
- Status-dot colors:
  - `Connecting` → `bg-brand-masthead-fg/40` (faded)
  - `Responding` → `bg-brand-gold` (active / working)
  - `Ready` → `bg-brand-masthead-fg` (full)

```tsx
<header className="sticky top-0 z-40 border-b border-brand-border-strong bg-brand-masthead text-brand-masthead-fg">
  <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-5 py-4 sm:px-8 sm:py-5">
    <button type="button" onClick={onHomeClick}
      className="font-display text-xl tracking-tight transition-colors hover:text-brand-gold focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-gold focus-visible:ring-offset-2 focus-visible:ring-offset-brand-masthead sm:text-2xl">
      Georgia Homeroom
    </button>
    <div className="flex items-center gap-3 text-meta uppercase tracking-smallcaps text-brand-masthead-fg/80">
      <span className="hidden sm:inline">English · Español</span>
      <span className="inline-flex items-center gap-1.5" aria-live="polite">
        <span className="h-1.5 w-1.5 rounded-full bg-brand-gold" aria-hidden="true" />
        {status}
      </span>
    </div>
  </div>
</header>
```

---

## Tables

Civic/editorial products lean on tables. Style:

- **No card wrapper.** Tables sit directly on `surface`.
- **Header row:** small-caps labels in `text-meta uppercase tracking-smallcaps text-brand-ink-subtle`, `pb-2`, hairline below (`border-b-2 border-brand-border-strong`).
- **Body rows:** hairline between (`border-b border-brand-border`), cell padding `py-2 pr-4`.
- **No zebra striping.** Hairlines do the work.
- **Numeric / date / code columns:** right-aligned or mono-aligned, `font-mono`.
- **Hover state on clickable rows:** `hover:bg-brand-muted transition-colors`.
- **Sort indicators:** small chevrons in `text-brand-ink-subtle`, `text-brand-accent` when active.
- **Empty-state row:** single row spanning all columns, italic text in `text-brand-ink-muted`.
- **Pagination:** below the table, small-caps page indicator + pill-shaped prev/next buttons.

Markdown-rendered tables use the same styling through a `ReactMarkdown` components override — see `MarkdownRenderer.tsx`.

---

## Modals and dialogs

Three flavors. All share: scrim behind, `elevation-3`, focus trap, Escape-to-close, return focus to trigger on close, body scroll locked.

### Dialog
Centered, `max-w-md`, `bg-brand-raised`, `rounded-card`, `p-6`. Close button (`×`) top-right in `text-brand-ink-subtle`. Primary (`accent`) + secondary (`raised` + `border`) buttons at bottom, right-aligned. On mobile, pins to center with `p-4` page padding.

### Sheet
Mobile: slides from bottom, full width, `rounded-t-card`. Desktop: same as dialog.

### Slide-over
From right, `w-full max-w-sm`, full height, `bg-brand-masthead text-brand-masthead-fg`. The canonical mobile-nav pattern. Nav items `font-display text-2xl`, hairlines between (`border-b border-brand-masthead-fg/15`).

**Focus trap:** use `focus-trap-react` or equivalent. Never hand-roll focus trap logic.

---

## Empty states

1. Outline icon (48px), centered, `text-brand-ink-subtle`
2. `font-display text-h3` heading, `text-brand-ink`
3. One-sentence explanation in `text-small text-brand-ink-muted`
4. Optional list of concrete examples, `text-small italic text-brand-ink-muted`
5. Optional primary CTA, pill-shaped, `bg-brand-accent`

Don't use illustrations (too brand-dependent) or pure-text empty states.

---

## Toasts and inline alerts

Muted semantic tint + hairline border pattern. Never stoplight-saturated colors.

### Inline alerts (form-level or page-level notices)
Rectangular, `rounded-card`, hairline border, pastel bg tint, icon left, text `text-small`.

```
Error:    bg-red-50 border-red-200 text-red-700
Warning:  bg-amber-50 border-amber-200 text-amber-700
Success:  bg-green-50 border-green-200 text-green-700
Info:     bg-brand-muted border-brand-border text-brand-ink
```

Reference (from the chatbot landing):
```tsx
<div className="mx-auto mt-8 max-w-3xl rounded-card border border-red-200 bg-red-50 px-4 py-3 text-small text-red-700">
  We couldn't connect right now. Please try again in a moment.
</div>
```

### Toasts (transient notifications)
- Bottom-right on desktop, top-center on mobile.
- Same tint + hairline pattern as inline alerts, plus `shadow-xl` (`elevation-3`).
- Auto-dismiss at 5s; always manually dismissible (× button).
- Stack vertically; max 3 visible. `z-toast` (60).

---

## Form elements

### Input styles

- **Editorial / chat inputs: underline style.** `border-b-2 border-brand-border-strong`, `bg-transparent`, `px-0 py-3`, resize-none textarea. On focus, `border-brand-accent`. Because the textarea itself uses `outline-none`, `focus-within:` on the wrapper carries the state.
- **Product-chrome / modal inputs: boxed style.** `bg-brand-raised`, `border border-brand-border`, `rounded-md`. Focus: `border-brand-accent` + `ring-1 ring-brand-accent/30`.
- **Select (inline).** Prefer the underline style with a chevron SVG pinned at right (see `GradeSelector.tsx`). `appearance-none border-0 border-b border-brand-border`.
- **Placeholders stay sans.** `text-brand-ink-subtle`, not italic.

### Buttons

- **Primary:** pill (`rounded-full`), `bg-brand-accent text-white`, hover `bg-brand-accent-strong`, `px-5 py-2 text-sm font-medium`. Disabled: `disabled:cursor-not-allowed disabled:opacity-40`.
- **Secondary:** pill, `bg-brand-raised text-brand-ink border border-brand-border`, hover `bg-brand-muted`.
- **Destructive:** `bg-brand-danger text-white`, hover one stop darker. Only for irreversible actions.
- **Ghost / text:** `text-brand-accent hover:text-brand-accent-strong`, no bg, no border. Good for footer links ("Start a new conversation").
- **Never gradient backgrounds.** No purple/pink SaaS CTAs.

### Form validation

- **Error input:** `border-red-500 focus:ring-red-500/30`.
- **Error message below input:** `text-sm text-red-600 mt-1.5`, with an optional icon.
- **Error state must include a non-color cue** — text or icon, never color alone (SC 1.4.1).
- Field-level success states are rarely needed; the absence of error is the signal.
- **Multi-field / auth errors** use an inline alert above the form.

---

## Chips and filters

The "no rainbow pills" anti-pattern applies to **passive metadata tags**. Single-tone chips for *interactive choices* are legitimate.

### Suggestion / grade chips (clickable choices)
`bg-brand-muted text-brand-ink-muted hover:bg-brand-border hover:text-brand-ink rounded-full px-3 py-1.5 text-sm`. Use for: grade pickers, starter prompts, quick actions. No icons inside.

Reference (from `GradeChips.tsx`):
```tsx
<button
  className="rounded-full bg-brand-muted px-3 py-1.5 text-sm text-brand-ink-muted hover:bg-brand-border hover:text-brand-ink disabled:opacity-50"
>
  {opt.label}
</button>
```

### Filter chips (active filter state)
Same base, with `text-brand-accent` and optional `×` to remove.

### Tag display in cards / article meta
Keep as **small-caps text, not pills.** Passive metadata isn't interactive.

**Rule:** chips for *interactive choices*, text for *passive metadata*.

---

## Loading states

### Spinner — for brief blocking loads (<3s expected)
Centered, `animate-spin`, `border-4 border-brand-accent border-t-transparent rounded-full h-8 w-8`, optional label below in `text-small text-brand-ink-muted`.

### Skeleton — for longer waits where layout is known
`bg-brand-border/30 animate-pulse`, shape matches incoming content. Only skeleton meaningful content.

### Progress bar — for multi-step or known-duration work
Thin bar (`h-1`), `bg-brand-accent`, positioned at top of page or within a container.

### Streaming typing-dots (chat/LLM)

Three small dots bouncing with staggered delays, paired with a concrete explanation sentence. Never plain "Loading…" — name what's happening.

```tsx
<div className="flex items-center gap-3 text-small italic text-brand-ink-muted">
  <span className="flex gap-1.5" aria-hidden="true">
    <span className="h-1.5 w-1.5 rounded-full bg-brand-accent/60 animate-bounce [animation-delay:0ms]" />
    <span className="h-1.5 w-1.5 rounded-full bg-brand-accent/60 animate-bounce [animation-delay:150ms]" />
    <span className="h-1.5 w-1.5 rounded-full bg-brand-accent/60 animate-bounce [animation-delay:300ms]" />
  </span>
  <span>Looking up what your child's grade is learning…</span>
</div>
```

---

## Prose and long-form content

Use `@tailwindcss/typography`'s `prose` class as the base. In this house, **headings stay sans** (`font-display`) — not serif.

Canonical pattern (see `MarkdownRenderer.tsx`):

```
prose prose-base max-w-none
  prose-headings:font-display prose-headings:tracking-tight prose-headings:text-brand-ink
  prose-h1:text-h2 prose-h2:text-h3 prose-h3:text-base prose-h3:font-medium
  prose-p:text-brand-ink prose-p:leading-relaxed
  prose-strong:text-brand-ink prose-strong:font-medium
  prose-em:text-brand-ink
  prose-a:text-brand-accent prose-a:underline
    prose-a:decoration-brand-accent/40 prose-a:underline-offset-4
  hover:prose-a:text-brand-accent-strong hover:prose-a:decoration-brand-accent-strong
  prose-li:text-brand-ink prose-li:my-1
  prose-ul:my-4 prose-ol:my-4
  prose-blockquote:border-l-4 prose-blockquote:border-brand-gold
    prose-blockquote:font-display prose-blockquote:italic
    prose-blockquote:text-brand-ink-muted prose-blockquote:bg-transparent
    prose-blockquote:pl-5
  prose-code:font-mono prose-code:text-[0.92em] prose-code:text-brand-accent-strong
    prose-code:bg-brand-muted prose-code:rounded prose-code:px-1 prose-code:py-0.5
    prose-code:before:content-[''] prose-code:after:content-['']
  prose-pre:font-mono prose-pre:text-small prose-pre:bg-brand-muted prose-pre:text-brand-ink
    prose-pre:border prose-pre:border-brand-border prose-pre:rounded-md
  prose-hr:border-brand-border
```

- **Sans body** (Inter) for long-form content — this is a warm publication, not a novel.
- Line height ~1.7, max-width ~65ch (`prose` default; don't override unless intentional).
- **Downshift heading sizes within prose one step** (`prose-h1:text-h2 prose-h2:text-h3`) — the document's outer H1 carries the page, prose headings are structural subheads, not restatements of the page title.
- **Links always underlined.** Use `decoration-brand-accent/40` and `underline-offset-4` for a refined editorial feel.
- **Block quotes** use `border-l-4 border-brand-gold`, `font-display italic`, no bg tint.
- **Inline code** is `font-mono` with `bg-brand-muted` + `text-brand-accent-strong`, small-padding rounded pill. Strip default `prose` backticks via `before:content-['']` / `after:content-['']`.
- **Tables** get a `components` override in `ReactMarkdown` for small-caps `th` and hairline `td` — no card wrapper.
- **Emphasis with italics** for conversational stress. Bold for terms-of-art and key phrases the parent should notice.

### Rendering markdown

```tsx
<div className="prose prose-base ...">
  <ReactMarkdown remarkPlugins={[remarkGfm]} components={{ table, thead, th, td }}>
    {content}
  </ReactMarkdown>
</div>
```

### Rendering external HTML

**Always sanitize first:**

```tsx
import DOMPurify from "isomorphic-dompurify";

<div
  className="prose prose-base ..."
  dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(external.html) }}
/>
```

Never inject external HTML without `DOMPurify.sanitize()`.

---

## Navigation

### Desktop header
See **Masthead** above. Nav links (when present): **underline-on-active** (2px underline in `masthead-fg`), not filled pills.

### Mobile header
Same colors. Height shrinks to ~56px. Drops the right-side language indicator if space is tight, but keeps the live status pill. Single hamburger on the right when there's more than home + status. **No** horizontally-scrolling tab strip.

### Mobile menu (slide-over)
- **Slide-over from the right**, not full-screen overlay.
- Panel: `bg-brand-masthead text-brand-masthead-fg`, `w-full max-w-sm`.
- Scrim: `bg-brand-scrim`, click-to-close.
- Nav links: `font-display text-2xl`, one per line, hairlines between.
- Body scroll locked while open. Escape closes. Route change closes. Focus trapped.

### Sticky input dock (chat / comment / compose pages)

A canonical pattern for apps centered on an input:

```tsx
<div className="sticky bottom-0 border-t border-brand-border bg-brand-surface">
  <div className="mx-auto w-full max-w-3xl px-5 py-4 sm:px-8 sm:py-5">
    <ChatInput onSend={handleSend} disabled={disabled} />
    <div className="mt-3 flex flex-wrap items-center justify-between gap-x-4 gap-y-1 text-meta uppercase tracking-smallcaps text-brand-ink-subtle">
      <span>Press Enter to send · Shift+Enter for a new line</span>
      <button className="font-medium tracking-smallcaps text-brand-accent hover:text-brand-accent-strong">
        Start a new conversation
      </button>
    </div>
  </div>
</div>
```

Page content above reserves space with `pb-44 sm:pb-32` so content scrolls clear of the dock.

### Footer
- `bg-brand-masthead text-brand-masthead-fg`.
- **Top rule in `gold` at 4px** — an editorial signature.
- Three columns on desktop (brand / related / contact), two or one on mobile.
- Wordmark in `font-display`, labels in small-caps, "Powered by X" line in mono.

---

## Micro-interactions

- **Transitions are under 250ms.** Fast, confident. Not bouncy.
- **Hover effects are subtle:** color shift, 2px translate-up, shadow increment. Never scale up, never rotate.
- **Focus style is a warm 2px outline**, not a Tailwind `ring`:

```css
:where(a, button, input, textarea, select, [tabindex]):focus-visible {
  outline: 2px solid color-mix(in srgb, var(--color-brand-accent) 45%, transparent);
  outline-offset: 2px;
  border-radius: 2px;
}
```

- **`.fade-up` — house entrance animation.** Use on cards, messages, staggered grid items. 320ms cubic-bezier, 6px rise, opacity 0→1.

```css
.fade-up { animation: fade-up 0.32s cubic-bezier(0.22, 1, 0.36, 1) both; }
@keyframes fade-up {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .fade-up { animation: none; }
}
```

Stagger with inline style: `style={{ animationDelay: \`${i * 40}ms\` }}`.

- **Selection color** uses the accent at 22% alpha:
```css
::selection {
  background: color-mix(in srgb, var(--color-brand-accent) 22%, transparent);
  color: var(--color-brand-ink);
}
```

- **Respect `prefers-reduced-motion`.** Animations collapse to short opacity fades or disappear.

---

## Iconography

- Single-stroke outline icons — Lucide (preferred), Heroicons outline, Feather.
- Icons inherit color from parent (`currentColor`). No multicolor icons.
- Icons are supporting, not decorative. Don't add an icon to every heading.
- For directional cues (CTA arrows, chevrons), inline a small SVG rather than importing an icon library when the icon appears once — keeps bundles slim.

---

## Accessibility baseline

- **AA contrast** for body text, small text, and interactive elements. Verify `ink-muted` on `surface`, `accent` on `surface`, and `masthead-fg` on `masthead`.
- **Touch targets ≥ 44×44px** on mobile. Pad hit area if the visible affordance is smaller.
- **Every interactive element has a visible focus state.** Use the warm 2px outline above.
- **Icon-only buttons require `aria-label`.** Decorative icons adjacent to text should be `aria-hidden="true"`.
- **Focus trap** on modals, dialogs, and slide-overs. Return focus to trigger on close.
- **Skip links.** Every page has a `<a href="#main" className="sr-only focus:not-sr-only ...">Skip to content</a>` as the first focusable element.
- **`text-balance`** on display headlines.
- **Respect `prefers-reduced-motion`.**
- **Links in prose are always underlined.** Color alone isn't sufficient (SC 1.4.1).
- **Form errors** combine a color cue with a text message or icon — never color-only.
- **Live status indicators** (connection, streaming) get `aria-live="polite"`.
- **Bilingual UI** — set the primary `lang` on `<html>`, swap `lang` per element when rendering the other language so screen readers choose the right voice.

---

## Testing with Playwright

- **`@axe-core/playwright`** runs per route for AA contrast, missing labels, keyboard traps, heading order.
- **Visual regression** snapshots on canonical components: masthead, hero, suggestion card grid, message bubble (user + assistant + streaming), mobile input dock.
- **Route smoke tests** confirming each route returns 200 and doesn't throw hydration errors.
- **Keyboard-only navigation test** for each page's primary flow.

```ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("home page is AA accessible", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
  expect(results.violations).toEqual([]);
});
```

---

## Anti-patterns

If the UI starts doing any of these, stop and reconsider:

- **Serif display faces.** This is a sans-display house. Don't reach for Fraunces, Crimson, Newsreader, or Instrument Serif — they fight Figtree's warmth.
- **Filled gray boxes** (`bg-gray-100 rounded-lg p-6`) as "info panels." Replace with eyebrow + prose + hairline rule.
- **Rainbow pill tags.** Tags are small-caps text. Single-tone chips for interactive choices are fine.
- **Pure `#fff` surfaces with `#000` text.** Too harsh for the warm palette.
- **Cool-gray borders on a warm-pink surface.** Borders stay in the warm family.
- **Geometric sans everywhere** (Futura, Poppins). Fights Figtree.
- **Cutesy voice, exclamation points, emoji.** "Let's go!" and "You've got this!" are out of register. Kid-voice on a parent-facing surface is worse.
- **Marketing puffery.** "Unlock." "Empower." "Journey." "Seamless." "Delight." Delete.
- **"Playful" curves and blobs.** Not our register.
- **Purple/pink SaaS gradients on CTAs.** Brochure tell.
- **Drop shadows on text.**
- **Multi-color accessibility-badge pills** scattered across cards.
- **Mobile layouts that are just desktop squished.** Design mobile first.
- **Hamburger menus that open full-screen white overlays.** Slide-over, in `masthead`, with Figtree nav.
- **Clever scroll-jack effects** on non-report pages.
- **`text-3xl font-bold`** as a detail-page title. Use `font-display text-h1 tracking-tight`.
- **Color-only form errors.** Always include a message or icon.
- **Unsanitized `dangerouslySetInnerHTML`.** Always pipe external HTML through `isomorphic-dompurify`.
- **Inline `z-[999]` hacks.** Use the z-index scale in `@theme`.
- **`shadow-2xl`** and higher.
- **`tailwind.config.ts` token duplication.** Tokens live in the CSS `@theme` block in Tailwind v4 — one source of truth, not two.
- **Generic "Loading…".** Name what's happening.
- **Blaming error messages.** "Something didn't work" not "Invalid request".

---

## Pre-ship checklist

### Visual
- [ ] Page background is `surface`, not pure white.
- [ ] Body text is `ink`, not pure black.
- [ ] Every heading (hero, section, card, prose) uses `font-display` (Figtree).
- [ ] Body and UI chrome use `font-sans` (Inter).
- [ ] At least one section uses the eyebrow + Figtree headline pattern.
- [ ] No filled gray info boxes — hairline rules or eyebrow + prose instead.
- [ ] Any "featured" treatment uses `muted` bg + `gold` left border, not a color fill.
- [ ] Tables use hairlines; no card wrapper around the table.
- [ ] Hero headline uses `text-balance` and ends with a period.

### Tone
- [ ] Headlines are sentence case, end with a period, read warmly.
- [ ] Second person singular throughout.
- [ ] No exclamation points, no emoji, no marketing puffery.
- [ ] Eyebrows are descriptive, not slogans.
- [ ] Error copy apologizes briefly and offers a next step.
- [ ] Loading copy names what's happening.
- [ ] Separators are middle-dot (`·`), not slash or pipe.

### Tokens
- [ ] Tokens live in the CSS `@theme` block; no duplicate `tailwind.config.ts` values.
- [ ] No hardcoded hex colors in component code. Everything uses `brand.*` tokens.
- [ ] Shadows use the four-level elevation scale; no `shadow-2xl`.
- [ ] Radii use the radius scale.
- [ ] Z-index uses the named scale; no `z-[999]`.

### Interaction
- [ ] Primary CTA is pill-shaped, in `accent`, not a gradient.
- [ ] Focus states visible on every interactive element (warm 2px outline).
- [ ] Modals/slide-overs trap focus, return focus on close, lock body scroll, close on Escape.
- [ ] Skip link present and visible on focus.
- [ ] Touch targets ≥ 44px on mobile.
- [ ] Form errors include a message or icon, not color alone.
- [ ] `.fade-up` used for entrance animation; respects `prefers-reduced-motion`.

### Mobile
- [ ] 375px: no horizontal scroll; hero headline doesn't overflow.
- [ ] Sticky input dock leaves `pb-44 sm:pb-32` for content above.
- [ ] Mobile nav is a slide-over in `masthead`, not a full-screen overlay.
- [ ] Images have explicit `width`/`height`; no layout shift.

### Content
- [ ] Long-form content uses `font-sans`, line-height ≥ 1.6, max-width ≤ 65ch.
- [ ] Prose headings use `font-display` with a size downshift from page H1.
- [ ] Links in `prose` are underlined with `underline-offset-4`.
- [ ] All external HTML piped through `DOMPurify.sanitize()`.
- [ ] Markdown rendered with `react-markdown` + `remark-gfm`.

### Accessibility
- [ ] Contrast passes AA for body text, links, and semantic state colors.
- [ ] Icon-only buttons have `aria-label`.
- [ ] Decorative icons have `aria-hidden="true"` or empty `alt`.
- [ ] Live status indicators have `aria-live="polite"`.
- [ ] `axe-playwright` passes on all routes.
- [ ] Keyboard-only flow completes for primary tasks.
