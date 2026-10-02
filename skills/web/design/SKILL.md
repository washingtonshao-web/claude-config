---
name: design
description: My visual design rules for anything I will look at - websites, local HTML pages, Artifacts, slides, Word/PDF documents, charts and images. Read before building, restyling or visually reviewing any of these.
---

# Design

## How to use this skill
Read this file, then only the reference file for what you are producing:

| Output | Also read |
|---|---|
| Website, map, catalog, game UI (Falconshire sites) | `web.md`, `kit-reference.md` |
| Artifact, or a local single-file HTML page | `artifact.md`, `kit-reference.md` |
| Any chart (HTML/SVG, matplotlib, pptx, docx) | `charts.md` (plus the dataviz skill for chart method) |
| Visual review before delivery (always) | `review.md` |

Platform skills own the technical contract (artifact-design for Artifacts; pptx/docx/pdf for files; dataviz for chart form and interaction). This skill owns the look. On a technical constraint the platform skill wins; on style, this one wins.

The kit at `E:\Claude\sites\_kit` (`v1.css`, `v1.js`, `apply_kit.py`) is the single source of colors, type and spacing. Do not read `v1.css`; use `kit-reference.md`. In Python (matplotlib, python-pptx, python-docx) get colors from `python scripts/tokens.py` instead of typing hex values.

## Rules for every medium
- **Conclusion first.** Page headlines, slide titles and chart titles state the finding ("德国仍居首"), not the topic ("各国出口额"). The subtitle carries measure, unit and period.
- **One accent color.** Red, amber and green are reserved for status (risk, assumption, good), always with a label or icon.
- **Fonts.** Web: the kit stack; never Microsoft YaHei alone (iPhone Safari lacks it). Office files: Microsoft YaHei UI. Headings bold, body regular.
- **Light and dark.** Pages work in both, unless a chosen style is deliberately single-theme (see `charts.md`).
- **Phones.** 16px side gutter, no horizontal page scroll, tap targets at least 44px, wide tables scroll inside their own box.
- **Contrast.** Text at least 4.5:1 against its background; chart marks at least 3:1.
- **Chinese typography.** Space between Chinese and Latin text or numbers ("出口 1,726 亿美元"); full-width punctuation in Chinese sentences; thousands separators; dates as 2026年6月 or 2026-06; units in the subtitle or right after the number.
- **Honesty.** Every figure and table has a source line. Label illustrative data 示例.

## Avoid (the "AI look")
Purple or blue gradients, glassmorphism and glows; emoji as icons or bullets; every block in a rounded card; everything centered; a heading over every paragraph; icons that carry no meaning; filler statistics; stock-photo collages.

## Other media (until they get their own reference file)
- **Slides:** 16:9; the title is a full-sentence conclusion; one idea per slide; at most 5 bullets, each one line; charts follow `charts.md`; numbers large, labels small.
- **Word / PDF:** title, then a one-paragraph summary with the conclusion; at most 3 heading levels; tables with a header rule and no vertical lines; figures numbered with a source line.
- **Images:** one consistent style per deliverable (GPT image via the codex-gpt skill, or real photos); WebP/JPEG under ~300 KB; fixed aspect-ratio boxes; never hotlink third-party hosts.

## Before delivery
Run the visual review in `review.md`: `scripts/shoot.py` for screenshots and measured checks, then the scorecard. Deliver at 16/20 or more with no item at 0; otherwise fix and re-shoot only the affected views.
