# Websites (Falconshire sites)

## Design kit (use it on every new site)
- Canonical kit: `E:\Claude\sites\_kit\` (`v1.css`, `v1.js`, `apply_kit.py`). Showcase (local only; the published page was retired 2026-10-13): `E:\Claude\sites\claude-design-kit\out\index.html`
- In `<head>`: `<link rel="stylesheet" href="kit/v1.css">` and `<script src="kit/v1.js"></script>`; `<body class="k">`. Write only page-specific CSS on top; do not restyle kit tokens per site except `--k-accent` when a brand color is required. Data sites (reports, briefs, atlases) also link `kit/styles/editorial.css` after `v1.css`; dashboards and tools stay on plain kit.
- Before publishing, run `python "E:\Claude\sites\_kit\apply_kit.py" <site-dir>`. It inlines the kit so the page is one self-contained HTML file (works with publish.py, the Falconshire Publisher connector and the Bunny mirror). Re-running refreshes an old copy to the current kit.
- Component classes and markup: `kit-reference.md`.
- Existing sites: move them onto the kit only when I ask for a redesign or a substantial update.

## Publishing and protected pages (moved from CLAUDE.md)
- Publish a single self-contained HTML page with the Falconshire Publisher connector when it is available. A site with local images, data files, map tiles or several pages, or any site when the connector is missing, goes through python "E:\Claude\sites\publish.py" <site-dir>. Use one publishing route per release. Preserve the existing AWS fixed-IP host, access setup, and Bunnynook mirror unless I explicitly request a change.
- Password-protected `*.falconshire.com` pages: open them in the Playwright browser, whose profile (`~\.claude\playwright-profile`) holds my 30-day login for every shared-password site; don't use curl or WebFetch for them. If it shows the `/_falcon-auth/login` page (login expired, a site with its own password, or a new PC), close the Playwright browser, open that profile in a visible Chrome window at the page (`chrome.exe --user-data-dir=<profile> <url>`) and bring it to the front for me to type the password. Once the page title changes, close the window gracefully so the login is saved, then continue.

## Page archetypes (the first screen decides the type)
- **Research report**: header → headline block (bold sans h1 stating the conclusion, one-line lede, date/meta; a rubric above the h1 only for a series name or report type, never the date; no big photo hero, see `images.md`) → `k-verdict` one-sentence conclusion → `k-kpi` row only for numbers the reader would act on (0–4) → the single most important chart. Then `k-section`s (numbered 01/02 only with 4+ sections and a TOC or in-text cross references such as "见第 3 节"), `k-toc` on wide screens, `k-sources` last. Put the evidence in visuals (chart, table, diagram) where it carries the argument; never add a chart or KPI as decoration.
- **Map / atlas**: the map fills the first screen, with no stats banner above it. Follow `maps.md`.
- **Catalog / encyclopedia**: sticky `k-search` + `k-chips` filters → `k-grid k-grid--rows` cards → `k-drawer` detail.
- **Game**: full-viewport canvas; kit only for menus, HUD text, pause/win/lose overlays.

## Typography and layout
- Body 16px on phones and 17px on desktop, line-height 1.75, prose width `--k-measure` (≈40 Chinese characters).
- Fonts come from the kit: one system sans stack (Segoe UI / -apple-system → PingFang SC → Microsoft YaHei UI) for body, headlines (bold 700) and charts. Do not add web fonts, serif CJK stacks or a page-specific font-family; site CSS and canvas/SVG text use `var(--k-font)`.
- Desktop and phone get equal care. Desktop uses the width: side TOC, two charts side by side where they compare; phone is one column with the same order.

## Images
Follow `images.md`: big hero only for travel and lifestyle sites; data sites open with the conclusion; illustrations, not photorealistic AI renders.

## Maps
See `maps.md` (basemap, boundaries, labels, drill-down, click test).

## Detail views
A panel that slides in with a photo header, then short labeled fact blocks, with sources last (`k-drawer` + `k-facts` + `k-sources`). No dark scrim (the kit's default is clear). It has Back (browser back closes it) as well as ✕, and opening it never scrolls the page. On phones, cards become rows with the thumbnail on the left, the drawer becomes a bottom sheet, and search stays pinned at the top.

## Performance
Show something within about 2 seconds. Load large data after the page appears, not before.

## Review loop for large jobs
Set a numeric goal (the `review.md` scorecard works). Each stage gets an independent GPT-6 Astra (high) review: from screenshots for visual stages (`review.md` §5), from the data and text for content stages. If Astra is unavailable, use a fresh Opus 5.5 high-effort agent, labelled 同模型复核. Keep going until the goal is met.
