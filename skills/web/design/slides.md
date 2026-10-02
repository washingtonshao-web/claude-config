# Slides

Technical work (python-pptx, templates, export) follows the pptx skill; HTML decks follow the slideshow skill. This file sets the look.

## Page
- 16:9, white background, a 4px falcon-copper `#b4531f` rule across the top of every slide with a short copper tab at the left (mirrors the web chart frame).
- Microsoft YaHei UI throughout; titles bold 28–32pt, body regular 16–20pt, source lines 10pt grey `#595959`.
- Margins 0.6 inch; content left-aligned; nothing centered except a cover title.
- Colors from `python "C:\Users\Administrator\.claude\skills\design\scripts\tokens.py" --style editorial` (`series`, `tokens.k-ink`, `tokens.k-muted`, `tokens.k-brand`).

## Content
- The title is the conclusion as a full sentence ("中国出口额一年增长 49%"); the subtitle line gives measure, unit and period.
- One idea per slide. At most 5 bullets, each one line; prefer a chart or table over bullets.
- Key numbers large (40–60pt) with a small label underneath, like web KPIs.
- Charts follow `charts.md` (direct labels, 1–2 notes, source line); export matplotlib charts at dpi 200 as PNG, or use native pptx charts styled with the series colors.
- Cover: title, one-line conclusion, date and author; optional one illustration per `images.md`.
- End with a sources slide when the deck contains data.

## Check
Render to images (the pptx skill's thumbnail or PDF route) and review them with the `review.md` scorecard: text overflow, alignment between slides, and consistent title positions are the usual failures.
