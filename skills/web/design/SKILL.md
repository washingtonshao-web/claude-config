---
name: design
description: My visual design rules for anything I will look at - websites, maps, local HTML pages, Artifacts, slides, Word/PDF/HTML documents, charts and images. Read before building, restyling or visually reviewing any of these.
---

# Design

## How to use this skill
Read this file, then only the reference file for what you are producing:

| Output | Also read |
|---|---|
| Website, catalog, game UI (Falconshire sites) | `web.md`, `kit-reference.md` |
| Any map (atlas, drill-down, route, bubbles) | `maps.md` (plus `web.md` for the page around it) |
| Artifact, or a local single-file HTML page | `artifact.md`, `kit-reference.md` |
| Any chart (HTML/SVG, matplotlib, pptx, docx) | `charts.md` (plus the dataviz skill for chart method) |
| Slides (HTML deck by default, or .pptx) | `slides.md` |
| Document (HTML long-read, Word or PDF) | `docs.md` |
| Hero, cover or illustration images | `images.md` |
| Visual review before delivery (always) | `review.md` |

Platform skills own the technical contract (artifact-design for Artifacts; pptx/docx/pdf for files; dataviz for chart form and interaction). This skill owns the look. On a technical constraint the platform skill wins; on style, this one wins.

The kit at `E:\Claude\sites\_kit` (`v1.css`, `v1.js`, `styles/editorial.css`, `map/`, `deck/`, `apply_kit.py`) is the single source of colors, type, spacing and map assets. Do not read its CSS; use `kit-reference.md`. In Python get colors from `python scripts/tokens.py --style editorial` instead of typing hex values.

## House style (decided 2026-10-03, fonts revised 2026-10-14)
| Question | Decision |
|---|---|
| Look | **editorial** (Economist-inspired) for everything with data: reports, briefs, atlases, slides and documents with charts. **kit** look only for interactive dashboards and tools |
| Signature color | Falcon copper `#b4531f` for the top rule, chart tabs, rubric and section numbers (where a page has them); never for data. Red stays for negatives and risk |
| Theme | editorial is light only; kit pages keep light and dark. Map panels may be dark relief (see `maps.md`) |
| Fonts | One system sans everywhere: Segoe UI / -apple-system for Latin, Microsoft YaHei UI / PingFang SC for Chinese. Headlines bold 700 (never 900: Latin Black next to CJK Bold looks uneven). Georgia serif only on English pages. **No Chinese serif and no web fonts**: Windows has no CJK serif, so the stack falls to SimSun |
| Big hero image | Only for travel and lifestyle content, as a full-bleed photo cover with the title over it; data pages open with the conclusion and the key chart or map (see `images.md`) |
| Image style | Flat editorial illustration in the house palette; no photorealistic AI renders. Real photos only for real places and things |
| Density | Medium: prose alternates with charts. Desktop and phone get equal care; desktop uses the width (side TOC, two-up charts), phone is one column |
| Annotation | Every chart: a conclusion title plus 1–2 short notes with leader lines on the points that matter |
| Interaction | By content: reports are static with hover tooltips; atlases, catalogs and tools get filters and switches; motion only when it explains something |
| Office files | Slides and Word use the same system (white page, copper rule, same palette, conclusion titles) |

## Rules for every medium
- **Conclusion first.** Page headlines, slide titles and chart titles state the finding ("德国仍居首"), not the topic ("各国出口额"). The subtitle carries measure, unit and period.
- **One accent color** for emphasis in data (`--k-accent`, editorial blue `#006ba2`); everything else in muted tones. The categorical series palette (`charts.md`) is only for charts whose categories each need their own identity; even then, the series the title talks about stays the strongest. Red, amber and green are reserved for status (risk, assumption, good), always with a label or icon.
- **Fonts.** Web: the kit stack, nothing else, including canvas and SVG text. Office files: Microsoft YaHei UI. Headings bold, body regular. `shoot.py` reports the fonts actually rendered; SimSun is a hard failure.
- **Phones.** Benchmark: iPhone 18 Pro Max in Safari (440 pt wide, ~760 pt visible first screen); must still work at 375. `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`; 16px side gutter; no horizontal page scroll; tap targets at least 44px; inputs at least 16px (iOS zooms otherwise); `dvh`/`svh`, not `vh`, for full-screen blocks; fixed bars pad with `env(safe-area-inset-*)`; nothing that works only on hover; wide tables scroll inside their own box.
- **Contrast.** Text at least 4.5:1 against its background; chart marks at least 3:1. White numbers on mid-tone cells usually fail: use dark text up to the middle of a sequential scale.
- **Chinese typography.** Space between Chinese and Latin text or numbers ("出口 1,726 亿美元"); full-width punctuation in Chinese sentences; thousands separators; dates as 2026年6月 or 2026-06; units in the subtitle or right after the number. No uppercase or wide letter-spacing on Chinese.
- **Interaction feel.** A click never jumps the page; panels have Back as well as Close; no dark overlay behind side panels; nothing flashes white between states; anything clicked responds within 150 ms.
- **Honesty.** Every figure and table has a source line. Label illustrative data 示例.
- **Website Library labels.** A site's library title, description, category and tags follow `publisher/METADATA-STYLE.md` in the GitHub repo washingtonshao-web/model-switchboard.

## Restraint (what I keep deleting)
Every element must earn its place for the reader. Do not add:
- vanity totals and counters ("全国 68 人次", "共 2,042 条"), version numbers, build or generation stamps, "data notes", "generated by …", system or sync status text. Meaningful metadata stays: reporting period, units, sources, and the publication date in the meta line;
- slogans, taglines and mottos; a subtitle only when it carries measure, unit and period;
- tool or model names on cards ("Claude", "Claude Code");
- usage hints longer than one line, and never repeated;
- KPI rows for their own sake: a KPI appears only if the reader would act on that number.

**When revising:** change only what I asked for. Do not restyle, reword or reorder anything else; list any other problems you see instead of fixing them.

## Avoid (the "AI look")
Purple or blue gradients, glassmorphism and glows; emoji as icons or bullets; every block in a rounded card; everything centered; a heading over every paragraph; icons that carry no meaning; filler statistics; stock-photo collages; glossy photorealistic AI scenes next to flat charts.

## Before delivery
Run the visual review in `review.md`: `scripts/shoot.py` for screenshots and measured checks, then the scorecard. For websites and pages others will see, the scorecard is filled in by GPT-6 Astra from the screenshots (independent reviewer), not by you. Deliver at 80% of the applicable points with no item at 0; otherwise fix and re-shoot only the affected views.
