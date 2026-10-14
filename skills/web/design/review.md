# Visual review

Inspect the rendered result separately from functionality, before every delivery.

## 1. Shoot and measure
```
python "C:\Users\Administrator\.claude\skills\design\scripts\shoot.py" <page.html | URL> [--full] [--views desktop-light,iphone-light]
```
- Default views: 1440×900 desktop (system Chrome) and iPhone 18 Pro Max (WebKit, Safari's engine; 440×760 visible, 3×, touch), each light and dark, first screen only. Plus `small-light` (375×667), which is measured but kept off the contact sheet. `--full` shoots whole pages; on long pages review the first screens, then run `--full` once at the end.
- Uses Python Playwright, so it works while the browser pane is hidden. An Artifact fragment (no doctype) is shot inside the skeleton the Artifact publisher adds.
- A protected live URL reports `"gated": true` (Falconshire login). Shoot the local build instead, or serve the release over SSH (see `maps.md`).
- A page with its own PIN or lock screen: pass the value the page itself stores after unlocking with `--storage KEY=VALUE` (repeatable; written to localStorage before load), so the real page is shot instead of the lock card.
- Output folder: `E:\AI\Claude\temp\shoot\<name>-<time>\`, with one PNG per view plus `contact.png` (all views on one sheet).
- The JSON report is measured, not eyeballed:
  - horizontal overflow and elements past the right edge;
  - page and console errors, failed requests, broken images;
  - low-contrast text (with its ratio);
  - phone tap targets under 44px, phone inputs under 16px, missing viewport meta;
  - **`fonts`**: the faces Chromium actually rendered, with their share. Look for `badFonts` (SimSun etc.), `mixedFonts` (three or more families) and `heavyWeights` (900 weights next to CJK bold).
- Exit code 1 on a hard failure: overflow, missing viewport meta, errors, broken images, or SimSun.
- Views with identical findings are folded ("same findings as …"). A deliberately single-theme style shows the same image in light and dark; that is expected.

## 2. Click test (maps, catalogs, tools, anything with panels)
Use Playwright at 1440×900 and 440×760:
- Click three representative targets, including one with a cold cache and two clicked in quick succession.
- After each click, check that `scrollY` is unchanged and that something visible responds within 150 ms (a panel shell is fine; data fills within 1 s).
- Take screenshots at 50, 150 and 300 ms, so a white or blank frame shows up.
- Check Back and Forward: browser back closes the panel or goes up one level, and restores the region, selection and viewport.
- At 200% browser zoom (emulate it with a 720×450 viewport at device scale 2), labels and controls are larger, usable and not clipped.

Report each result as one line, and give these lines to the reviewer.

## 3. Look
Open `contact.png` first (about 1.6k tokens for four views). Open a single view, or crop a region, only to inspect a specific problem. Do not re-shoot views you did not change.

## 4. Score (24 points; deliver at 80% of the applicable points with no item at 0)
Items that don't apply (for example interaction on a static document) are marked n/a and left out of the total.
| # | Item | 2 | 1 | 0 |
|---|---|---|---|---|
| 1 | Conclusion first | Finding (or the map) readable in the first screen | Present but below the fold | Topic headline only |
| 2 | Hierarchy | One clear entry point per screen | Two competing | Flat wall |
| 3 | Typography | Kit fonts only (measured), sizes, measure, Chinese spacing | Minor slips | SimSun, mixed fonts, uneven weights or cramped text |
| 4 | Color | One accent; status colors only for status | One stray color | Rainbow or decorative status colors |
| 5 | Charts and maps | `charts.md` / `maps.md` rules met, sources present | One rule missed | Legend hunting, no boundaries, no source |
| 6 | Spacing and alignment | Consistent rhythm and edges | A few uneven gaps | Visibly misaligned, stray boxes |
| 7 | Phone (iPhone view) | No overflow, conclusion in first screen, targets OK | Minor crowding | Overflow or unreadable |
| 8 | Interaction feel | Click test clean: no jumps, Back works, no white flash, fast | One slip | Page jumps, no way back, or blank frames |
| 9 | Restraint | Nothing from the Restraint list in SKILL.md | One instance | Several |
| 10 | Images | Consistent style, sharp, no layout jump | One weak image | Stretched, blurry or missing |
| 11 | AI look | None of the "Avoid" list in SKILL.md | One instance | Several |
| 12 | Theme and contrast | Dark mode (or the chosen single theme) clean, contrast passes | Small slips | Broken or unreadable |

## 5. Who scores
- **Private drafts and quick answers in chat:** score it yourself, one line per item.
- **Anything published, shared or delivered as finished work:** GPT-6 Astra scores it independently from the screenshots. Run the codex-gpt command with images attached, for example:
  ```
  "$C" exec -m gpt-6-astra -c model_reasoning_effort=high --skip-git-repo-check --ephemeral -s read-only -C <dir> -i <contact.png> -i <desktop-light.png> -i <iphone-light.png> -o <scratchpad>/astra-review.txt "<prompt>" </dev/null
  ```
  In the prompt, include the scorecard above, the Restraint and Avoid lists from SKILL.md, the page's purpose, the shoot.py JSON and the click-test lines. Ask for a score per item, the three most important fixes, and nothing else.
- If Astra is unavailable, use a fresh Opus 5.5 high-effort subagent with the same inputs, and label it 同模型复核.
- Fix every 0. Fix every 1 on items 3, 5, 8 and 9 (fonts, charts and maps, interaction, restraint), the complaints that keep coming back. Fix other 1s when it's cheap. Re-shoot only the affected views and re-score those items. Report the final score and the reviewer in one line.
