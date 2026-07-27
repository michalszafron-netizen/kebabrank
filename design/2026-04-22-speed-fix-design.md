# kebabrank.com — Speed Fix Design Doc

**Date:** 2026-04-22  
**Goal:** Fix mobile AND desktop load performance (Core Web Vitals) to unblock SEO ranking improvements.  
**Scope:** Speed-only ship. UI/redesign is a separate, later effort.  
**Out of scope:** New dark-mode dashboard design (design/code.html), content SEO work, Ahrefs crawl fixes.

---

## Diagnosis: What's Actually Slow

### 1. Tailwind CSS CDN (Critical — fix this first)

**File:** `templates/base.html:119`

```html
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
```

This is the development CDN build. It downloads ~4MB of JavaScript, then scans your entire DOM at runtime and generates CSS on the fly. PageSpeed Insights will give this a red flag every time. It's the single biggest performance hit on the page.

**Fix:** Replace with compiled, purged Tailwind CSS (~20–40KB).

---

### 2. Three Separate Google Fonts Requests (High Impact)

**File:** `templates/base.html:122–127`

Three separate network connections to Google Fonts:
- `Inter:wght@400;700;900` — body font
- `Material Icons` — icon set 1
- `Material Symbols Outlined` — icon set 2 (variable font, ~400–600KB)

Each is a separate DNS lookup + TLS handshake + HTTP request. Material Symbols Outlined is the worst offender — it's a huge variable font loaded with a very broad weight/fill range (`wght,FILL@100..700,0..1`).

**Fix:** Self-host Inter. Replace Material Symbols with a self-hosted subset or SVG icons.

---

### 3. Unminified CSS Being Served (Easy Win)

**File:** `templates/base.html:153`

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}?v=6">
```

`style.min.css` exists in `static/css/` but isn't being used. You're serving 492 lines of unminified CSS.

**Fix:** One line change. Use `style.min.css`.

---

### 4. Leaflet.js from External CDN (Medium Impact)

**File:** `templates/base.html:130`

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" ...>
```

Leaflet JS and CSS are loaded from `unpkg.com` on every page, even when the map isn't in view. External CDN = extra DNS + connection + no cache guarantee.

**Fix:** Bundle Leaflet locally in `static/js/` + lazy-load it only when the map tab is opened.

---

### 5. Two Analytics Scripts in `<head>` (Low Impact, Easy to Fix)

Both `gtag` and Ahrefs analytics load in `<head>` with `async`. The `async` attribute means they don't block parsing, so this is lower priority. But moving them to just before `</body>` removes them from the critical rendering path entirely.

---

## Proposed Architecture

### Before

```
<head>
  ├── Google Analytics (async)
  ├── Ahrefs Analytics (async)
  ├── preload cdn.tailwindcss.com  ← contradictory with CDN approach
  ├── preconnect fonts.googleapis.com
  ├── Tailwind CDN script (~4MB runtime)   ← MAIN KILLER
  ├── Google Fonts: Inter               ← request 1
  ├── Google Fonts: Material Icons      ← request 2
  ├── Google Fonts: Material Symbols    ← request 3 (~400KB variable font)
  ├── Leaflet CSS (unpkg)               ← external CDN
  ├── tailwind.config inline script
  ├── style.css (492 lines, unminified)
  └── skeleton.css
```

### After (Speed-Only Ship)

```
<head>
  ├── preconnect (self-hosted fonts folder)
  ├── preload inter-latin-subset.woff2   ← critical font, preloaded
  ├── Compiled Tailwind (~25KB minified)  ← replaces 4MB CDN
  ├── Inter self-hosted CSS (@font-face)  ← replaces Google Fonts request 1
  ├── Material Icons self-hosted subset   ← replaces Google Fonts request 2
  ├── style.min.css                       ← replaces unminified style.css
  └── skeleton.css

<body>
  ...content...
  ├── Leaflet (loaded lazily on map tab open, from /static/js/leaflet/)
  ├── Google Analytics (moved here, async)
  └── Ahrefs Analytics (moved here, async)
```

