# Visual review

Inspect the rendered result separately from functionality, before every delivery.

## 1. Shoot and measure
```
python "C:\Users\Administrator\.claude\skills\design\scripts\shoot.py" <page.html | URL> [--full] [--views desktop-light,mobile-light]
```
- Default: 1440×900 desktop (system Chrome) and iPhone 18 Pro Max (WebKit, Safari's engine; 440×760 visible, 3×, touch), each light and dark, first screen only; plus `small-light` (375×667), measured only and kept off the contact sheet. `--full` for whole pages (long pages: review the first screens, then `--full` once at the end).
- Python Playwright, so it works while the browser pane is hidden. An Artifact fragment (no doctype) is shot inside the skeleton the Artifact publisher adds.
- A protected live URL reports `"gated": true` (Falconshire login); shoot the local build instead, which the release verified as identical.
- Output folder `E:\AI\Claude\temp\shoot\<name>-<time>\`: one PNG per view plus `contact.png` (all views on one sheet).
- The JSON report is measured, not eyeballed: horizontal overflow, elements past the right edge, page and console errors, failed requests, broken images, low-contrast text (with ratio), phone tap targets under 44px, phone inputs under 16px, missing viewport meta, YaHei-only font stacks. Exit code 1 on a hard failure (overflow, missing viewport meta, errors, broken images).
- Views with identical findings are folded ("same findings as …"). A deliberately single-theme style shows the same image in light and dark; that is expected.

## 2. Look
Open `contact.png` first (about 1.6k tokens for four views). Open a single view, or crop a region, only to inspect a specific problem. Do not re-shoot views you did not change.

## 3. Score (20 points; deliver at 16+ with no item at 0)
| # | Item | 2 | 1 | 0 |
|---|---|---|---|---|
| 1 | Conclusion first | Finding readable in the first screen | Present but below the fold | Topic headline only |
| 2 | Hierarchy | One clear entry point per screen | Two competing | Flat wall |
| 3 | Typography | Kit sizes, measure, line-height, Chinese spacing | Minor slips | Mixed fonts or cramped text |
| 4 | Color | One accent; status colors only for status | One stray color | Rainbow or decorative status colors |
| 5 | Charts | `charts.md` rules met, source lines present | One rule missed | Legend hunting, dual axes, no source |
| 6 | Spacing and alignment | Consistent rhythm and edges | A few uneven gaps | Visibly misaligned |
| 7 | Phone (iPhone view) | No overflow, conclusion in first screen, targets OK | Minor crowding | Overflow or unreadable |
| 8 | Dark mode (or chosen single theme) | Both clean | Small contrast slips | Broken or unreadable |
| 9 | Images | Consistent style, sharp, no layout jump | One weak image | Stretched, blurry or missing |
| 10 | AI look | None of the "Avoid" list in SKILL.md | One instance | Several |

Report the score and the fixes in one line each; fix what scores 0 or 1, re-shoot only the affected views.
