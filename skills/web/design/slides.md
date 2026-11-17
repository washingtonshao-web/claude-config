# Slides

## Route
| Request | Build with |
|---|---|
| A deck, with no file format named (default) | A single-file **HTML deck** on `kit/deck` (below). Publish it per CLAUDE.md Websites, and also deliver the 16:9 PDF from `deck_pdf.py` for WeChat and email |
| Others must edit it, or a .pptx/.potx is named or supplied | The pptx skill; this file sets the look |
| The Artifact **Slides** type | Only when I ask for it by name; use the design system **Falconshire Editorial** (https://claude.ai/artifact/24eZ3vxVomaArgKq7SY8K2) |
| An animated or video-style deck | HyperFrames, only when I ask for animation |

For .pptx: the pptx skill's "safe font" list does not apply: headings are Microsoft YaHei UI Bold and body text Microsoft YaHei UI. Leave about 10% slack in text boxes, because LibreOffice QA may substitute the font.

## Page
- 16:9 and a white background. Every slide has a 4px falcon-copper `#b4531f` rule across the top, with a short copper tab at the left (mirrors the web chart frame).
- Microsoft YaHei UI throughout (HTML: the kit's system stack, which is Segoe UI / PingFang SC / Microsoft YaHei UI); titles bold 28–32pt, body regular 16–20pt, source lines 10–11pt grey `#595959`.
- Margins 0.6 inch; content left-aligned; nothing centered except a cover title.
- Colors come from `python "C:\Users\Administrator\.claude\skills\design\scripts\tokens.py" --style editorial` (`series`, `tokens.k-ink`, `tokens.k-muted`, `tokens.k-brand`); HTML decks use the kit tokens.

## Content
- The title is the conclusion as a full sentence ("中国出口额一年增长 49%"); the subtitle line gives measure, unit and period.
- One idea per slide. At most 5 bullets, each one line; prefer a chart, a big number or a statement over bullets.
- Key numbers large: 60–96pt alone on a big-number slide, 40–60pt beside other content, with a small label underneath.
- Charts follow `charts.md` (direct labels, 1–2 notes, source line). HTML: inline SVG; pptx: matplotlib PNG at dpi 200 or native charts in the series colors.
- Cover: title, one-line conclusion, date and author. No agenda or section dividers unless the deck has 12+ slides.
- End with a sources slide when the deck contains data. Label illustrative numbers 示例.
- No filler slides ("Thank you", "Q&A", a mission statement) unless I ask.

## HTML deck
Kit files: `E:\Claude\sites\_kit\deck\` (`deck.css`, `deck.js`, `deck_pdf.py`). Each slide is a 1920×1080 canvas scaled to the screen (letterboxed); page CSS inside a slide writes sizes as `calc(N * var(--u))`, N in canvas px (1pt = 2px).
```html
<html lang="zh-CN"><head>…viewport meta…
<link rel="stylesheet" href="kit/v1.css"><link rel="stylesheet" href="kit/styles/editorial.css">
<link rel="stylesheet" href="kit/deck/deck.css"><script src="kit/deck/deck.js"></script></head>
<body class="k k-deck">
<section class="k-slide k-slide--cover"><h1>标题</h1><p class="k-slide__lede">一句话结论</p><p class="k-slide__meta">作者 · 2026年10月</p></section>
<section class="k-slide"><h2 class="k-slide__title">结论句标题</h2><p class="k-slide__sub">度量，单位，时期</p>…<p class="k-slide__source">来源：…</p>
  <aside class="k-notes">讲稿（不显示）</aside></section>
```
| Layout | Class and parts |
|---|---|
| Cover | `k-slide--cover`: `h1`, `k-slide__lede`, `k-slide__meta` |
| Statement | `k-slide--statement`: `h2.k-slide__statement` (one sentence; break at the comma with `<br>`), optional `k-slide__lede` |
| Big number | `k-slide--number`: title, `k-bigs` > `k-big` (`k-big__value` with `k-big__unit`, `k-big__label`); two numbers side by side at most; source |
| Chart | `k-slide--chart`: title, sub, `figure.k-slide__figure` with an inline SVG `viewBox="0 0 1728 H" preserveAspectRatio="xMinYMin meet"` drawn in canvas px (classes `k-tick k-dlabel k-dlabel--on k-note k-leader k-axis-line k-grid-line`), source |
| Text | plain `k-slide`: title, `ul.k-slide__body` (≤5 one-line bullets) |
| Comparison | title, `k-cols` with two `div`s (`h3` + `ul`); `k-col--key` marks the side the title favours |
| Quote | `k-slide--quote`: `blockquote.k-slide__quote` > `p` + `footer` (real quotes only) |
| Section divider | `k-slide--section`: title, `k-slide__part`; decks of 12+ slides only |
| Sources | `k-slide--sources`: title, `ol.k-slide__sources` |

Behaviour: ←/→, PageUp/PageDown, Space, Home/End, click or tap the left/right half, swipe on phones; `#3` deep-links and Back/Forward step through slides; O or the grid button shows all slides as a list (two columns on desktop, one on phones). Portrait phones show the slide fitted to the width with the bar under it; small text has a 9–10px floor, chart text does not (keep chart labels ≥ 26 canvas px). Print gives one 16:9 page per slide.

Build and check:
1. `python "E:\Claude\sites\_kit\apply_kit.py" deck.html` (inlines kit and deck files; re-run after kit changes).
2. `python "E:\Claude\sites\_kit\deck\deck_pdf.py" deck.html --png all` → `deck.pdf` (fails if pages ≠ slides, i.e. a slide overflows) plus 1920×1080 PNGs in `deck-slides\`. Look at every PNG for overflow, tiny text and title positions that jump between slides.
3. `shoot.py deck.html --views desktop-light,iphone-light` for the screen and phone views, then the `review.md` scorecard.

## Check (pptx)
Render to images (the pptx skill's thumbnail/PDF route) and review them with the `review.md` scorecard. The usual failures are text overflow, alignment between slides and inconsistent title positions.