---

## Implementation Plan (Ordered by Impact)

### Step 1: Compile Tailwind CSS locally (~2 hours)

**Impact:** Largest. Drops CSS payload from ~4MB to ~25KB.

1. Install Tailwind CLI:
   ```bash
   npm install -D tailwindcss
   ```

2. Create `tailwind.config.js` in project root — move your existing inline config here:
   ```js
   module.exports = {
     darkMode: 'class',
     content: ['./templates/**/*.html', './static/js/**/*.js'],
     theme: {
       extend: {
         colors: {
           'primary': '#ff6a00',
           'background-light': '#f8f7f5',
           'background-dark': '#0b1121',
           'surface-dark': '#1e293b',
         },
         fontFamily: { 'display': ['Inter', 'sans-serif'] },
         borderRadius: { 'DEFAULT': '0.5rem', 'lg': '1rem', 'xl': '1.5rem', 'full': '9999px' },
       },
     },
     plugins: [require('@tailwindcss/forms')],
   }
   ```

3. Create `static/css/input.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

4. Build:
   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.min.css --minify
   ```

5. Add a build script to `package.json` (or a Makefile):
   ```json
   "scripts": {
     "build:css": "tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.min.css --minify",
     "watch:css": "tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.min.css --watch"
   }
   ```

6. In `base.html`, replace:
   ```html
   <!-- DELETE this preload -->
   <link rel="preload" href="https://cdn.tailwindcss.com?plugins=forms,container-queries" as="script">
   
   <!-- DELETE this script -->
   <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
   
   <!-- DELETE the inline tailwind-config script -->
   <script id="tailwind-config">tailwind.config = {...}</script>
   ```
   
   Add instead:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='css/tailwind.min.css') }}?v=1">
   ```

**Validation:** Run the build, open the site, verify no styles are broken. Check that dark mode class still works (`<html class="dark">`). If any styles break, they're using dynamic class names — add them to the Tailwind `safelist` in config.

---

### Step 2: Use the minified CSS that already exists (~5 minutes)

In `base.html:153`, change:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}?v=6">
```
to:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.min.css') }}?v=6">
```

Done.

---

### Step 3: Self-host Inter font (~1 hour)

Google Fonts for Inter adds latency + GDPR concerns (user IP sent to Google). Self-hosting avoids both.

1. Go to [gwfh.mranftl.com](https://gwfh.mranftl.com/fonts) (google-webfonts-helper)
2. Search "Inter", select weights: 400, 700, 900 — Latin subset only
3. Download WOFF2 files → place in `static/fonts/inter/`
4. Download the generated `@font-face` CSS → add to `style.css` (and rebuild `style.min.css`)
5. In `base.html`, replace the Inter Google Fonts link with:
   ```html
   <link rel="preload" href="/static/fonts/inter/inter-latin-400.woff2" as="font" type="font/woff2" crossorigin>
   <link rel="preload" href="/static/fonts/inter/inter-latin-700.woff2" as="font" type="font/woff2" crossorigin>
   ```
   (No Google Fonts link needed — the CSS handles it via `@font-face`)

---

### Step 4: Replace Material Symbols/Icons with a self-hosted subset (~2 hours)

Material Symbols Outlined is loaded with `wght,FILL@100..700,0..1` — the maximum range. This downloads a huge variable font file.

**Option A (Simpler):** Pin to a fixed subset using Google Fonts' `text=` parameter:
```html
<!-- Only load the specific icons you use -->
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap" rel="stylesheet">
```
This narrows the download significantly. Audit your templates for which icons are actually used and list them in `&text=icon1,icon2,icon3`.

**Option B (Best — no external requests):** Download a subset of Material Icons as SVGs and inline them or serve from `/static/img/icons/`. This is a bigger effort but eliminates the external font dependency entirely.

**Recommendation for this ship:** Do Option A. It's one line change and cuts the variable font payload by 60-70%. Option B is right for the redesign ship.

---

### Step 5: Lazy-load Leaflet (~1 hour)

Leaflet loads on every page, but the map is only shown when the user clicks a map tab. Move Leaflet to lazy load:

1. Download Leaflet 1.9.4 CSS + JS → `static/js/leaflet/leaflet.css` and `leaflet.js`
2. Remove the `<link rel="stylesheet">` for Leaflet from `<head>`
3. In the JS that initializes the map, add a dynamic loader:
   ```javascript
   async function loadMap() {
     if (window.L) return; // already loaded
     await Promise.all([
       loadCSS('/static/js/leaflet/leaflet.css'),
       loadScript('/static/js/leaflet/leaflet.js')
     ]);
     initializeMap();
   }
   ```
   Call `loadMap()` when the user opens the map tab.

---

### Step 6: Move analytics to bottom of `<body>` (~10 minutes)

In `base.html`, move the Google Analytics and Ahrefs scripts from `<head>` to just before `</body>`. Both already have `async`, so this is cosmetic — but it removes them from PageSpeed's "eliminate render-blocking resources" list.

---

## Expected Outcome

| Metric | Before (estimate) | After (estimate) |
|--------|-------------------|------------------|
| CSS payload | ~4MB+ | ~25–40KB |
| Font requests | 3 external | 1 preloaded local |
| External CDN deps | 3 (Tailwind, Fonts×3, Leaflet) | 0 on page load |
| Mobile Performance score | ~30–50 | ~75–90 |
| LCP | 4–6s | 1.5–2.5s |
| Build step required? | No | Yes (1 command) |

Actual scores will depend on server response time and network. Run PageSpeed after each step to validate.

---

## Risks

1. **Dynamic Tailwind class names** — if JavaScript builds class strings like `text-${color}-500`, Tailwind's purge won't find them. Audit `static/js/` for dynamic class generation. Add any found to `tailwind.config.js` safelist.

2. **`container-queries` plugin** — you're using it in the CDN URL. Add `require('@tailwindcss/container-queries')` to the plugins array in `tailwind.config.js` (install: `npm install -D @tailwindcss/container-queries`).

3. **Flask static file caching** — increment the `?v=` cache-buster on `tailwind.min.css` every time you rebuild.

4. **CI/CD build step** — the compiled CSS needs to be built before deploy. If you're using Docker, add `npm run build:css` to your `Dockerfile` build step.

---

---

## Desktop — Additional Issues (Beyond Mobile)

Desktop PageSpeed typically scores 20-30 points higher than mobile because Google assumes faster CPU and network. The Tailwind CDN issue still hurts desktop — just less than mobile. After fixing Tailwind, desktop should reach 90+.

But desktop has **two additional issues mobile doesn't have.**

---

### Desktop Issue 1: app.js Loaded Unminified (Easy Win)

**File:** `templates/base.html` (near `</body>`)

```html
<script src="{{ url_for('static', filename='js/app.js') }}?v=1" defer></script>
```

`app.min.js` already exists in `static/js/` but isn't being used. `app.js` is 2,530 lines of unminified JavaScript. Same pattern as `style.css` vs `style.min.css` — you have the minified file, you're just not loading it.

**Fix:** One line change.

```html
<script src="{{ url_for('static', filename='js/app.min.js') }}?v=1" defer></script>
```

**Important:** Make sure `app.min.js` is kept in sync with `app.js` when you make JS changes. Add a build step:

```bash
npx terser static/js/app.js -o static/js/app.min.js --compress --mangle
```

Or add it to your `package.json` scripts alongside the Tailwind build:

```json
"build:js": "terser static/js/app.js -o static/js/app.min.js --compress --mangle",
"build": "npm run build:css && npm run build:js"
```

---

### Desktop Issue 2: Leaflet CSS Blocks Rendering on Desktop

**File:** `templates/base.html:130`

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" ...>
```

