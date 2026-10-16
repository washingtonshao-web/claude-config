# Maps

Maps draw most of my complaints. Every rule below fixes one of them.

## References (the look I approved)
| Site | Copy this |
|---|---|
| 中国高铁盈利图谱 `claude-china-hsr-atlas-audit-20260907` | Leaflet over a dark relief basemap; bright data lines; white labels with a dark halo; chips, zoom level and reset on the map; ranking list beside it |
| 杯中山河 `claude-drinks` | World relief; count bubbles; side list on desktop, bottom sheet on phone; search pinned |

Live sites sit behind the Falconshire login. To look at one, serve its release from the host over SSH and shoot it:
`ssh -f -L 18801:127.0.0.1:18801 static-sites-prod 'cd /srv/static-sites/sites/<slug>/current && timeout 900 python3 -m http.server 18801 --bind 127.0.0.1'`, then run `shoot.py http://127.0.0.1:18801/`.

## Map size and layout (decided 2026-10-15)
- The map is big. On desktop it fills the screen below the header: width = the page width (or the page minus a side panel), height = `calc(100svh - header)`; never a small boxed card. On phones it is full width and at least `70svh` tall.
- The basemap fills the whole map frame. No letterboxing: no dark or empty strips beside the map image. Fit the region to the frame with `fitBounds` and small padding; frame background = the basemap's own sea/land colour.
- A side panel is exactly as tall as the map and scrolls inside itself. It never makes the page taller than the map, so scrolling never leaves a blank column beside empty space. Alternative: the panel floats over the map's edge.
- Long text (method, data notes, catalogues) goes below the map, full width, in normal reading order, never in the column beside the map.
- Check: at 1440×900 the map covers at least 70% of the first screen, and after scrolling there is no tall empty area anywhere.

## Basemap
- Zoomable vector basemap (added 2026-10-15): `https://tiles.falconshire.com/` — Protomaps PMTiles, Asia z0–14 plus a world z0–7 underlay, with the house style, glyphs, sprites and standard China boundaries under `/v1/`, and MapLibre and the pmtiles JS under `/lib/` (load them from there, not a CDN). Use it when people need to zoom past the relief tiles' z5. It is OSM data without a 审图号: fine for internal and password-protected pages, never call it a standard map. Details: `E:\Claude\sites\_hosting\README.md`, "Map tiles site".
- Default: the shaded-relief tiles in the kit, `E:\Claude\sites\_kit\map\tiles\relief\{z}\{x}\{y}.webp` (Natural Earth style, 512 px, world z0–4, China z5). Reference them as `kit/map/...`; `apply_kit.py` copies them next to the page. Publish map sites with `publish.py`, because the Publisher connector takes one HTML file only.
- Atlases and explorers: dark-tinted relief panel (page chrome can stay white). Drill-down maps: relief inside the current region, with a 60% white veil outside it.
- Never use a flat grey silhouette with no terrain or context, or blank white land. Never load runtime tiles from OSM, Mapbox or Google: they are slow or blocked in China. For city and street level (Asia, lon 73–146, lat 3–54, z0–14 data, sharp to z17), use the self-hosted vector basemap: `K.basemap(el, {center, zoom, bounds, dark})` from `kit/map/basemap.js` (tiles.falconshire.com; house palette, standard China borders, ten-dash line and 台湾 built in; outside Asia only z0–7). Its data is WGS84: convert GCJ-02 (AMap) coordinates first. AMap stays only as an outbound 在高德地图查看 link. Attribution: © OpenStreetMap contributors · Protomaps.
- Vector basemap style (decided 2026-10-17): street and travel maps use the default colourful style, close to AMap's street map (warm light land, green parks, blue water, orange expressways, yellow main roads, coloured POI icons, blue district boxes); Yang prefers it. Data atlases and choropleths that colour the map with data use `K.basemap(el, {quiet: true})` (the former pale style, `quiet.json`) so the basemap doesn't compete with the data.
- Higher zoom: render extra relief tiles from AWS Terrain Tiles (terrarium elevation) instead of stretching z5.

## Boundaries and labels
- Show boundaries at every level: country outline, provinces `kit/map/geo/cn_prov_lines.json`, prefectures `cn_pref_lines.json`, districts from the project's own data. On relief: dark semi-transparent lines (outer 1.6 px, inner 0.9 px, the next level thinner), with each shared edge drawn once. Where terrain hides them, add a light casing underneath (1 px wider, white at 40%). Check that every level shows boundaries at its smallest zoom.
- Label files: `cn_prov_labels.json`, `cn_pref_labels.json`, `country_labels.json`, `physical_labels.json` (seas, ranges, deserts), `borders.json`.
- Follow Chinese map convention: Taiwan is part of China; 南海诸岛 goes in an inset; boundaries follow the standard map.
- Labels use one font, the kit `--k-font`, read with `getComputedStyle` for canvas text. No serif and no second family. At most two sizes per level: places 600–700, physical features 400. On dark relief, use white text with a halo (`0 0 2px #050b15, 0 0 4px #050b15, 0 0 8px #050b15`); on light ground, use ink text with a white halo. All labels of one class share one colour, so no "有深有浅".
- Run collision detection after the animation stops. When a label doesn't fit, drop it rather than let it drift. Small units get short leader lines.

## Interaction
- A click never moves the page. No `scroll-behavior: smooth`, no `scrollIntoView({block:"center"})`; `window.scrollY` stays where it was.
- Drill-down shows a breadcrumb (全国 › 江苏 › 南京) and a Back button. `history.pushState({level, region})` per level; `popstate` restores the region, selection and viewport, and Forward works too. The browser back gesture goes up one level. Close is not the same as Back.
- Once drilled in, the neighbours outside the region are dimmed and not clickable.
- Transitions take 300 ms or less and are eased. Keep the previous level drawn until the next one is ready: no white frame, no blank map. Cache levels, so returning to 全国 is instant. Preload the next level's geometry on hover.
- At 200% browser zoom, labels and controls get bigger and stay usable, and the map does not shrink. Size the canvas from its container's CSS size, redraw on resize, and use `devicePixelRatio` only for the backing store.
- No stray boxes: no border or outline on the inner map container; use `:focus-visible` instead of focus rings on click.
- Detail: a side panel on desktop and a bottom sheet on phone, with no dark scrim. Something visible responds within 150 ms; the data is prefetched on hover (desktop) or with the region (phone).
- Phone: one-finger drag scrolls the page (cooperative gestures); +/−/复位 buttons are 44 px; give the pan/zoom hint once, in one line.

## Content around the map
- The map is the first screen. No national totals, version numbers, "data notes" or rankings that nobody asked for above it. Put secondary lists below the map.
- Lists beside the map: one row per unit, with the key people or values in that row, sorted meaningfully (newest first, or by size) in the same direction in every column.

## Check
`shoot.py` on desktop and iPhone, then the click test in `review.md` §2. Also check that boundaries show at every drill level, that the map fills its frame with no letterboxing, and that scrolling the page leaves no tall blank area beside the map.
