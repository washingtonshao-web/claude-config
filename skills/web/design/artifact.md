# Artifacts and local HTML pages

Two cases share these rules: a page published with the Artifact tool, and a single HTML file I open locally (sent with SendUserFile or opened in the browser pane).

## Order of work
1. For a published Artifact, load artifact-design first. It sets the page contract: a 2–4 word `<title>`, tokens on `:root`, dark mode under `prefers-color-scheme` and `:root[data-theme]`, an explicit `body` background, scripts only from the allowed CDNs, stylesheets only from Google Fonts, everything else inline.
2. Build on the kit. It already meets the token and dark-mode parts of that contract: `--k-*` on `:root`, both dark-mode selectors, and the theme toggle sets `data-theme` on `<html>`.
3. Write the page with `<link rel="stylesheet" href="kit/v1.css">` and `<script src="kit/v1.js"></script>`, `<body class="k">`, then run `python "E:\Claude\sites\_kit\apply_kit.py" page.html` to inline the kit (about 28 KB). Never hand an Artifact a relative `kit/` link: it will not load.
4. Run `review.md` on the local file before publishing.

## Pick the shape from the job
| Job | Shape |
|---|---|
| Answer or brief (one finding, a few numbers) | Single column, no header nav: h1 conclusion → `k-kpis` → one chart → short notes and sources |
| Report | Same as the web research-report archetype (`web.md`), TOC only if there are 5+ sections |
| Comparison or decision | Verdict first, then a comparison table with the recommended column marked |
| Tool, calculator or dashboard | Controls on top (or left on desktop), results immediately below; state saves per the artifact-capabilities skill |
| Diagram or explainer | The diagram fills the first screen; text after it |

## Effort
- Match design effort to the job: a quick answer page gets kit defaults and one chart; a deliverable for other people gets a hero, full archetype and the full review.
- Keep it to what the first screen needs: the conclusion and the evidence must be visible without scrolling on a 1440×900 desktop.

## Small things that matter
- Icon parameter on first publish: one plain word (chart, map, report, table).
- Charts follow `charts.md`; for an Artifact, build inline SVG from a JS data array, no chart library unless the chart needs one (then load it from cdnjs).
- Images: inline small ones as WebP data URIs, or upload large ones as assets; keep the page under 16 MB.
