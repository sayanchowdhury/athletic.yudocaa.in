# Athletic — Hugo Theme
### athletic.yudocaa.in

Bold, high-contrast Hugo theme for fitness tracking. Everything data-driven via YAML. No CMS, no database — just files.

---

## Quick start

```bash
# 1. Copy theme into your Hugo project
cp -r theme/athletic/ /path/to/your/hugo-project/themes/

# 2. Copy example site files into your project
cp -r exampleSite/* /path/to/your/hugo-project/

# 3. Run locally
cd /path/to/your/hugo-project
hugo server -D

# 4. Visit http://localhost:1313
```

---

## Directory structure

```
your-hugo-project/
├── hugo.toml                    # site config
├── themes/
│   └── athletic/                # the theme
├── content/
│   ├── log/                     # daily training logs
│   │   ├── _index.md
│   │   └── 2025-03-23-upper-a.md
│   ├── fitness/                 # longer fitness posts
│   │   ├── _index.md
│   │   └── 2025-03-01-why-i-started.md
│   ├── recipes/                 # one stub per recipe
│   │   ├── _index.md
│   │   └── chicken-masala-dinner.md   # just frontmatter, data in YAML
│   ├── stats/_index.md
│   ├── meals/_index.md
│   └── photos/_index.md
└── data/
    ├── stats.yaml               # body stats + weekly log
    ├── photos.yaml              # progress photo entries
    └── recipes/
        ├── chicken-masala-dinner.yaml
        ├── paneer-tikka-tawa.yaml
        └── (one file per recipe)
```

---

## URL structure

| URL | Content |
|-----|---------|
| `athletic.yudocaa.in/` | Homepage with latest log + stats |
| `athletic.yudocaa.in/log/` | All daily log entries |
| `athletic.yudocaa.in/log/daily/2025/upper-a/` | Single log entry |
| `athletic.yudocaa.in/fitness/` | Fitness writing |
| `athletic.yudocaa.in/fitness/2025/why-i-started/` | Single post |
| `athletic.yudocaa.in/recipes/` | Recipe library |
| `athletic.yudocaa.in/recipes/chicken-masala-dinner/` | Single recipe |
| `athletic.yudocaa.in/stats/` | Body stats tracker |
| `athletic.yudocaa.in/meals/` | Meal plan |
| `athletic.yudocaa.in/photos/` | Progress photos |

---

## Daily workflow — adding a log entry

```bash
# Create new log entry (uses archetype automatically)
hugo new log/2025-03-24-lower-b.md

# This generates content/log/2025-03-24-lower-b.md
# with all frontmatter fields pre-filled — just fill in the values
```

### Log entry frontmatter schema

```yaml
---
title: "Lower B — Posterior Focus"
date: 2025-03-24
type: "strength"          # strength | cardio | rest | mobility
duration: 50              # minutes
weight: 84.7              # kg — morning fasted
hevy_url: "https://hevy.com/workout/abc123"

workout:
  - exercise: "Romanian Deadlift (Dumbbell)"
    sets:
      - { set: 1, weight: 20, reps: 10, warmup: true }
      - { set: 2, weight: 30, reps: 8 }
      - { set: 3, weight: 35, reps: 6 }
      - { set: 4, weight: 35, reps: 6, note: "Good depth" }

nutrition:
  calories: 2350
  protein: 84
  carbs: 208
  fat: 60

body:
  weight: 84.7
  sleep: 8
  energy: 8

meals:
  - { name: "Oats + whey + banana", protein: "32g" }
  - { name: "Brown chana sprouts", protein: "10g" }
  - { name: "Fish curry + rice", protein: "38g" }
  - { name: "Green moong sprouts", protein: "8g" }
  - { name: "Pre-workout shake", protein: "24g" }
  - { name: "Lemon herb chicken + veg", protein: "30g" }
---

Session notes go here in Markdown.
```

---

## Adding a recipe

### Step 1 — create the YAML data file