On **mobile**, the map is hidden (`hidden md:flex`) so this is wasteful but not critical.  
On **desktop**, the map panel takes 65% of the screen and is visible on initial load. Leaflet is a hard dependency for desktop — you can't lazy-load it. But you can still eliminate the external CDN round-trip by self-hosting it.

**Fix:** Download Leaflet locally.

```bash
# Download to static/js/leaflet/
curl -o static/js/leaflet/leaflet.css https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
curl -o static/js/leaflet/leaflet.js https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
```

In `base.html`, replace:
```html
<!-- DELETE these two lines -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="..." crossorigin="">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="..." crossorigin="" defer></script>
```

Add instead:
```html
<!-- Desktop: Leaflet needed immediately for map panel -->
<link rel="stylesheet" href="{{ url_for('static', filename='js/leaflet/leaflet.css') }}">
<script src="{{ url_for('static', filename='js/leaflet/leaflet.js') }}" defer></script>
```

This removes the external CDN dependency and gives you a guaranteed cache hit after first load.

**Mobile optimization (bonus):** On mobile, the map is hidden and Leaflet isn't needed until the user taps "Mapa". You can skip loading Leaflet on mobile entirely and only load it on map tab click. But this requires a JS change to dynamically load the CSS + JS. Worth doing in a follow-up, not this ship.

