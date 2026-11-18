# Review before delivery

Three parts, in this order: measured checks, things only eyes can check, then a verdict in plain words. Two rounds at most.

## 1. Measured checks (pass or fail)
```
python scripts/shoot.py <page.html | URL> --look report|showcase|tool [--full] [--views desktop-light,iphone-light] [--log <site folder>]
```
(`scripts/` is the folder beside this file.)
- Default views: 1440×900 desktop (system Chrome) and iPhone 18 Pro Max (WebKit, Safari's engine; 440×760 visible, 3×, touch), each light and dark, first screen only, plus `small-light` (375×667), measured but kept off the contact sheet. `--full` shoots whole pages; a single-theme page shows the same image in light and dark.
- Output: `E:\AI\Claude\temp\shoot\<name>-<time>\` with one PNG per view and `contact.png`. A row is appended to `design-log.csv` beside the page (use `--log` for a URL), so the record keeps itself.
- Hard failures (exit code 1), all to be fixed:
  - horizontal overflow, missing viewport meta, page or console errors, broken images;
  - SimSun or another fallback face in the rendered `fonts`;
  - `floor.fails`, the first-screen floor for the look: a report with a headline over 28 Chinese characters or 14 English words, or with no chart, map, figure or key number on the first screen; a showcase whose first screen is not carried by a picture, scene or map (50% of the screen); a tool with no working control on the first screen.
- Reported, to be fixed or justified in one line each: low-contrast text, phone tap targets under 44px, inputs under 16px, `floor.restraint` (stamps, counters, disclaimers, tool names), `floor.warn` (too many text sizes), three or more font families, and under the report look the `aiTells` (gradient text, tracked capitals, eyebrows, numbered labels without a reason, side stripes, emoji icons).
- A protected live URL reports `"gated": true`: rerun with `--login`, or shoot the local build. A page with its own PIN: `--storage KEY=VALUE`.

## 2. What a script cannot see
- **Open `contact.png` and confirm each view shows what its name says**: the real page, loaded, not a lock screen, a spinner or a blank frame. Then look at it as the reader would.
- **Click test, on every page that has a control** (maps, catalogs, tools, decision pages, Artifacts with buttons). A static report whose only controls are links, a TOC and tooltips: check that the TOC and anchors jump without breaking Back, and that tooltips open on tap; nothing more. With Playwright at 1440×900 and 440×760: click three representative targets, one with a cold cache and two in quick succession. After each click `scrollY` is unchanged and something visible responds within 150 ms; screenshots at 50, 150 and 300 ms show no white frame; browser Back closes the panel or goes up a level and Forward works; at 200% zoom (720×450 at scale 2) controls are larger and not clipped. One line per result.
- **Checklist** (one line each, yes or the fix): nothing from the Restraint list; chart rules in `charts.md` met, sources present; images sharp, one style, right subject (`images.md`); nothing told apart by colour alone; on a revision, no link, field or heading lost.

## 3. The verdict (anything published, shared or delivered as finished)
An independent model judges the look in plain words. In Claude that is GPT-6.2 Astra through the codex-gpt command, with the screenshots attached; if Astra is unavailable, a fresh Claude Fable 5.2 high-effort agent, labelled `Fable 复核（非 Astra）`. Private drafts, quick answers in chat, and runs where the brief rules out an outside reviewer: answer the same questions yourself and log the verdict as `self`.

Give the reviewer:
- the contact sheet, plus the desktop and iPhone views;
- for a showcase page, two pages from `shelf.md` of the nearest kind; for a report, the page's own chart at full size;
- the page's purpose, reader and look in two lines. Do not give it the script output before it answers.

Ask exactly this, and nothing about points:
1. For a showcase: of these three pages, which looks weakest and why? For a report: can you state the finding and its evidence from the first screen alone?
2. Would the owner call this page 好看 for its purpose, or would they call it plain, empty, cluttered or ugly? Say which, and where.
3. The three worst things about how it looks, most important first, each with the fix.
4. One word: ship, fix or rebuild.

Then:
- **ship:** deliver. **fix:** make the named fixes, re-shoot only the affected views, and ask once more. **rebuild:** the direction is wrong; start the first screen again (for a showcase, from another of the three directions).
- After the second round, deliver with what is still open stated plainly. Do not ask a third time.
- Record it: `python scripts/shoot.py <page> --look <look> --verdict "<reviewer>: <ship|fix|rebuild>; worst: <one phrase>"`.
- Tell me the result in one line of plain words, with no scores: who reviewed, the verdict, and the worst remaining weakness.
