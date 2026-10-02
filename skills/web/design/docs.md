# Word and PDF documents

Technical work follows the docx and pdf skills. This file sets the look.

## Page and type
- A4, margins 2.2 cm; Microsoft YaHei UI for Chinese and Latin text (Segoe UI acceptable for Latin); body 10.5–11pt, line spacing 1.5; headings bold.
- Heading 1 16pt with a thin falcon-copper `#b4531f` rule under it; Heading 2 13pt; Heading 3 11pt bold. No more than 3 levels.
- Header: document title in 9pt grey; footer: page number and date.
- Colors from `python "C:\Users\Administrator\.claude\skills\design\scripts\tokens.py" --style editorial`.

## Structure
- Title, then a one-paragraph summary that states the conclusion and the 2–3 numbers behind it (a shaded box is fine).
- Numbered sections; each data claim near its chart or table.
- Sources at the end, numbered, matching in-text markers.

## Tables and figures
- Tables: header row bold with a 1pt ink rule under it, 0.5pt light rules between rows, no vertical lines, numbers right-aligned with thousands separators.
- Figures: matplotlib per `charts.md` at dpi 200, full text width; numbered caption "图 1 …" with the conclusion, then the source line in 9pt grey.

## Check
Convert to PDF and review page images with the `review.md` scorecard: widows, tables split across pages, and figure/caption separation are the usual failures.