---

### Desktop vs Mobile — Issue Comparison

| Issue | Mobile impact | Desktop impact | Fix applies to both? |
|-------|--------------|----------------|----------------------|
| Tailwind CDN (~4MB) | Critical | High | Yes — same fix |
| 3 Google Fonts requests | High | High | Yes — same fix |
| style.css unminified | Medium | Medium | Yes — same fix |
| app.js unminified | Medium | Medium | Yes — same fix (new) |
| Leaflet from unpkg CDN | Low | Medium | Self-host for both; lazy-load mobile only later |
| Analytics in `<head>` | Low | Low | Yes — same fix |

---

### Updated Implementation Plan (Desktop Additions)

The mobile plan from above still applies. Add these two steps:

**Step 2b: Use app.min.js (~5 minutes)**

In `base.html` (near `</body>`), change:
```html
<script src="{{ url_for('static', filename='js/app.js') }}?v=1" defer></script>
```
to:
```html
<script src="{{ url_for('static', filename='js/app.min.js') }}?v=1" defer></script>
```

**Step 4b: Self-host Leaflet (~20 minutes)**

Download Leaflet to `static/js/leaflet/`, update the two references in `base.html` as shown above.

---

### Updated Expected Outcome

| Metric | Mobile Before | Mobile After | Desktop Before | Desktop After |
|--------|--------------|--------------|----------------|---------------|
| Performance score | ~30–50 | ~75–90 | ~55–70 | ~88–96 |
| LCP | 4–6s | 1.5–2.5s | 2–4s | 1–2s |
| CSS payload | ~4MB+ | ~25–40KB | ~4MB+ | ~25–40KB |
| JS payload (app.js) | large | ~60% smaller | large | ~60% smaller |
| External CDN deps | 3+ | 0 | 3+ | 0 |

Desktop scores higher because PageSpeed assumes a faster device and network. The same fixes apply — desktop just starts from a better baseline.

---

## What's Not in This Doc

- The dark-mode redesign (design/code.html) — that's a separate ship
- Ahrefs-specific issues (broken links, duplicate content, missing H1s on specific pages)
- Server-side caching / Flask-Caching tuning
- Image optimization (top10.png, city photos)
- Structured data expansion or content SEO

---

## GSTACK REVIEW REPORT
*Generated by /autoplan — 2026-04-22*

### Review Runs

| Review | Status | Findings |
|--------|--------|----------|
| CEO Review | DONE | Hold Scope. Plan correct direction. Inter partially done. |
| Eng Review | DONE | 4 findings: 3 critical, 1 medium |
| Design Review | DONE | 2 concerns (both covered by Eng findings) |
| Codex Review | SKIPPED | Binary unavailable |

### Overall Verdict: NEEDS_FIXES_BEFORE_SHIP

