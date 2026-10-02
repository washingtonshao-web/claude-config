# Charts

The dataviz skill decides chart form, marks and interaction. This file decides the look.

## Rules for every style
- Title states the finding ("德国仍居首"); subtitle gives measure, unit and period ("2025年7月–2026年6月出口额，亿美元").
- Every chart carries 1–2 short notes with leader lines on the points the reader must not miss (a turning point, the leader, an outlier). Not more: two notes is the ceiling.
- Label lines and bars directly; a legend only when there are more than 4 series.
- Emphasize the series the title talks about in the accent color; push the rest toward grey.
- One value axis. No dual axes, no 3D, no pie with more than 5 slices.
- Bars start at zero and are sorted by value unless order itself carries meaning (time, rank change).
- Hairline grid in one direction only; no chart border; no background fill.
- Thousands separators; the same decimals within one chart; negative changes in red, positive in the accent.
- Source line under every chart, 12px, muted.
- Hover tooltip on interactive charts; the static reading must not depend on it.

## Styles
Pick the style for the whole deliverable, not per chart.

**Default:** `editorial` for everything with data (reports, briefs, atlases, slides, documents). `kit` only for interactive dashboards and tools. Decided 2026-10-03.

| Style | Look | Use for |
|---|---|---|
| `editorial` | Economist-inspired house style. White page, light only. Falcon-copper `#b4531f` rule across the top of each chart with a short copper tab at the left; bold short title plus one-line subtitle; value axis on the right; hairline horizontal grid; condensed sans for chart text. Series `#006ba2 #3ebcd2 #379a8b #ebb434 #b4ba39 #9a607f #d1b07c #758d99`; red `#e3120b` only for negatives and risk | Default for all data work |
| `kit` | Kit tokens `--k-s1…--k-s8` in fixed order, `--k-seq-*` for magnitude; 2px lines with end dots, 10% area tint, 4px rounded bars, light and dark | Dashboards, tools, pages that must match older kit sites |
| `ft` | Light salmon paper, serif headline, tick labels on the grid lines, bold zero line, Oxford blue / orange / teal | Only when I ask for it |

To use `editorial` on a web page, link `kit/styles/editorial.css` after `kit/v1.css` (see `kit-reference.md`); it restyles kit components, so do not read or copy its CSS. Style samples (original four options): https://claude.ai/artifact/DqYnAiTXxrWrsRU6VD1MhN.

## Fonts in charts
- Web: `editorial` chart text uses `--k-chart-font` (`"Roboto Condensed", "Noto Sans SC", "PingFang SC", "Microsoft YaHei UI", sans-serif`; Roboto Condensed and Noto from Google Fonts, falling back cleanly where they are blocked).
- Python and Office: Microsoft YaHei UI for Chinese, colors from `tokens.py`.

## Python charts (matplotlib)
```python
import subprocess, json, matplotlib as mpl
t = json.loads(subprocess.run(["python", r"C:\Users\Administrator\.claude\skills\design\scripts\tokens.py", "--style", "editorial"], capture_output=True, text=True).stdout)
mpl.rcParams.update(t["matplotlib"])
```
Export at 2× (dpi 200), PNG for slides and documents, SVG for the web. Add the 1–2 notes with `ax.annotate(..., arrowprops=dict(arrowstyle="-", lw=0.6))`.
