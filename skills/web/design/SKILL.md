---
name: design
description: My visual design rules for anything I will look at - websites, maps, local HTML pages, Artifacts, slides, Word/PDF/HTML documents, charts and images. Read before building, restyling or visually reviewing any of these.
---

# Design

## How to use this skill
1. Decide the page's **look** from its purpose (next section) and say it in your first line of work.
2. Read this file, then only the reference files for what you are producing. **In Codex, also read `references/codex.md`**: it replaces the steps that name Claude tools.

| Output | Also read |
|---|---|
| A page with the report look (research, brief, data atlas, decision page) | `web.md`, `kit-reference.md`, `charts.md` |
| A page with the showcase look (home or hub page, travel, story or history atlas, catalog or 图鉴, game, film page, personal dashboard or tool) | `showcase.md`, `shelf.md`, `images.md` (plus `kit-reference.md` for the components you reuse) |
| Any map (atlas, drill-down, route, bubbles) | `maps.md` |
| Artifact, or a local single-file HTML page | `artifact.md`, `kit-reference.md` |
| Any chart (HTML/SVG, matplotlib, pptx, docx) | `charts.md` (plus the dataviz skill for chart method) |
| Diagrams | `diagrams.md` (+ the diagram-design skill) |
| Slides (HTML deck by default, or .pptx) | `slides.md` |
| Document (HTML long-read, Word or PDF) | `docs.md` |
| Hero, cover or illustration images | `images.md` |
| Falcon Toolkit or another desktop app | `app.md` |
| Publishing a site; password-protected pages | `publish.md` |
| Any prose, captions, slide text or narration (always) | `writing.md` (short rules; full pass = the de-ai skill) |
| Review before delivery (always) | `review.md` |

Platform skills own the technical contract (artifact-design for Artifacts; pptx/docx/pdf for files; dataviz for chart form and interaction). This skill owns the look. On a technical constraint the platform skill wins; on style, this one wins.

The kit at `E:\Claude\sites\_kit` (`v1.css`, `v1.js`, `styles/editorial.css`, `map/`, `deck/`, `apply_kit.py`) is the single source of colors, type, spacing and map assets. Start from `kit-reference.md`, which lists the components and the kit behaviour that surprises people; open `v1.css` only to debug one rule, and never copy it into a page. In Python get colors from `python scripts/tokens.py --style editorial` instead of typing hex values.

## The look follows the purpose (decided 2026-11-17)
| | Report | Showcase |
|---|---|---|
| When | Someone must decide or learn something from data: research, briefs, market and data atlases, decision pages, slides and documents with data | The page is made to enjoy, to show, to welcome, or to use at home: home and hub pages, travel, history and story atlases, catalogs and 图鉴, games, film pages, personal dashboards and tools |
| Look | **Editorial** (Economist-inspired): white page, falcon-copper rule, one system sans, one blue accent, light only | **One theme drawn from the subject**: a full-screen photograph, painting or cinematic scene, the subject's own colours, one display typeface, texture and motion where they serve it. Dark allowed |
| First screen carries | A short headline, the verdict, and one chart, map, figure or key number | One scene, picture or map that fills the screen, with the title over it and one way in. A tool: the working control with a real result |
| Stays banned | Everything under Restraint and Avoid | Status text, disclaimers, tool names, stamps and counters; mixed image styles; a second display typeface; decoration from some other world |
| The reviewer asks | Are the finding and its evidence on the first screen? | Would this sit beside the pages on `shelf.md`? |

- Unsure which? If the reader is at work deciding something, it is a report. Everything else is a showcase. A data atlas about investments is a report with the map first; an atlas of animals is a showcase with the map first.
- What I say about a given site overrides this table.
- A page operated as a tool keeps the kit's components for its controls under either look.

## Report look (house style decided 2026-10-03, fonts revised 2026-10-14)
| Question | Decision |
|---|---|
| Signature color | Falcon copper `#b4531f` for the top rule, chart tabs, rubric and section numbers (where a page has them); never for data. Red stays for negatives and risk |
| Fonts | One system sans everywhere: Segoe UI / -apple-system for Latin, Microsoft YaHei UI / PingFang SC for Chinese. Headlines bold 700 (never 900: Latin Black next to CJK Bold looks uneven). Georgia serif only on English pages. No Chinese serif and no web fonts: Windows has no CJK serif, so the stack falls to SimSun |
| Density | Medium: prose alternates with charts. Desktop uses the width (side TOC, two-up charts); phone is one column |
| Annotation | Every chart: a conclusion title plus 1–2 short notes with leader lines on the points that matter |
| Interaction | Reports are static with hover tooltips; atlases get filters and switches; motion only when it explains something |
| Office files | Slides and Word use the same system (white page, copper rule, same palette, conclusion titles) |

## Rules for every page
- **First screen.** This is the one definition; other files refer to it. Restraint removes things; it must never leave a screen of words. On desktop and on the phone the first screen carries what the table above says, and `shoot.py --look report|showcase|tool` measures it.
  - Report: a headline of about 24 Chinese characters or 12 English words (the check fails above 28 or 14), the verdict, and something to look at: a chart, a map, a figure, a small table of the key numbers, or one key number. Measure, unit, period and detail go in the line under the headline.
  - On the phone, above the first visual: headline, one line of lede, the verdict. The date and data-cutoff line moves below the verdict or to the sources, and takes one line. If the first visual still does not start on the phone's first screen, shorten what sits above it.
  - Showcase and tool: as in the table above.