```yaml
# data/recipes/paneer-bhurji.yaml
title: "Paneer Bhurji"
slug: "paneer-bhurji"
category: "dinner"         # dinner | lunch | snack | breakfast
protein_source: "paneer"
prep_time: 5
cook_time: 15
total_time: 20
servings: 1
calories: 280
macros:
  protein: 18
  carbs: 8
  fat: 16
tags: ["paneer", "dinner", "quick"]
meal_prep: false
description: "Scrambled paneer with onion, tomato and capsicum."
ingredients:
  - item: "Paneer"
    amount: "100g"
  - item: "Onion"
    amount: "50g"
steps:
  - "Heat oil, add onion and cook 3 min"
  - "Add tomato, cook 2 min"
  - "Add paneer, scramble with spices 3 min"
reheat: "Microwave 60 sec"
notes: "Optional: add green capsicum for crunch"
```

### Step 2 — create the content stub

```bash
# Just a minimal file — theme reads data from the YAML
cat > content/recipes/paneer-bhurji.md << 'EOF'
---
title: "Paneer Bhurji"
---
EOF
```

Or generate all stubs at once from existing YAML files:

```bash
for f in data/recipes/*.yaml; do
  slug=$(basename "$f" .yaml)
  title=$(grep '^title:' "$f" | sed 's/title: "//' | sed 's/"//')
  echo "---
title: \"$title\"
---" > "content/recipes/$slug.md"
done
```

---

## Updating body stats

Edit `data/stats.yaml` every Sunday morning:

```yaml
current_weight: 84.3    # update this
waist_cm: 93            # update this

weekly_log:
  - week: 3
    date: "2025-03-30"
    weight: 84.3
    waist: 93
    change: -0.6
    notes: "First real movement"
```

---

## Adding progress photos

Edit `data/photos.yaml`:

```yaml
- month: "April"
  year: 2025
  weight: 83.5
  waist: 92
  body_fat: "~21"
  notes: "Visible waist narrowing. Upper chest leaning out."
  images:
    - caption: "Front — April 2025"
      url: "/photos/2025-04-front.jpg"   # put image in static/photos/
    - caption: "Side — April 2025"
      url: "/photos/2025-04-side.jpg"
```

Images go in `static/photos/` — they'll be served at `/photos/filename.jpg`.

---

## Deploying to athletic.yudocaa.in

### Cloudflare Pages (recommended)

```bash
# Build command
hugo --minify

# Publish directory
public/

# Environment variable
HUGO_VERSION = 0.124.0
```

Point your DNS `athletic` subdomain CNAME to your Cloudflare Pages URL.

### Netlify

```toml
# netlify.toml
[build]
  command = "hugo --minify"
  publish = "public"

[build.environment]
  HUGO_VERSION = "0.124.0"
```

### GitHub Pages

```yaml
# .github/workflows/hugo.yml
name: Deploy Hugo site
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.124.0'
          extended: true
      - run: hugo --minify
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

---

## Theme colours (CSS variables)

```css
--acid:   #C8FF00   /* primary accent — electric lime */
--teal:   #00C9A7   /* protein / positive */
--amber:  #FFB800   /* carbs / dinner */
--red:    #FF3D3D   /* fat / cardio / snack */
--black:  #0A0A0A   /* background */
--white:  #F5F5F0   /* text */
```

To customise, override in `static/css/custom.css`:

```css
:root {
  --acid: #00FF88;   /* change accent colour */
}
```

Add `<link rel="stylesheet" href="/css/custom.css">` to your baseof.html extended_head.

---

## What's YAML-controlled (no code editing needed)

| Thing | File |
|-------|------|
| Body stats + weekly log | `data/stats.yaml` |
| Progress photos | `data/photos.yaml` |
| All recipes | `data/recipes/*.yaml` |
| Site config + hero text | `hugo.toml` |
| Daily log entries | `content/log/*.md` (frontmatter) |

Everything else is either automatic (Hugo templates) or Markdown prose.
