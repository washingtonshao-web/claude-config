# Showcase look

For pages made to enjoy, to show or to welcome. The standard is the set of pages I approved: open the screenshots listed in `shelf.md` before you design anything, and aim to sit beside them.

## 1. Name the world before any CSS
Write this as a comment at the top of the page's stylesheet, then build from it.
- **World:** five concrete things from the subject's own world (materials, objects, places, instruments, a period, a painting tradition).
- **Palette:** four to six colours taken from that world, each with where it comes from, including the ground, the ink and one accent. Body text still needs 4.5:1.
- **Signature:** the one thing a visitor will remember (the scene, a map texture, a title treatment, a movement). One. Everything around it stays quiet.
- **Test:** would this palette, typeface and layout have appeared whatever the subject was? If yes, start again.

## 2. The first screen is one scene
- One picture, scene or map fills the whole first screen on desktop and phone (`100svh`; minus a slim top bar if the site needs one): a real photograph for a real place or thing, a frame from the film for a film page, a painting in the subject's own tradition for history and story sites, the map itself for an atlas (`maps.md`). Images follow `images.md`.
- A slow cross-fade between three to six frames of the same world still counts as one scene. A carousel with arrows, dots or captions does not.
- The title sits over the scene in the display typeface, with at most one line under it and one way in (a button or a scroll cue). No statistics row, no wall of navigation, no cards over the picture. On an atlas, the search and two or three map controls may sit on the map; filters and lists go in one side panel (it may be open by default beside the map, as on the 高铁盈亏图谱) or behind one button.
- Keep the title zone clear: a soft gradient behind the title, and nothing interactive (markers, pins, labels) drawn under it. On a map, pad `fitBounds` on the title's side.
- Choose the phone crop on purpose: keep the focal point, and give the phone its own image or `object-position` if the desktop crop loses it.
- Text over a picture: measure contrast on the picture; if it falls short, darken or lighten only the area behind the text.
- A new site or a full redesign: put three different first screens in the one batch of questions my instructions allow at the start of a large task, with your default marked. When the task gives you no such batch (an unattended run, a brief that settles the scope), build your default and describe the other two directions in one line each at delivery. Never stop to ask later.

## 3. Type
- One display typeface for titles, chosen for the subject (a brush or 楷 face for a Chinese history piece, a grotesque for a racing game). Self-host it as a subset `woff2` that contains every character the titles use, with `font-display: swap` and a system fallback.
- The site title is big and confident: about `clamp(44px, 9vw, 112px)` on the cover, at least 40px on a phone. On an atlas whose first screen is the map, keep it to about `clamp(40px, 6vw, 80px)` so the map stays the subject. It is the one size allowed outside the kit scale; everything else stays on the scale.
- Check it: `shoot.py` must show the display face in `fonts` and no SimSun. When titles are data-driven (item names, places), build the subset from the data, not from the mock-up.
- Body text, lists, tables and controls stay in the kit's system sans, so long text reads the same everywhere. Never a second display face. No tracking or capitals on Chinese.
- A home or hub page may carry one line in the site's own voice (a motto, a greeting). Not more than one, and never on a report.

## 4. Below the first screen
- Keep the world: the same palette, textures and image style all the way down. Reuse the kit's mechanics (grid, search, chips, drawer, tabs) and re-skin them through the `--k-*` tokens; do not rewrite them and do not fall back to the white editorial page. A single-theme page sets its tokens on `:root` and repeats them under the kit's two dark-mode selectors (`kit-reference.md`).
- The site's own images (cover, banners, section illustrations) share one style. The items of a collection keep their own: film posters, paintings, photographs of objects or animals.
- Every screen carries something to look at (a picture, a map, the object itself), not paragraphs alone. Catalogs show real photographs of the actual thing.
- A tool or personal dashboard puts the working control and a real result on the first screen; the theme frames it and never hides it.
- Group with space, rules and the scene itself before reaching for cards. When cards are right (a catalog), give them one shape and one image ratio.
- A catalog leads with what a visitor knows and the best pictures: famous items and sharp, recognisable photographs first; specimen drawings, plant close-ups and obscure items later. A map cluster takes its cover from its best-known member.
- Pick each grid's columns from the number of items in that section, so no row ends with one lonely card or a half-empty line.
- Text under pictures and in lists stays readable on a dark theme: at least `--k-fs-sm` (14px), 4.5:1 against the ground, one line of description per card. Dim, tiny captions make a rich page look cheap.

## 5. Motion
- Controls answer within 150 ms; panels and drawers finish within 300 ms, eased out.
- The hero and the atmosphere may move freely when the movement belongs to the scene: a slow pan, parallax, a muted video loop, drifting mist. One orchestrated movement beats many small ones.
- Under `prefers-reduced-motion` everything rests on a complete still frame. The page must look finished without any animation having run.

## 6. Still banned here
Status and sync text, disclaimers, tool or model names, version stamps, counters for their own sake; mixed image styles on one site; emoji as icons; a generic grid of rounded cards as the first screen; decoration that belongs to some other subject.

## My hobby sites (decided 2026-11-08)
藏宝阁, 荐品, Objectarium 器物与玩具, 山茶花园 and 免提子 keep the identity I picked for each: its self-hosted display font, textured page, illustrated banner carrying the title only, and no dark mode where I removed it. The qc-site skill checks that their fonts load and cover every character.
