#!/usr/bin/env python3
"""Screenshot a page in desktop/mobile x light/dark, run measured checks, build one contact sheet.

Usage:
    python shoot.py <page.html | URL> [--out DIR] [--views desktop-light,mobile-dark] [--full] [--wait MS]

Look at contact.png first (about 1.6k tokens for all four views); open a single view only
to inspect a problem. Checks are measured, not eyeballed: horizontal overflow, elements past
the right edge, page/console errors, failed requests, broken images, low-contrast text,
small tap targets on phones, Microsoft YaHei used without a fallback.
Prints a JSON report; exit code 1 when a hard check fails (overflow, errors, broken images).
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

VIEWS = {
    "desktop-light": dict(viewport={"width": 1440, "height": 900}, color_scheme="light"),
    "desktop-dark": dict(viewport={"width": 1440, "height": 900}, color_scheme="dark"),
    "mobile-light": dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                         device_scale_factor=2, color_scheme="light"),
    "mobile-dark": dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                        device_scale_factor=2, color_scheme="dark"),
}

CHECKS_JS = r"""
(isMobile) => {
  const de = document.documentElement, vw = de.clientWidth;
  const out = {overflowX: de.scrollWidth - vw, pastEdge: [], brokenImages: [], lowContrast: [], lowContrastCount: 0, smallTargets: 0, fontWarning: null};
  const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : '');
  const visible = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const clipped = el => { for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
    const s = getComputedStyle(p); if (/(auto|scroll|hidden|clip)/.test(s.overflowX)) return true; } return false; };
  for (const el of document.body.querySelectorAll('*')) {
    if (!visible(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 && !clipped(el) && out.pastEdge.length < 5) out.pastEdge.push(`${name(el)} right=${Math.round(r.right)}`);
  }
  for (const img of document.images) if (img.complete && img.naturalWidth === 0 && img.getAttribute('src')) out.brokenImages.push(img.getAttribute('src').slice(0, 80));
  const rgb = c => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : [0, 0, 0, 1]; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const bgOf = el => { for (let p = el; p; p = p.parentElement) { const s = getComputedStyle(p);
    if (s.backgroundImage !== 'none') return null; const c = rgb(s.backgroundColor); if ((c[3] ?? 1) > 0.5) return c; }
    return rgb(getComputedStyle(document.body).backgroundColor); };
  let n = 0;
  for (const el of document.body.querySelectorAll('h1,h2,h3,h4,p,li,td,th,a,span,button,label,figcaption,small,div')) {
    if (n > 600) break;
    if (![...el.childNodes].some(t => t.nodeType === 3 && t.textContent.trim())) continue;
    if (!visible(el)) continue; n++;
    const s = getComputedStyle(el), bg = bgOf(el); if (!bg) continue;
    const fg = rgb(s.color), a = fg[3] ?? 1, mix = fg.slice(0, 3).map((v, i) => v * a + bg[i] * (1 - a));
    const L1 = lum(mix), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const big = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.66 && +s.fontWeight >= 700);
    if (ratio < (big ? 3 : 4.5) && out.lowContrastCount++ < 3)
      out.lowContrast.push(`${name(el)} ${ratio.toFixed(2)} "${el.textContent.trim().slice(0, 24)}"`);
  }
  if (isMobile) for (const el of document.querySelectorAll('a,button,input,select,[role=button]')) {
    if (!visible(el)) continue; const r = el.getBoundingClientRect();
    if ((r.width < 32 || r.height < 32) && !(el.tagName === 'A' && el.closest('p,li,td,figcaption'))) out.smallTargets++;
  }
  const ff = getComputedStyle(document.body).fontFamily;
  if (/^["']?Microsoft YaHei/i.test(ff) && !/PingFang|Noto Sans|sans-serif/i.test(ff)) out.fontWarning = ff;
  return out;
}
"""


def contact_sheet(shots: dict[str, Path], dest: Path) -> None:
    tiles = []
    for name, p in shots.items():
        im = Image.open(p).convert("RGB")
        w = 760 if name.startswith("desktop") else 300
        h = min(int(im.height * w / im.width), 1100 if name.startswith("desktop") else 650)
        im = im.resize((w, int(im.height * w / im.width))).crop((0, 0, w, h))
        tiles.append((name, im))
    desk = [t for t in tiles if t[0].startswith("desktop")]
    mob = [t for t in tiles if t[0].startswith("mobile")]
    gap, label = 16, 22
    row1_h = max((im.height for _, im in desk), default=0)
    row2_h = max((im.height for _, im in mob), default=0)
    width = max(sum(im.width for _, im in desk) + gap * (len(desk) + 1),
                sum(im.width for _, im in mob) + gap * (len(mob) + 1), 400)
    height = (row1_h + label + gap if desk else 0) + (row2_h + label + gap if mob else 0) + gap
    sheet = Image.new("RGB", (width, height), (128, 128, 128))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    y = gap
    for row, rh in ((desk, row1_h), (mob, row2_h)):
        if not row:
            continue
        x = gap
        for name, im in row:
            draw.text((x, y), name, fill=(255, 255, 255), font=font)
            sheet.paste(im, (x, y + label))
            x += im.width + gap
        y += rh + label + gap
    sheet.save(dest)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out")
    ap.add_argument("--views", default=",".join(VIEWS))
    ap.add_argument("--full", action="store_true", help="full-page screenshots instead of the first screen")
    ap.add_argument("--wait", type=int, default=800, help="ms to wait after load for charts and fonts")
    a = ap.parse_args()

    t = a.target
    url = t if t.startswith(("http://", "https://", "file:")) else Path(t).resolve().as_uri()
    stem = Path(t).stem if not t.startswith("http") else t.split("//")[1].split("/")[0]
    temp = Path(r"E:\AI\Claude\temp") if Path("E:\\").exists() else Path(r"D:\AI\Claude\temp")  # PCs without E: use D:
    out = Path(a.out) if a.out else temp / "shoot" / f"{stem}-{datetime.datetime.now():%m%d-%H%M%S}"
    out.mkdir(parents=True, exist_ok=True)

    report, shots, hard = {"url": url, "out": str(out), "views": {}}, {}, False
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            browser = p.chromium.launch()
        for name in [v.strip() for v in a.views.split(",") if v.strip()]:
            ctx = browser.new_context(**VIEWS[name])
            page = ctx.new_page()
            errors, failed = [], []
            page.on("pageerror", lambda e: errors.append(str(e)[:160]))
            page.on("console", lambda m: m.type == "error" and errors.append("console: " + m.text[:160]))
            page.on("requestfailed", lambda r: failed.append(r.url[:120]))
            page.on("response", lambda r: r.status >= 400 and failed.append(f"{r.status} {r.url[:110]}"))
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(a.wait)
            res = page.evaluate(CHECKS_JS, name.startswith("mobile"))
            shot = out / f"{name}.png"
            page.screenshot(path=str(shot), full_page=a.full)
            shots[name] = shot
            res.update(errors=errors[:5], failedRequests=failed[:5])
            res = {k: v for k, v in res.items() if v not in ([], 0, None)}
            res["hardFail"] = bool(res.get("overflowX", 0) > 0 or errors or res.get("brokenImages"))
            hard |= res["hardFail"]
            same = next((k for k, v in report["views"].items() if v == res), None)
            report["views"][name] = f"same findings as {same}" if same else res
            ctx.close()
        browser.close()
    contact_sheet(shots, out / "contact.png")
    report["contact"] = str(out / "contact.png")
    report["pass"] = not hard
    print(json.dumps(report, ensure_ascii=False, indent=1))
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