- **Conclusion first** (report look). Page headlines, slide titles and chart titles state the finding ("德国仍居首"), not the topic ("各国出口额"). The subtitle carries measure, unit and period.
- **One accent color** for emphasis in data (`--k-accent`, editorial blue `#006ba2`); everything else in muted tones. The categorical series palette (`charts.md`) is only for charts whose categories each need their own identity. Red, amber and green are reserved for status (risk, assumption, good).
- **Colour is never the only signal.** I am colour-blind. Anything told apart by colour is also told apart by a label, a shape, a pattern or its position: status gets a word or icon, chart series get direct labels or different marks. Keep the house palette; do not swap in a "colour-blind palette".
- **Fonts.** Report look: the kit stack, nothing else, including canvas and SVG text; Office files use Microsoft YaHei UI. Showcase look: one display typeface as `showcase.md` allows. Text sizes come from the kit's scale (`--k-fs-*`), not one-off values. `shoot.py` reports the fonts actually rendered; SimSun is a hard failure under either look.
- **Phones.** Benchmark: iPhone 18 Pro Max in Safari (440 pt wide, ~760 pt visible first screen); must still work at 375. `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`; 16px side gutter; no horizontal page scroll; tap targets at least 44px; inputs at least 16px; `dvh`/`svh`, not `vh`, for full-screen blocks; fixed bars pad with `env(safe-area-inset-*)`; nothing that works only on hover; wide tables scroll inside their own box or stack.
- **Contrast.** Text at least 4.5:1 against its background, measured on the image when text sits on a picture; chart marks at least 3:1.
- **Chinese typography.** Space between Chinese and Latin text or numbers ("出口 1,726 亿美元"); full-width punctuation in Chinese sentences; thousands separators; dates as 2026年6月 or 2026-06; units in the subtitle or right after the number. No uppercase or wide letter-spacing on Chinese.
- **Interaction feel.** A click never jumps the page; panels have Back as well as Close; no dark overlay behind side panels; nothing flashes white between states; anything clicked responds within 150 ms. The wheel never needs Ctrl (`maps.md`).
- **Honesty.** Every figure and table has a source line. Label illustrative data 示例.
- **Website Library labels.** A site's library title, description, category and tags follow `publisher/METADATA-STYLE.md` in the GitHub repo washingtonshao-web/model-switchboard.

## Restraint (what I keep deleting)
Every element must earn its place for the reader. Under both looks, do not add:
- vanity totals and counters ("全国 68 人次", "共 2,042 条"), version numbers, build or generation stamps, "data notes", disclaimers, "generated by …", system or sync status text. Meaningful metadata stays: reporting period, units, sources, and the publication date in the meta line;
- tool or model names on cards ("Claude", "Claude Code");
- usage hints longer than one line, and never repeated;
- KPI rows for their own sake: a KPI appears only if the reader would act on that number.

Report look only: no slogans, taglines or mottos; a subtitle only when it carries measure, unit and period. (A home or hub page in the showcase look may carry one line in the site's own voice.)

What stays:
- A count that answers the reader's own filter or search ("视野内 23 种", "显示 10 / 21") is part of the control, not a vanity counter.
- Caveats and limits stay, once each: beside the number they qualify, or in the method and sources section. Not as a banner, and not repeated on every item.
- Every fact, number and source of the page you are rebuilding stays; a total that was decoration becomes a row in a table or a line in the method.

`shoot.py --look` lists the stamps, counters and tool names it finds as `restraint`; remove each one or be able to say why the reader needs it.

**When revising:** change only what I asked for. Do not restyle, reword or reorder anything else; list any other problems you see instead of fixing them. Never drop a link, a field or a heading that was there, and name every region you changed at delivery. Exception: when I ask for a revamp / 重做 / 推倒重来 of a whole deliverable, the revamp skill applies: anything may change; the look, Restraint and Avoid still apply.

## Avoid (the "AI look")
Purple or blue gradients, glassmorphism and glows used as decoration; emoji as icons or bullets; every block in a rounded card; everything centered; a heading over every paragraph; icons that carry no meaning; filler statistics; stock-photo collages; glossy photorealistic AI scenes next to flat charts.
In the showcase look a gradient, a glow or a cinematic image is welcome when it belongs to the subject's scene; the rest of the list still holds.
The words have their own AI look: `writing.md`, and the de-ai skill for a full pass.

## Corrections
A correction I give on one site is recorded with that site (its qc ledger or STATE.md) and fixed there. It becomes a rule in this skill only when the same thing comes up on a second site or I say it is general; a choice I make for one piece ("这次用这个字体") is not a rule for the next. A promoted rule that can be measured becomes a check in `scripts/shoot.py`; a sentence is the fallback.

## Before delivery
Run `review.md`: the measured checks with `--look`, the click test on any page with a control, the short checklist, then the reviewer's verdict for anything published or delivered as finished. Close the delivery with one plain line: the look, checks passed, controls clicked, reviewer and verdict.
