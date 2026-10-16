# Kit map assets

Shared basemap and China boundary layers for every Falconshire map (rules: design skill `maps.md`).

- `tiles/relief/{z}/{x}/{y}.webp`: 512 px shaded-relief raster tiles in Natural Earth style, Web Mercator XYZ. World z0–4; z5 covers China only (x 22–28, y 10–14). Taken from the 杯中山河 site (`claude-drinks`, release 2026-09-30), the look Yang approved.
- `geo/*.json`: GeoJSON lines and label points (lng/lat). `cn_prov_lines` / `cn_pref_lines` are province and prefecture boundaries; `cn_*_labels` carry `n` (short name), `full` and `ad` (admin code). Also `cn_outline`, `borders` (country borders), `country_labels`, `physical_labels` (seas, ranges, deserts).
- Higher zoom: render more tiles with `D:\Claude\260909\tools\relief-hi.py` (AWS Terrain Tiles), as the leaders map does.

`apply_kit.py` copies this folder to `<page dir>/kit/map/` when a page references `kit/map/`.

## Vector basemap (`basemap.js`)

Self-hosted street-level basemap (Protomaps/OSM vector tiles, Asia z0–14, world z0–7) on `https://tiles.falconshire.com`. Chinese labels, kit borders (`borders.json`, South China Sea dashes, `cn_prov_lines` up to z8), Taiwan labelled 台湾; OSM country and disputed lines are never drawn. Light and dark styles.

```html
<div id="map" style="height:70svh"></div>
<script src="kit/map/basemap.js"></script>
<script>
  K.basemap("#map", { center: [118.79, 32.05], zoom: 11 }).then(function (map) {
    // style is loaded: add your sources and layers here
  });
</script>
```

Options: `center` [lng, lat], `zoom`, `bounds` [[w, s], [e, n]] (overrides center/zoom), `dark` (`true`/`false`, default follows the kit theme), `interactive` (default true), `controls` (false hides +/−), `maxZoom` (default 16), `options` (extra MapLibre map options). On touch screens one finger scrolls the page (cooperative gestures). Loads MapLibre GL 5.24.0 and PMTiles 4.4.1 from the tiles host once per page; failed range requests are retried once. Attribution (© OpenStreetMap contributors · Protomaps) stays visible in compact form.

Styles: default `light.json` is the colourful AMap-like street map (2026-10-17); `quiet: true` loads the pale `quiet.json` for data maps (choropleths, atlases) where the basemap should stay in the background; `dark: true` wins over `quiet`.

To keep place names above your data, insert data layers below the place labels: `map.addLayer(layer, "places_subplace")`. `base` (testing only) serves style, fonts, sprites, geo and libraries from another origin while the tile archives stay on the tiles host.
