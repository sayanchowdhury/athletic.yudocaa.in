# Athletic Theme — Frontend Style Guide

**Bold. High contrast. Dark-first. Sports journal aesthetic.**

Copy this into any project to replicate the Athletic theme's visual language.

---

## Fonts

```
Google Fonts import:
  Barlow Condensed: 400, 600, 700, 800, 900
  Barlow: 300, 400, 500, 600
  JetBrains Mono: 400, 500
```

| Token | Font | Use |
|-------|------|-----|
| `--font-display` | Barlow Condensed | Headings, brand, buttons, labels |
| `--font-body` | Barlow | Body text, descriptions |
| `--font-mono` | JetBrains Mono | Metrics, dates, metadata, code |

### Heading rules
- Font: `--font-display`, weight **800**
- Transform: **uppercase**
- Letter-spacing: `-0.01em`
- Line-height: `1.05`
- Sizing via `clamp()`:
  - h1: `clamp(48px, 8vw, 96px)`
  - h2: `clamp(32px, 5vw, 56px)`
  - h3: `clamp(22px, 3vw, 36px)`
  - h4: `20px`, h5: `16px`

### Body text
- Size: `15px`, line-height: `1.7`, color: `--grey-6`
- Prose content: `17px`, color: `--white` at `0.82` opacity

---

## Color System

### Dark theme (default)

| Token | Value | Role |
|-------|-------|------|
| `--black` | `#0A0A0A` | Background |
| `--white` | `#F5F5F0` | Primary text |
| `--grey-1` | `#141414` | Surface (cards, sections) |
| `--grey-2` | `#1E1E1E` | Elevated surface |
| `--grey-3` | `#2A2A2A` | Borders, dividers |
| `--grey-4` | `#3A3A3A` | Hover borders |
| `--grey-5` | `#6A6A6A` | Secondary text |
| `--grey-6` | `#9A9A9A` | Tertiary text |
| `--acid` | `#C8FF00` | Primary accent (lime) |
| `--acid-dim` | `#8CB200` | Accent muted |
| `--acid-hover` | `#d4ff1a` | Accent hover |
| `--teal` | `#00C9A7` | Protein / positive / success |
| `--amber` | `#FFB800` | Carbs / warning |
| `--red` | `#FF3D3D` | Fat / danger |

### Light theme (`[data-theme="light"]`)

| Token | Value |
|-------|-------|
| `--black` | `#F5F5F0` |
| `--white` | `#1A1A1A` |
| `--grey-1` | `#EAEAE5` |
| `--grey-2` | `#E0E0DB` |
| `--grey-3` | `#CCCCC7` |
| `--grey-4` | `#B0B0AB` |
| `--grey-5` | `#787873` |
| `--grey-6` | `#5A5A55` |
| `--acid` | `#4A7A00` |
| `--teal` | `#009E83` |
| `--amber` | `#CC9300` |
| `--red` | `#D42E2E` |

### Semantic color use

- **Acid (lime):** Primary accent, active states, brand, links, callout borders
- **Teal:** Protein, positive change, success, lunch category
- **Amber:** Carbs, warnings, dinner category
- **Red:** Fat, danger, cardio, snack category
- **Grey scale:** Surfaces, borders, secondary/tertiary text (never color for emphasis)

### Pill color patterns

Pills use translucent backgrounds with matching borders:
```css
--pill-red-bg: rgba(255,61,61,.15);
--pill-red-border: rgba(255,61,61,.3);
/* same pattern for teal, amber */
```

---

## Layout

| Token | Value |
|-------|-------|
| `--radius` | `4px` |
| `--radius-lg` | `8px` |
| Container max-width | `1120px` |
| Narrow container | `720px` |
| Navbar height | `56px` (sticky) |
| Base font size | `16px` |
| Large screen scaling | `zoom: 1.75` at `1200px+` |

### Grid utilities

```css
.grid-2  →  2 columns, 16px gap
.grid-3  →  3 columns, 16px gap
.grid-4  →  4 columns, 12px gap
```

Mobile (below 768px): grid-2 and grid-3 collapse to 1 column, grid-4 to 2 columns.

---

## Components

### Card
- Background: `--grey-1`, border: `1px solid --grey-3`, radius: `--radius-lg`
- Hover: border brightens to `--grey-4`, `translateY(-2px)`
- Optional `.card-accent-top`: 3px acid-colored bar at top
- Body padding: `20px`
- Title: `--font-display`, 20px, weight 800, uppercase

