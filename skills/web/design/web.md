# Websites (Falconshire sites)

Publishing, auto-publish and password-protected pages: `publish.md`.

## Design kit (use it on every new site)
- Canonical kit: `E:\Claude\sites\_kit\` (`v1.css`, `v1.js`, `apply_kit.py`).
- In `<head>`: `<link rel="stylesheet" href="kit/v1.css">` and `<script src="kit/v1.js"></script>`; `<body class="k">`. Write only page-specific CSS on top.
- **Report look:** also link `kit/styles/editorial.css` after `v1.css`. Do not restyle kit tokens.
- **Showcase look:** do not link the editorial skin. Set the page's own theme by redefining the kit tokens once on `:root` (`--k-page`, `--k-surface`, `--k-ink`, `--k-ink-2`, `--k-muted`, `--k-line`, `--k-accent`, `--k-accent-soft`) from the palette you named (`showcase.md`), and add the display typeface as one extra variable used only by titles. Kit components then follow the theme.
- Run `python "E:\Claude\sites\_kit\apply_kit.py" <site-dir>` on anything that leaves the build folder (published, sent as a file, opened from elsewhere). It inlines the kit so the page is one self-contained HTML file. Re-running refreshes an old copy.
- Phones: the kit hides `.k-nav` and `.k-toc` under 720px. A page with 4+ sections adds a compact jump row under the header on phones.
- Component classes and markup: `kit-reference.md`.
- Existing sites: move them onto the kit only when I ask for a redesign or a substantial update.

## Page archetypes
- **Research report** (report look): the first screen follows SKILL.md "First screen". Headline block (bold sans h1 at `--k-fs-3xl` stating the conclusion, one-line lede with the detail; a rubric above the h1 only for a series name or report type) → `k-verdict` one-sentence conclusion, which may hold a small table of the key choices → the single most important chart, beside the verdict on desktop where it fits → the date and data-cutoff line → `k-kpi` row only for numbers the reader would act on (0–4). Then `k-section`s (numbered 01/02 only with 4+ sections and a TOC or in-text cross references), `k-toc` on wide screens, `k-sources` last. Put the evidence in visuals where it carries the argument; never add a chart or KPI as decoration.
- **Data atlas** (report look): a slim white title band (title and one line of finding), then the map filling the rest of the first screen, with the evidence (top and bottom items with numbers) at the top of the side panel; no stats banner and no block over the map. Follow `maps.md`.
- **Showcase page** (showcase look): one scene fills the first screen with the title over it (`showcase.md`), then the content in the same theme.
- **Catalog, 图鉴, encyclopedia** (showcase look): a cover scene or the map first, then sticky `k-search` + `k-chips` filters → `k-grid k-grid--rows` cards with real photographs → `k-drawer` detail.
- **Game:** full-viewport canvas; kit only for menus, HUD text, pause/win/lose overlays.

## Typography and layout
- Body 16px on phones and 17px on desktop, line-height 1.75, prose width `--k-measure` (≈40 Chinese characters).
- Text sizes come from the kit scale (`--k-fs-xs sm md lg xl 2xl 3xl 4xl`); do not invent sizes in between. Report look: the kit's one system sans stack for body, headlines (bold 700) and charts, with no web fonts. Showcase look: one display typeface for titles (`showcase.md`), body in `var(--k-font)`.
- Reading sizes: prose at body size; tables, lists and panel rows at least `--k-fs-sm` (14px) in `--k-ink-2` or darker; `--k-fs-xs` and `--k-muted` only for sources, axis ticks and secondary meta. When a first screen is too full, take something off it; never shrink the text to make it fit.
- Long tables: over 15 rows, show the first 10 with a "显示全部 N 行" button, so two long tables never run back to back. Every row stays in the page.
- Desktop and phone get equal care. Desktop uses the width: side TOC, two charts side by side where they compare; phone is one column with the same order.

## Images
Follow `images.md`.

## Maps
See `maps.md` (basemap, boundaries, labels, drill-down, click test).

## Detail views
A panel that slides in with a photo header when the item has a photo, then short labeled fact blocks, with sources last (`k-drawer` + `k-facts` + `k-sources`). When a side list already occupies the right edge, the detail opens inside that list's panel instead (`maps.md`). No dark scrim (the kit's default is clear). It has Back (browser back closes it) as well as ✕, and opening it never scrolls the page. On phones, cards become rows with the thumbnail on the left, the drawer becomes a bottom sheet, and search stays pinned at the top.

## Performance
Show something within about 2 seconds. Load large data after the page appears, not before. A cover image is preloaded and sized so the first screen does not jump.

## Large jobs
Each stage gets the independent verdict in `review.md` (from screenshots for visual stages, from the data and text for content stages). Two rounds at most per stage.
