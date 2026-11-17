# Images

## By look
| Look | Images |
|---|---|
| Report | No hero. Open with headline, verdict and the key chart. Optional: a slim illustration band (21:6) or a small spot illustration beside the headline, as flat editorial illustration in the house palette. Never a photorealistic or cinematic picture next to flat charts |
| Showcase | One full-screen scene opens the page (`showcase.md`). Choose **one image style for the whole site** and keep to it: real photographs, paintings in the subject's own tradition, or cinematic renders. Never two of these on one site |
| Catalogs and 图鉴 | Real photographs of the actual thing for every item, one aspect ratio, no generated stand-ins for real objects or animals |
| Slides | Cover may carry one illustration; content slides use charts |

## Choosing the style (showcase)
- A real place, a real object, a real trip: real photographs first. Documentary, natural light, no heavy filter. Credit the source small at the edge.
- A film page: frames from the films themselves.
- History, myth, culture, language: a painting in that subject's tradition (水墨, 青绿山水, 浮世绘, fresco, miniature). Name the tradition in the prompt.
- A game or an imagined world: a cinematic scene, one lighting mood for the whole site.
- An atlas: the map is the image (`maps.md`).

## Full-screen cover
The picture fills the whole first screen on desktop and phone (100svh, minus a slim bar if one sits above it). Title and at most one line over it; contrast at least 4.5:1 measured on the picture behind the text, with a local gradient behind the text only if needed. Give the phone its own crop or `object-position` so the focal point stays in view. Content starts on the second screen.

Sharpness: the cover source is about 1920px wide (at least 1600px) and the phone crop at least 1100px tall. When the only source is smaller (a 960px film frame), enlarge it through the image route ("upscale this frame to 1920×1080; keep every shape, colour and figure exactly as they are"; the route may return about 1670px, which is enough) and look at the result at 100% before using it. Never show a picture larger than 1.5× its own pixels.

## Generated images
- Generate 2–3 options with the same prompt skeleton, **open each at full size**, and pick one. Check it against the subject before using it: the right animal, the right building, the right period, the right number of fingers. A falcon that came out as an eagle is a wrong picture.
- No text or logos inside the image. Leave calm space where the title will sit.
- Keep the prompt skeleton for every image on the site so they share a style.
- Report illustration template (codex-gpt skill):
```
Flat editorial illustration for a data article about <subject>. <one concrete scene>.
Limited palette: deep blue #006ba2, cyan #3ebcd2, teal #379a8b, mustard #ebb434, one copper accent #b4531f,
on an off-white background. Simple geometric shapes, subtle paper grain, clean vector look, no gradients,
no text, no logos, not photorealistic. Wide <21:9 | 21:6 | 4:3> composition with calm empty space on the <left|right>.
```
- Showcase scene template:
```
<Tradition or medium, e.g. "Chinese blue-green landscape painting on silk" | "cinematic night photograph">: <one concrete scene from the subject's world>.
<The site's palette in words>. One clear focal point on the <left|right> third, calm open space on the other side for a title.
No text, no logos, no borders. <16:9 for desktop | 9:16 for the phone crop>.
```

## Files
- WebP (or JPEG) under ~300 KB for a cover at ~1920px, ~160 KB for the phone crop (about 630×1120); thumbnails under 40 KB.
- Fixed aspect-ratio boxes so the layout never jumps; `loading="lazy"` below the first screen, never on the cover.
- Store with the site or as Artifact assets; never hotlink Wikimedia or other third-party hosts. Exception: a catalog whose data already points at thousands of item photos on their source (for example Wikimedia thumbnails in 环球生灵图鉴) keeps those links, loads them lazily and shows a neutral placeholder when one fails. Covers and the site's own images are always stored with the site.
- Caption generated images 示意图（AI 生成） only where a reader could mistake them for a record of something real (a report illustration, a historical scene presented as fact). A cover painting for a story site needs no caption.
