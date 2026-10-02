# Websites (Falconshire sites)

## Design kit (use it on every new site)
- Canonical kit: `E:\Claude\sites\_kit\` (`v1.css`, `v1.js`, `apply_kit.py`). Showcase: https://claude-design-kit.falconshire.com
- In `<head>`: `<link rel="stylesheet" href="kit/v1.css">` and `<script src="kit/v1.js"></script>`; `<body class="k">`. Write only page-specific CSS on top; do not restyle kit tokens per site except `--k-accent` when a brand color is required. Data sites (reports, briefs, atlases) also link `kit/styles/editorial.css` after `v1.css`; dashboards and tools stay on plain kit.
- Before publishing, run `python "E:\Claude\sites\_kit\apply_kit.py" <site-dir>`. It inlines the kit so the page is one self-contained HTML file (works with publish.py, the Falconshire Publisher connector and the Bunny mirror). Re-running refreshes an old copy to the current kit.
- Component classes and markup: `kit-reference.md`.
- Existing sites: move them onto the kit only when I ask for a redesign or a substantial update.

## Page archetypes (the first screen decides the type)
- **Research report**: header → headline block (rubric, serif h1 stating the conclusion, one-line lede, date/meta; no big photo hero, see `images.md`) → `k-verdict` one-sentence conclusion → 3–5 `k-kpi` → the single most important chart. Then numbered `k-section`s, `k-toc` on wide screens, `k-sources` last. Every section carries at least one visual (chart, table, diagram or KPI row); no section is text only.
- **Map / atlas**: the map fills the first screen. Map rules below.
- **Catalog / encyclopedia**: sticky `k-search` + `k-chips` filters → `k-grid k-grid--rows` cards → `k-drawer` detail.
- **Game**: full-viewport canvas; kit only for menus, HUD text, pause/win/lose overlays.

## Typography and layout
- Body 16px on phones and 17px on desktop, line-height 1.75, prose width `--k-measure` (≈40 Chinese characters).
- Fonts come from the kit (Latin UI font → PingFang SC → Microsoft YaHei UI → Noto Sans SC); editorial adds serif headlines and a condensed chart font.
- Desktop and phone get equal care. Desktop uses the width: side TOC, two charts side by side where they compare; phone is one column with the same order.

## Images
Follow `images.md`: big hero only for travel and lifestyle sites; data sites open with the conclusion; illustrations, not photorealistic AI renders.

## Maps
Data atlases use the editorial light map (pale land, white borders, copper rule on the frame); a dark stylized base with grid lines and a globe outline only for kit-style explorers. Bubbles show counts by region. Provide +/−/reset buttons with the current zoom level shown, filter chips, a legend, and a one-line hint on how to pan and zoom. Use the kit's `k-map` chrome.

## Detail views
A panel that slides in with a photo header, then short labeled fact blocks, with sources last (`k-drawer` + `k-facts` + `k-sources`). On phones, cards become rows with the thumbnail on the left, the drawer becomes a bottom sheet, and search stays pinned at the top.

## Performance
Show something within about 2 seconds. Load large data after the page appears, not before.

## Review loop for large jobs
Set a numeric goal (the `review.md` scorecard works). Have an independent Opus 5.5 (high effort) subagent review each stage. Keep going until the goal is met.