3 blocking issues found. Plan is correct in direction but incomplete in 3 specific areas. Fix these before implementation.

---

### Critical Fixes Required

#### Fix A: Add Tailwind Safelist for Dynamic Rank Badge Classes

`static/js/app.js:2175-2178` builds Tailwind class strings via JavaScript assignment.
Tailwind's static scanner won't find them — they'll be purged from the compiled CSS.
This breaks the gold/silver/bronze rank badges (most visible UI element on the page).

Add to `tailwind.config.js`:
```javascript
safelist: [
  'bg-surface-dark', 'text-gray-400',      // rank badge default
  'bg-yellow-500', 'text-black',            // rank 1 gold
  'bg-gray-400',                            // rank 2 silver
  'bg-orange-700', 'text-white',            // rank 3 bronze
  'group', 'snap-start', 'active',          // app.js:2102 compact-city-card
]
```

#### Fix B: Fix Inter Unicode-Range for Polish Diacritics

`static/css/style.css:1-8` already has a self-hosted Inter `@font-face` — but the
`unicode-range` excludes Polish diacritics (ą=U+0105, ę=U+0119, ś=U+015B, etc.).
Currently the Google Fonts fallback in `base.html` covers these. Removing Google Fonts
without fixing the unicode-range means Polish city names render in system font.

Step 1 — verify WOFF2 has Latin Extended glyphs:
```bash
python3 -c "from fontTools.ttLib import TTFont; f=TTFont('static/fonts/inter/inter-latin-var.woff2'); print(sorted([hex(c) for c in f.getBestCmap().keys() if 0x100 <= c <= 0x24F]))"
```

Step 2 — if glyphs present, extend unicode-range in `style.css`:
```css
unicode-range: U+0000-00FF, U+0100-024F, U+0131, U+0152-0153,
               U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304,
               U+0308, U+0329, U+2000-206F, U+20AC, U+2122,
               U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
```

Step 3 — only then remove the Google Fonts Inter link from `base.html`.

Note: Step 3 in the original plan says "self-host Inter" but Inter is already
self-hosted (style.css:1). The actual work is fixing the unicode-range and
removing the now-redundant Google Fonts link.

#### Fix C: Docker Strategy — Commit tailwind.min.css to Git

`dockerfile` uses `FROM python:3.9-slim`. No Node.js. `npm run build:css`
won't run in the current Dockerfile without a multi-stage build.

Simplest fix: build locally, commit the output file to git.
```bash
npm run build:css
git add static/css/tailwind.min.css
git commit -m "chore: add compiled tailwind (build output)"
```
Rebuild and recommit whenever new Tailwind classes are added to templates.

---

### Auto-Decided (No Action Needed)

| Decision | Choice | Reason |
|----------|--------|--------|
| container-queries plugin | DROP — not used anywhere | Zero `@container` in codebase |
| Material Symbols strategy | Option A (pinned subset) | Good enough for this ship |
| Full plan vs minimal-only | Full plan | 5-min wins leave 60+ points on table |

The `tailwind.config.js` plugins line should be:
```javascript
plugins: [require('@tailwindcss/forms')]
// NOT: require('@tailwindcss/container-queries') — never used, don't add
```

---

### Visual Test Checklist (add before shipping)

Run these manually in local dev after the build:
- [ ] Rank badge #1 shows gold background (`bg-yellow-500`)
- [ ] Rank badge #2 shows silver (`bg-gray-400`)
- [ ] Rank badge #3 shows bronze (`bg-orange-700`)
- [ ] Polish diacritics (ą, ę, ś, ź, ż, ć, ń, ł) render in Inter, not system font
- [ ] Dark mode active (`<html class="dark">` → dark background visible)
- [ ] Desktop map loads (35/65 split, L.map() initializes)
- [ ] Mobile "Mapa" tab loads the map
- [ ] Chrome DevTools Network tab: zero requests to `cdn.tailwindcss.com` or `unpkg.com`
- [ ] PageSpeed mobile score recorded (before vs after baseline)
