#!/usr/bin/env python3
"""Screenshot a page in desktop and iPhone x light/dark (plus a small-phone check), run measured checks, build one contact sheet.

Usage:
    python shoot.py <page.html | URL> [--out DIR] [--views desktop-light,iphone-dark] [--full] [--wait MS]
                    [--storage KEY=VALUE ...]   # localStorage set before the page loads (e.g. a site's own PIN unlock)
                    [--login]                   # live password-protected *.falconshire.com page: reuse the saved login

Look at contact.png first (about 1.6k tokens for all four views); open a single view only
to inspect a problem. Checks are measured, not eyeballed: horizontal overflow, elements past
the right edge, page/console errors, failed requests, broken images, low-contrast text,
tap targets under 44px and inputs under 16px on phones, Microsoft YaHei used without a fallback, and the fonts
Chromium actually rendered (any SimSun/宋体 fallback is a hard failure; three or more text faces is flagged).
Phone views run in WebKit (Safari's engine) at iPhone 18 Pro Max size; "gated" means the URL
redirected to the Falconshire login: rerun with --login (cookies from ~/.claude/playwright-profile; close the
Playwright browser first), or shoot the local build.
AI tells are warnings under "aiTells" (never a hard failure): gradient text, tracked caps, eyebrows, 01/02 labels, side stripes, flat type scale, gray on color, em-dash density, emoji icons, >3 card radii.
Prints a JSON report; exit code 1 when a hard check fails (overflow, errors, broken images).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

# Some sessions point PLAYWRIGHT_BROWSERS_PATH at an empty temp dir; use the installed browsers instead.
_pw = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
_home = Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"
if _pw and not any(Path(_pw).glob("webkit-*")) and any(_home.glob("webkit-*")):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(_home)

# iphone-*: iPhone 18 Pro Max in Safari (WebKit engine), 440x956 pt screen at 3x, ~440x760 visible
# below the browser bars, so the screenshot is the real first screen. small-*: 375x667 (iPhone SE,
# small Android) - measured checks only, kept off the contact sheet.
IOS_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 "
          "(KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1")
IPHONE = dict(viewport={"width": 440, "height": 760}, screen={"width": 440, "height": 956},
              device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=IOS_UA)
SMALL = dict(viewport={"width": 375, "height": 667}, device_scale_factor=2, is_mobile=True, has_touch=True)
VIEWS = {
    "desktop-light": ("chromium", dict(viewport={"width": 1440, "height": 900}, color_scheme="light")),
    "desktop-dark": ("chromium", dict(viewport={"width": 1440, "height": 900}, color_scheme="dark")),
    "iphone-light": ("webkit", dict(IPHONE, color_scheme="light")),
    "iphone-dark": ("webkit", dict(IPHONE, color_scheme="dark")),
    "small-light": ("chromium", dict(SMALL, color_scheme="light")),
}

CHECKS_JS = r"""
(isMobile) => {
  const de = document.documentElement, vw = de.clientWidth;
  const out = {overflowX: de.scrollWidth - vw, pastEdge: [], brokenImages: [], lowContrast: [], lowContrastCount: 0, smallTargets: 0, smallInputs: 0, fontWarning: null};
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
    return [255, 255, 255]; };  // nothing painted: browser default white
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
    if ((r.width < 44 || r.height < 44) && !(el.tagName === 'A' && el.closest('p,li,td,figcaption'))) out.smallTargets++;
  }
  if (isMobile) for (const el of document.querySelectorAll('input,select,textarea'))
    if (visible(el) && parseFloat(getComputedStyle(el).fontSize) < 16) out.smallInputs++;  // iOS zooms on focus
  if (isMobile && !document.querySelector('meta[name=viewport]')) out.noViewportMeta = true;  // iPhone lays out at 980px
  const ff = getComputedStyle(document.body).fontFamily;
  if (/^["']?Microsoft YaHei/i.test(ff) && !/PingFang|Noto Sans|sans-serif/i.test(ff)) out.fontWarning = ff;
  return out;
}
"""

# "AI tells": devices the community design skills flag as the generated look. Warnings only (never hardFail);
# rule ids are from pbakaus/impeccable (detector), Nutlope/hallmark (slop-test gates), Leonxlnx/taste-skill (tells.md).
AI_TELLS_JS = r"""
() => {
  const out = {};
  const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : '');
  const visible = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const rgb = c => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : [0, 0, 0, 1]; };
  const spread = c => Math.max(c[0], c[1], c[2]) - Math.min(c[0], c[1], c[2]);
  const px = v => parseFloat(v) || 0;
  const snip = el => '"' + el.textContent.trim().replace(/\s+/g, ' ').slice(0, 24) + '"';
  const own = el => [...el.childNodes].filter(t => t.nodeType === 3).map(t => t.textContent).join('').trim();
  const CJK = /[\u3400-\u9fff\uf900-\ufaff]/;
  const texts = [...document.body.querySelectorAll('*')].filter(el => own(el) && !el.closest('svg,script,style,pre,code') && visible(el)).slice(0, 1500);

  // gradient-text (impeccable gradient-text; hallmark gate 2: "No genre allows gradient text")
  const grad = [...document.body.querySelectorAll('*')].filter(el => { const s = getComputedStyle(el);
    return /text/.test(s.webkitBackgroundClip || s.backgroundClip || '') && /gradient/.test(s.backgroundImage) && el.textContent.trim() && visible(el); });
  if (grad.length) out.gradientText = grad.slice(0, 3).map(el => `${name(el)} ${snip(el)}`);

  // tracked caps on short labels: uppercase + letter-spacing >= 0.08em, <= 40 chars (impeccable hero-eyebrow-chip
  // HERO_EYEBROW_TRACKING_EM = 0.08; taste-skill micro-label: tiny tracked capitals on 16% of top sites vs 57% of weak ones)
  const caps = texts.filter(el => { const s = getComputedStyle(el), t = el.textContent.trim();
    const upper = s.textTransform === 'uppercase' || (/[A-Z]{2}/.test(t) && !/[a-z]/.test(t));
    return upper && t.length <= 40 && px(s.letterSpacing) / px(s.fontSize) >= 0.08; });
  if (caps.length) out.trackedCaps = caps.slice(0, 4).map(el => `${name(el)} ${(px(getComputedStyle(el).letterSpacing) / px(getComputedStyle(el).fontSize)).toFixed(2)}em `
    + snip(el) + (CJK.test(el.textContent) ? ' (Chinese: house rule says no tracking)' : ''));

  // eyebrow / kicker: a small short label as its own block above (or beside) a heading.
  // Label ceiling max(14px, min(16px, 0.45 x heading)), 2-34 chars, heading >= 1.3 x label (impeccable kicker-above-heading,
  // label_size_ceiling); beside counts too (hallmark gate 54 "tag-left / header-right"). Flag at >= 60% of h2/h3.
  const labelOf = h => { const hs = px(getComputedStyle(h).fontSize), hr = h.getBoundingClientRect();
    const c = h.previousElementSibling || (h.parentElement && h.parentElement.firstElementChild === h ? h.parentElement.previousElementSibling : null);
    if (!c || !visible(c) || /^H[1-6]$/.test(c.tagName) || c.querySelector('h1,h2,h3,h4,h5,h6,img,svg,canvas,table,ul,ol,p')) return null;
    const t = c.textContent.trim(), fs = px(getComputedStyle(c).fontSize), r = c.getBoundingClientRect();
    if (t.length < 2 || t.length > (h.tagName === 'H1' ? 60 : 34) || fs > Math.max(14, Math.min(16, hs * 0.45)) || hs < fs * 1.3) return null;
    const pos = r.bottom <= hr.top + 4 && hr.top - r.bottom <= Math.max(72, hs * 1.1) ? 'above' : (r.right <= hr.left + 4 && r.bottom > hr.top ? 'beside' : null);
    return pos && {el: c, pos, t};
  };
  const heads = [...document.querySelectorAll('h2,h3')].filter(visible), kick = heads.map(labelOf).filter(Boolean);
  const h1 = [...document.querySelectorAll('h1')].find(visible), heroKick = h1 && labelOf(h1);
  const most = heads.length >= 2 && kick.length / heads.length >= 0.6;
  if (most || heroKick) out.eyebrow = most ? {headings: `${kick.length}/${heads.length} h2/h3 have one`,
    samples: kick.slice(0, 3).map(k => `${k.pos} ${name(k.el)} "${k.t.slice(0, 20)}"`)} : {};
  if (heroKick) out.eyebrow.hero = `${heroKick.pos} h1: "${heroKick.t.slice(0, 30)}"`;  // impeccable hero-eyebrow-chip

  // numbered section labels 01 / 02 / "01 · Features" - flag only (impeccable numbered-section-labels: >= 2 distinct;
  // hallmark "Eyebrow on every section"; taste-skill measured index numbering on 38% of top vs 21% of weak sites)
  const nums = texts.filter(el => !el.closest('td,th,ol,time') && el.textContent.trim().length <= 40 &&
    (/^[(\[#]?0\d{1,2}[)\].:\/]?$/.test(el.textContent.trim()) || /^0\d\s*[·\/.:|—–-]\s*\S/.test(el.textContent.trim())));
  const distinct = new Set(nums.map(el => el.textContent.trim().slice(0, 2)));
  if (distinct.size >= 2) out.numberedLabels = `${nums.length} (${[...distinct].slice(0, 6).join(' ')})`;

  // colored left/right stripe > 1px on a card-like box (impeccable side-tab: stripe >= 2x the other sides; card-like =
  // stripe + (radius or fill); impeccable exempts square boxes, hallmark gate 5 does not)
  const SAFE = /^(BLOCKQUOTE|NAV|A|INPUT|TEXTAREA|SELECT|PRE|CODE|SPAN|TH|TD|TR|LI|BUTTON|HR|IMG|SVG)$/;
  const boxes = [...document.body.querySelectorAll('*')].filter(el => !SAFE.test(el.tagName) && visible(el)).slice(0, 3000);
  const stripes = [];
  for (const el of boxes) { const s = getComputedStyle(el), r = el.getBoundingClientRect();
    if (r.width < 120 || r.height < 32) continue;
    const fill = rgb(s.backgroundColor)[3] ?? 1, rad = px(s.borderTopRightRadius) + px(s.borderBottomRightRadius) + px(s.borderTopLeftRadius);
    for (const side of ['Left', 'Right']) { const w = px(s[`border${side}Width`]), other = Math.max(px(s.borderTopWidth), px(s.borderBottomWidth), px(s[`border${side === 'Left' ? 'Right' : 'Left'}Width`]));
      if (w > 1 && s[`border${side}Style`] !== 'none' && spread(rgb(s[`border${side}Color`])) >= 30 && w >= other * 2 && (rad > 0 || fill > 0.05))
        stripes.push(`${name(el)} border-${side.toLowerCase()} ${w}px` + (rad >= 4 ? ' rounded' : ' square (impeccable exempts)')); } }
  if (stripes.length) out.sideStripe = stripes.slice(0, 3);

  // flat type scale: h1 / body < 1.8 (impeccable flat-type-hierarchy uses 1.25 per adjacent step; 1.8 is the house bar)
  const sizes = {};
  for (const el of texts) if (/^(P|LI|DD|TD)$/.test(el.tagName)) { const k = px(getComputedStyle(el).fontSize); sizes[k] = (sizes[k] || 0) + el.textContent.length; }
  const body = +Object.keys(sizes).sort((a, b) => sizes[b] - sizes[a])[0] || px(getComputedStyle(document.body).fontSize);
  const top = h1 || [...document.querySelectorAll('h2')].find(visible);
  if (top && px(getComputedStyle(top).fontSize) / body < 1.8) out.flatScale = `${top.tagName.toLowerCase()} ${px(getComputedStyle(top).fontSize)}px / body ${body}px = ${(px(getComputedStyle(top).fontSize) / body).toFixed(2)}`;

  // gray text on a colored ground (impeccable gray-on-color: ink HSL s < 0.2, 0.3 < l < 0.85; ground channel spread >= 40)
  const bgOf = el => { for (let p = el; p; p = p.parentElement) { const c = rgb(getComputedStyle(p).backgroundColor); if ((c[3] ?? 1) > 0.5) return c; } return [255, 255, 255]; };
  const gray = texts.filter(el => { const c = rgb(getComputedStyle(el).color); if ((c[3] ?? 1) < 0.5) return false;
    const mx = Math.max(c[0], c[1], c[2]) / 255, mn = Math.min(c[0], c[1], c[2]) / 255, l = (mx + mn) / 2, sat = mx === mn ? 0 : (mx - mn) / (1 - Math.abs(2 * l - 1));
    return sat < 0.2 && l > 0.3 && l < 0.85 && spread(bgOf(el)) >= 40; });
  if (gray.length) out.grayOnColor = gray.slice(0, 3).map(el => `${name(el)} ${getComputedStyle(el).color} on rgb(${bgOf(el).slice(0, 3).join(',')}) ${snip(el)}`);

  // em-dash density: > 1 per 120 non-space chars of body text, at least 3 (impeccable em-dash-overuse is looser: >= 8 and
  // ~1 per 500; taste-skill lint warns past 4 per page). A Chinese "——" counts once.
  const copy = (document.querySelector('main') || document.body).innerText, chars = copy.replace(/\s/g, '').length, dashes = (copy.match(/—+|\s--\s/g) || []).length;
  if (dashes >= 3 && dashes * 120 > chars) out.emDash = `${dashes} in ${chars} chars (1 per ${Math.round(chars / dashes)})`;

  // emoji as icons in headings, buttons and list markers (hallmark gate 30 "Icon tells"; taste-skill emoji, banned)
  const EMOJI = /\p{Emoji_Presentation}|\p{Extended_Pictographic}\uFE0F/u, emo = [];
  for (const el of document.querySelectorAll('h1,h2,h3,h4,h5,h6,button,[role=button],summary,li')) { if (!visible(el)) continue;
    const t = el.tagName === 'LI' ? el.textContent.trim().slice(0, 3) + getComputedStyle(el, '::before').content + getComputedStyle(el, '::marker').content : el.textContent;
    if (EMOJI.test(t)) emo.push(`${name(el)} ${snip(el)}`); }
  if (emo.length) out.emojiIcons = `${emo.length}: ` + emo.slice(0, 3).join(', ');

  // more than 3 distinct corner radii on card-like boxes (impeccable is_card_like: border or shadow, plus radius or fill;
  // taste-skill tells: "Square or fully round, chosen once"); pills and circles are left out
  const radii = new Set();
  for (const el of boxes) { const s = getComputedStyle(el), r = el.getBoundingClientRect(), rad = px(s.borderTopLeftRadius);
    if (r.width < 120 || r.height < 48 || !rad || rad >= Math.min(r.width, r.height) / 2) continue;
    const edge = px(s.borderTopWidth) + px(s.borderLeftWidth) > 0 || s.boxShadow !== 'none', fill = (rgb(s.backgroundColor)[3] ?? 1) > 0.05;
    if (edge && (rad || fill)) radii.add(rad); }
  if (radii.size > 3) out.cardRadii = [...radii].sort((a, b) => a - b).map(v => v + 'px').join(' ');
  return out;
}
"""

BAD_FONTS = ("simsun", "nsimsun", "宋体", "新宋体", "mingliu", "pmingliu", "simsun-extb", "simsun-extg")
ICON_FONTS = ("segoe ui symbol", "segoe ui emoji", "segoe mdl2", "segoe fluent", "material", "font awesome", "apple color emoji")


def rendered_fonts(page) -> dict:
    """Ask Chromium which platform fonts drew the text (CDP CSS.getPlatformFontsForNode). WebKit has no CDP: skipped."""
    try:
        cdp = page.context.new_cdp_session(page)
    except Exception:
        return {}
    cdp.send("DOM.enable"); cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
    sel = "h1,h2,h3,h4,h5,p,li,td,th,a,button,label,figcaption,small,span,div,text,tspan,dd,dt"
    ids = cdp.send("DOM.querySelectorAll", {"nodeId": root, "selector": sel})["nodeIds"][:600]
    glyphs: dict[str, int] = {}
    for nid in ids:
        try:
            for f in cdp.send("CSS.getPlatformFontsForNode", {"nodeId": nid})["fonts"]:
                glyphs[f["familyName"]] = glyphs.get(f["familyName"], 0) + f["glyphCount"]
        except Exception:
            continue
    total = sum(glyphs.values()) or 1
    text = {k: v for k, v in glyphs.items() if not any(i in k.lower() for i in ICON_FONTS)}
    share = {k: round(v / total, 3) for k, v in sorted(text.items(), key=lambda kv: -kv[1]) if v / total >= 0.005}
    bad = [k for k in text if any(b in k.lower() for b in BAD_FONTS)]
    out = {"fonts": share}
    if bad:
        out["badFonts"] = bad  # SimSun etc.: a serif/CJK stack fell back to the Windows default
    base = {re.sub(r"\s+(Semibold|Semilight|ExtraLight|Light|Thin|ExtraBold|Bold|Black|Medium|Heavy|Regular)$", "", k, flags=re.I) for k in share}
    if len(base) >= 3:  # one Latin face + one CJK face is normal; a third usually means mixed stacks
        out["mixedFonts"] = sorted(base)
    heavy = [k for k in share if re.search(r"Black|Heavy", k, re.I)]
    if heavy:
        out["heavyWeights"] = heavy  # 900 Latin next to 700 CJK reads as uneven ("有深有浅")
    return out


def contact_sheet(shots: dict[str, Path], dest: Path) -> None:
    tiles = []
    for name, p in shots.items():
        im = Image.open(p).convert("RGB")
        w = 760 if name.startswith("desktop") else 330
        h = min(int(im.height * w / im.width), 1100 if name.startswith("desktop") else 650)
        im = im.resize((w, int(im.height * w / im.width))).crop((0, 0, w, h))
        tiles.append((name, im))
    desk = [t for t in tiles if t[0].startswith("desktop")]
    mob = [t for t in tiles if t[0].startswith("iphone")]
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


def login_state(p, report):
    """Cookies of the Playwright profile that holds the 30-day Falconshire login, for every view's context."""
    profile, errors = Path.home() / ".claude" / "playwright-profile", []
    for channel in ("chrome", None):  # the profile's cookies are encrypted for the browser that wrote them
        try:
            ctx = p.chromium.launch_persistent_context(str(profile), headless=True, **({"channel": channel} if channel else {}))
            state = ctx.storage_state()
            ctx.close()
        except Exception as e:
            errors.append(str(e).splitlines()[0][:100])
            continue
        if any("falconshire" in c.get("domain", "") for c in state.get("cookies", [])):
            return state
        report.setdefault("notes", []).append("--login: the Playwright profile has no Falconshire login; sign in once "
                                              "(CLAUDE.md, password-protected pages), then rerun")
        return None
    report.setdefault("notes", []).append(f"--login: profile not readable ({errors[0]}); close the Playwright browser and rerun")
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out")
    ap.add_argument("--views", default=",".join(VIEWS), help="default: all; e.g. iphone-light,small-light")
    ap.add_argument("--full", action="store_true", help="full-page screenshots instead of the first screen")
    ap.add_argument("--wait", type=int, default=800, help="ms to wait after load for charts and fonts")
    ap.add_argument("--storage", action="append", default=[], metavar="KEY=VALUE",
                    help="localStorage entry written before every load, e.g. a PIN page's own unlock value; repeatable")
    ap.add_argument("--login", action="store_true",
                    help="reuse the Falconshire login saved in ~/.claude/playwright-profile (password-protected live pages)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    t = a.target
    url = t if t.startswith(("http://", "https://", "file:")) else Path(t).resolve().as_uri()
    stem = Path(t).stem if not t.startswith("http") else t.split("//")[1].split("/")[0]
    temp = Path(r"E:\AI\Claude\temp") if Path("E:\\").exists() else Path(r"D:\AI\Claude\temp")  # PCs without E: use D:
    out = Path(a.out) if a.out else temp / "shoot" / f"{stem}-{datetime.datetime.now():%m%d-%H%M%S}"
    out.mkdir(parents=True, exist_ok=True)
    src = Path(t)
    if src.is_file() and not src.read_text(encoding="utf-8", errors="replace")[:600].lstrip().lower().startswith("<!doctype"):
        # Artifact fragment: shoot it inside the skeleton the Artifact publisher adds.
        wrapped = src.with_name(f".shoot-{src.stem}.html")
        wrapped.write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" '
                           'content="width=device-width, initial-scale=1">' + src.read_text(encoding="utf-8")
                           + "</html>", encoding="utf-8")
        url = wrapped.resolve().as_uri()

    report, shots, hard = {"url": url, "out": str(out), "views": {}}, {}, False
    with sync_playwright() as p:
        browsers = {}

        def browser_for(engine: str):
            if engine not in browsers:
                try:
                    browsers[engine] = p.webkit.launch() if engine == "webkit" else p.chromium.launch(channel="chrome")
                except Exception as e:  # WebKit missing: `python -m playwright install webkit`
                    report.setdefault("notes", []).append(f"{engine} unavailable, used Chromium: {str(e)[:80]}")
                    browsers[engine] = p.chromium.launch()
            return browsers[engine]

        state = login_state(p, report) if a.login else None
        for name in [v.strip() for v in a.views.split(",") if v.strip()]:
            engine, opts = VIEWS[name]
            ctx = browser_for(engine).new_context(**opts, **({"storage_state": state} if state else {}))
            if a.storage:
                pairs = dict(kv.split("=", 1) for kv in a.storage)
                ctx.add_init_script("try{const p=%s;for(const k in p)localStorage.setItem(k,p[k])}catch(e){}" % json.dumps(pairs))
            page = ctx.new_page()
            errors, failed = [], []
            page.on("pageerror", lambda e: errors.append(str(e)[:160]))
            page.on("console", lambda m: m.type == "error" and errors.append("console: " + m.text[:160]))
            page.on("requestfailed", lambda r: failed.append(r.url[:120]))
            page.on("response", lambda r: r.status >= 400 and failed.append(f"{r.status} {r.url[:110]}"))
            page.goto(url, wait_until="networkidle", timeout=45000)
            if "/_falcon-auth/" in page.url:
                report["gated"] = True
                hard = True
                ctx.close()
                break
            page.wait_for_timeout(a.wait)
            res = page.evaluate(CHECKS_JS, not name.startswith("desktop"))
            tells = page.evaluate(AI_TELLS_JS)
            if tells:
                res["aiTells"] = tells  # warnings only: not part of hardFail
            if engine == "chromium":
                res.update(rendered_fonts(page))
            shot = out / f"{name}.png"
            page.screenshot(path=str(shot), full_page=a.full)
            if not name.startswith("small"):
                shots[name] = shot
            res.update(errors=errors[:5], failedRequests=failed[:5])
            res = {k: v for k, v in res.items() if v not in ([], 0, None)}
            res["hardFail"] = bool(res.get("overflowX", 0) > 0 or res.get("noViewportMeta") or errors or res.get("brokenImages")
                                or res.get("badFonts"))
            hard |= res["hardFail"]
            same = next((k for k, v in report["views"].items() if v == res), None)
            report["views"][name] = f"same findings as {same}" if same else res
            ctx.close()
        for b in browsers.values():
            b.close()
    if src.is_file() and url.endswith(f".shoot-{src.stem}.html"):
        src.with_name(f".shoot-{src.stem}.html").unlink(missing_ok=True)
    if shots:
        contact_sheet(shots, out / "contact.png")
        report["contact"] = str(out / "contact.png")
    report["pass"] = not hard
    print(json.dumps(report, ensure_ascii=False, indent=1))
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
