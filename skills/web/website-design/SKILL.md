---
name: website-design
description: Design rules and review checklist for my static websites. Read before building, redesigning or visually reviewing any site, map page or detail view.
---

# Website design rules

## Design kit (use it on every new site)
- Canonical kit: `E:\Claude\sites\_kit\` (`v1.css`, `v1.js`, `apply_kit.py`). Showcase: https://claude-design-kit.falconshire.com
- In `<head>`: `<link rel="stylesheet" href="kit/v1.css">` and `<script src="kit/v1.js"></script>`; `<body class="k">`. Write only page-specific CSS on top; do not restyle kit tokens per site except `--k-accent` when a brand color is required.
- Before publishing, run `python "E:\Claude\sites\_kit\apply_kit.py" <site-dir>`. It inlines the kit so the page is one self-contained HTML file (works with publish.py, the Falconshire Publisher connector and the Bunny mirror). Re-running refreshes an old copy to the current kit.
- Component classes and markup: read `kit-reference.md` in this skill folder when writing the HTML. Do not read v1.css itself.
- Existing sites: move them onto the kit only when I ask for a redesign or a substantial update.

## Page archetypes (the first screen decides the type)
- **Research report**: header → hero (eyebrow, h1, one-line lede, date/meta) → `k-verdict` one-sentence conclusion → 3–5 `k-kpi` → the single most important chart. Then numbered `k-section`s, `k-toc` on wide screens, `k-sources` last. Every section carries at least one visual (chart, table, diagram or KPI row); no section is text only.
- **Map / atlas**: the map fills the first screen. Map rules below.
- **Catalog / encyclopedia**: sticky `k-search` + `k-chips` filters → `k-grid k-grid--rows` cards → `k-drawer` detail.
- **Game**: full-viewport canvas; kit only for menus, HUD text, pause/win/lose overlays.

## Typography and layout
- Fonts come from the kit (Latin UI font → PingFang SC → Microsoft YaHei UI → Noto Sans SC). Never set Microsoft YaHei alone: iPhone Safari does not have it.
- Body 16px on phones and 17px on desktop, line-height 1.75, prose width `--k-measure` (≈40 Chinese characters). Headings bold, body regular.
- One accent color. Red, amber and green are reserved for status (risk, assumption, good), always with a label or icon.
- 16px side gutter on phones; no horizontal page scroll. Wide tables scroll inside `k-table-wrap`.

## Charts
- Load the dataviz skill before the first chart. Use kit chart tokens `--k-s1…--k-s8` in fixed order and `--k-seq-*` for magnitude. One axis per chart, direct labels on ≤4 series, hover tooltip, a source line under every figure.
- Prefer inline SVG built from a JS data array. Label illustrative data as 示例.

## Images
- Every site gets a hero or cover image in one consistent style (GPT image via the codex-gpt skill, or real photos). Store images with the site or on the server; never hotlink Wikimedia or other third-party hosts.
- Compress to WebP/JPEG under ~300 KB each and give images fixed aspect-ratio boxes so the layout never jumps.

## Maps
Dark stylized base with grid lines and a globe outline. Bubbles show counts by region. Provide +/−/reset buttons with the current zoom level shown, filter chips, a legend, and a one-line hint on how to pan and zoom. Use the kit's `k-map` chrome.

## Detail views
A panel that slides in with a photo header, then short labeled fact blocks, with sources last (`k-drawer` + `k-facts` + `k-sources`). On phones, cards become rows with the thumbnail on the left, the drawer becomes a bottom sheet, and search stays pinned at the top.

## Performance
Show something within about 2 seconds. Load large data after the page appears, not before.

## Review loop for large jobs
Set a numeric goal. Have an independent Opus 5.5 (high effort) subagent review each stage. Keep going until the goal is met.

## Visual review (required before delivery)
Inspect the rendered result separately from functionality. Take real screenshots with Playwright and system Chrome (Python `playwright` is installed; `p.chromium.launch(channel="chrome")`) rather than relying on the browser pane, which cannot capture while hidden:
- 1440×900 desktop and 390×844 mobile (`is_mobile=True`, `device_scale_factor=2`), each in light and dark (`color_scheme`).
- In the script, assert no horizontal overflow (`scrollWidth == clientWidth`) and no page errors.
- Look at the images for layout, typography, spacing, alignment, color, contrast, image quality, clipping and overlap. Fix visible problems and re-shoot the affected views before publishing.
