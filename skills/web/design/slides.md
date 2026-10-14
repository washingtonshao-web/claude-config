# Slides

## Route
| Request | Build with |
|---|---|
| A deck, with no file format named | The Artifact **Slides** type (Artifact `quickstart`, intent `slides`) with the design system **Falconshire Editorial** (https://claude.ai/artifact/24eZ3vxVomaArgKq7SY8K2). It downloads as .pptx or PDF when someone needs a file |
| A .pptx/.potx is named, supplied or must be edited | The pptx skill; this file sets the look |
| An animated or video-style deck | HyperFrames, only when I ask for animation |

The pptx skill's "safe font" list does not apply: headings are Microsoft YaHei UI Bold and body text Microsoft YaHei UI. Leave about 10% slack in text boxes, because LibreOffice QA may substitute the font.

## Page
- 16:9 and a white background. Every slide has a 4px falcon-copper `#b4531f` rule across the top, with a short copper tab at the left (mirrors the web chart frame).
- Microsoft YaHei UI throughout; titles bold 28–32pt, body regular 16–20pt, source lines 10pt grey `#595959`.
- Margins 0.6 inch; content left-aligned; nothing centered except a cover title.
- Colors come from `python "C:\Users\Administrator\.claude\skills\design\scripts\tokens.py" --style editorial` (`series`, `tokens.k-ink`, `tokens.k-muted`, `tokens.k-brand`).

## Content
- The title is the conclusion as a full sentence ("中国出口额一年增长 49%"); the subtitle line gives measure, unit and period.
- One idea per slide. At most 5 bullets, each one line; prefer a chart or table over bullets.
- Key numbers large (40–60pt) with a small label underneath, like web KPIs.
- Charts follow `charts.md` (direct labels, 1–2 notes, source line). Export matplotlib charts at dpi 200 as PNG, or use native pptx charts styled with the series colors.
- Cover: title, one-line conclusion, date and author; optionally one illustration per `images.md`. No agenda slide unless the deck has 12+ slides.
- End with a sources slide when the deck contains data.
- No filler slides ("Thank you", "Q&A", a mission statement) unless I ask.

## Check
Render to images (the Slides page in shoot.py, or the pptx skill's thumbnail/PDF route) and review them with the `review.md` scorecard. The usual failures are text overflow, alignment between slides and inconsistent title positions.
