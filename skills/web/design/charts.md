# Charts

The dataviz skill decides chart form, marks and interaction. This file decides the look.

## Rules for every style
- Title states the finding ("德国仍居首"); subtitle gives measure, unit and period ("2025年7月–2026年6月出口额，亿美元").
- Label lines and bars directly; a legend only when there are more than 4 series.
- Emphasize the series the title talks about in the accent color; push the rest toward grey.
- Annotate the one or two points the reader must not miss (a short note with a leader line).
- One value axis. No dual axes, no 3D, no pie with more than 5 slices.
- Bars start at zero and are sorted by value unless order itself carries meaning (time, rank change).
- Hairline grid in one direction only; no chart border; no background fill.
- Thousands separators; the same decimals within one chart; negative changes in red, positive in the accent.
- Source line under every chart, 12px, muted.
- Hover tooltip on interactive charts; the static reading must not depend on it.

## Styles
Pick the style for the whole deliverable, not per chart.

**Current default:** `economist` for data reports and research pages (chosen on the car-export atlas, 2026-10-02); `kit` for interactive dashboards and tools.

| Style | Look | Use for |
|---|---|---|
| `economist` | White page, single theme. Red rule across the top of each chart with a short red tab at the left; bold short title plus one-line subtitle; value axis on the right; hairline horizontal grid; condensed sans for chart text. Series: `#006ba2 #3ebcd2 #379a8b #ebb434 #b4ba39 #9a607f #d1b07c #758d99`; red `#e3120b` for brand rule and negatives | Research reports, data briefs |
| `ft` | Light salmon paper, serif headline, tick labels sitting on the grid lines, bold zero line, Oxford blue / orange / teal, series named at the line end | Market and finance audiences |
| `annotated` | One story per chart: the subject in the accent, everything else grey, conclusion title, leader-line notes on the chart | Sharing outside, storytelling; combine with any style above |
| `kit` | Kit tokens `--k-s1…--k-s8` in fixed order, `--k-seq-*` for magnitude; 2px lines with end dots, 10% area tint, 4px rounded bars, both themes | Dashboards, tools, pages that must match existing sites |

To use `economist` on a web page, link `kit/styles/economist.css` after `kit/v1.css` (see `kit-reference.md`); it restyles kit components, so do not read or copy its CSS. Style samples: https://claude.ai/artifact/DqYnAiTXxrWrsRU6VD1MhN.

## Fonts in charts
- Web: chart text uses the page font; `economist` uses `"Roboto Condensed", "Noto Sans SC", "PingFang SC", "Microsoft YaHei UI", sans-serif` (Roboto Condensed from Google Fonts).
- Python and Office: Microsoft YaHei UI for Chinese, the same colors from `python scripts/tokens.py --style economist` (or `--style kit`).

## Python charts (matplotlib)
```python
import subprocess, json, matplotlib as mpl
t = json.loads(subprocess.run(["python", r"C:\Users\Administrator\.claude\skills\design\scripts\tokens.py", "--style", "economist"], capture_output=True, text=True).stdout)
mpl.rcParams.update(t["matplotlib"])
```
Export at 2× (dpi 200), PNG for slides and documents, SVG for the web.
