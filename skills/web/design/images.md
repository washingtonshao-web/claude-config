# Images

## When to use a big image
| Content | Lead image |
|---|---|
| Travel, places, lifestyle, food | Big hero (21:9 desktop, 4:3 phone). Real photos of the real place first; illustration if none are usable |
| Data reports, briefs, atlases | No hero. Open with headline, conclusion and the key chart. Optional slim illustration band (21:6) or a small spot illustration beside the headline |
| Catalogs and encyclopedias | Thumbnails per item (real photos of the actual thing), no hero |
| Slides | Cover may carry one illustration; content slides use charts, not pictures |

## Style
- One style per deliverable. Default: **flat editorial illustration** in the house palette, matching the charts. Never photorealistic AI renders: they clash with flat charts and read as fake.
- Palette for prompts: editorial blue `#006ba2`, cyan `#3ebcd2`, teal `#379a8b`, yellow `#ebb434`, falcon copper `#b4531f` as the one warm accent, on a white or very light warm-grey ground; ink `#0d0d0d` for outlines if any.
- Composition: one clear subject, generous empty space where text or the crop may land, no text or logos inside the image, no lens flare, no dramatic sunset lighting.
- Real photos: documentary, natural light, no heavy filters; crop to the same aspect ratios as above. Credit the source in the caption.

## GPT image prompt template (codex-gpt skill)
```
Flat editorial illustration for a data article about <subject>. <one concrete scene>.
Limited palette: deep blue #006ba2, cyan #3ebcd2, teal #379a8b, mustard #ebb434, one copper accent #b4531f,
on an off-white background. Simple geometric shapes, subtle paper grain, clean vector look, no gradients,
no text, no logos, not photorealistic. Wide <21:9 | 21:6 | 4:3> composition with calm empty space on the <left|right>.
```
Generate 2–3 options, pick one, and keep the same prompt skeleton for every image in the deliverable.

## Files
- WebP (or JPEG) under ~300 KB; provide a ~1600px desktop and ~800px phone version for heroes.
- Fixed aspect-ratio boxes so the layout never jumps; `loading="lazy"` below the first screen.
- Store with the site or as Artifact assets; never hotlink Wikimedia or other third-party hosts.
- Caption AI images as 示意图（AI 生成）.
