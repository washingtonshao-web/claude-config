# Kit map assets

Shared basemap and China boundary layers for every Falconshire map (rules: design skill `maps.md`).

- `tiles/relief/{z}/{x}/{y}.webp`: 512 px shaded-relief raster tiles in Natural Earth style, Web Mercator XYZ. World z0–4; z5 covers China only (x 22–28, y 10–14). Taken from the 杯中山河 site (`claude-drinks`, release 2026-09-30), the look Yang approved.
- `geo/*.json`: GeoJSON lines and label points (lng/lat). `cn_prov_lines` / `cn_pref_lines` are province and prefecture boundaries; `cn_*_labels` carry `n` (short name), `full` and `ad` (admin code). Also `cn_outline`, `borders` (country borders), `country_labels`, `physical_labels` (seas, ranges, deserts).
- Higher zoom: render more tiles with `D:\Claude\260909\tools\relief-hi.py` (AWS Terrain Tiles), as the leaders map does.

`apply_kit.py` copies this folder to `<page dir>/kit/map/` when a page references `kit/map/`.