### Pill
- Font: 10px, weight 600, uppercase, `letter-spacing: .06em`
- Padding: `3px 8px`, radius: `2px`
- Variants: `.pill-acid` (solid), `.pill-red` / `.pill-teal` / `.pill-amber` (translucent bg + border), `.pill-ghost` (transparent + grey border)

### Button
- Font: `--font-display`, 13px, weight 700, uppercase, `letter-spacing: .08em`
- Padding: `10px 20px`, radius: `--radius`
- `.btn-acid`: solid accent bg, dark text
- `.btn-ghost`: transparent, white text, grey border → white border on hover

### Stat block
- `.stat-grid`: auto-fit grid with 1px gap (border effect), radius-lg
- `.stat-val`: `--font-display`, 36px, weight 900
- `.stat-lbl`: `--font-mono`, 11px, uppercase, `--grey-6`

### Data table
- Headers: `--font-mono`, 10px, uppercase, `--grey-5`, bg `--grey-1`
- Cells: 15px, `--white` at 0.8 opacity
- Row hover: bg `--grey-2`
- Borders: 1px solid `--grey-3`

### Progress bar (`.prog-row`)
- Layout: flex row — label (80px, mono) + track (flex:1, 6px height) + value (80px, mono, right-aligned)
- Track: `--grey-3` bg, 3px radius
- Fill: animated width transition (`1s ease`)

### Macro bar
- Flex row, 6px height, 2px gap, 3px radius
- Segments: `.macro-seg-p` (teal), `.macro-seg-c` (amber), `.macro-seg-f` (red)

### Section label
- `--font-mono`, 10px, `--acid`, uppercase, `letter-spacing: .15em`
- Followed by a `::after` horizontal line (1px, `--grey-3`)

### Callout
- Left border: 3px `--acid`
- Background: `--callout-bg` (translucent acid)
- Rounded on right side only
- `strong` inside callout: colored `--acid`

### Log entry (timeline)
- Left border: 2px `--grey-3` (timeline line)
- `::before` dot: 8px circle, `--grey-3` (or `--acid` for `.today`)
- Date: `--font-mono`, 11px, `--acid`, uppercase
- Title: `--font-display`, 22px, uppercase
- Body: 15px, `--white` at 0.8 opacity

### Photo grid
- Auto-fill grid, `minmax(200px, 1fr)`, 8px gap
- Items: `aspect-ratio: 3/4`, `object-fit: cover`
- Overlay: gradient from bottom, date label in `--acid` mono

---

## Prose (content typography)

- Max-width: `800px`
- Headings: h2 at 28px, h3 at 22px, 32px top margin
- Paragraphs: 17px, `--white` at 0.82 opacity, 16px bottom margin
- Links: `--acid` with underline, `text-underline-offset: 3px`
- Inline code: `--code-bg`, 14px, `--acid` color, 2px 6px padding
- Code blocks: `--grey-1` bg, `--grey-3` border, 3px `--acid` left border, 18px 22px padding

---

## Responsive

| Breakpoint | Behavior |
|------------|----------|
| Default | Mobile-first base styles |
| `768px` | Grids collapse, nav links hide behind toggle |
| `1200px+` | `zoom: 1.75` global scale |

Mobile nav: links stack vertically in absolute dropdown, 44px touch targets.

---

## JS Patterns

- Vanilla JS, no framework
- Theme toggle: read/write `data-theme` attribute on `<html>`, persist in `localStorage`
- Feature-scoped IIFEs to avoid globals
- Clock: update DOM element every 10s with `setInterval`
- Interactive features (serving multipliers, filters) operate on `data-*` attributes

---

## Design Principles

1. **Dark-first** — `#0A0A0A` bg, light text. Light theme is the alternate.
2. **High contrast accent** — Electric lime (`#C8FF00`) against dark. Never subtle.
3. **Uppercase display type** — Headings and labels always uppercase Barlow Condensed.
4. **Mono for data** — Any number, date, or metric uses JetBrains Mono.
5. **Semantic color** — Teal=protein/positive, Amber=carbs/warning, Red=fat/danger. Consistent everywhere.
6. **Minimal radius** — 4px default, 8px for cards. No large rounded corners.
7. **1px borders** — `--grey-3` dividers everywhere. Surfaces defined by border, not shadow.
8. **No shadows** — Depth via background color layers (`--grey-1` → `--grey-2`) and borders, never box-shadow.
9. **Metric-forward** — Numbers are large (`36px+`), bold (weight 900), display font. Labels are tiny mono.
