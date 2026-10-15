#!/usr/bin/env python3
"""Inline the Falconshire design kit into built pages.

Usage:
    python apply_kit.py <site-dir | page.html> [--copy]

Pages reference the kit with
    <link rel="stylesheet" href="kit/v1.css">
    <script src="kit/v1.js"></script>
and this script swaps those tags for inline <style data-kit="v1"> / <script data-kit="v1">
blocks, so every page is one self-contained HTML file (works with publish.py, the
Falconshire Publisher connector, the Bunny mirror and offline). Style skins linked as
    <link rel="stylesheet" href="kit/styles/<name>.css">
are inlined the same way as <style data-kit-style="<name>">. The HTML slide deck
    <link rel="stylesheet" href="kit/deck/deck.css">  <script src="kit/deck/deck.js"></script>
is inlined as <style data-kit-deck="css"> / <script data-kit-deck="js"> (see design/slides.md). Re-running refreshes
previously inlined blocks to the current kit. --copy also places the raw kit files in
out/kit/ so they are served alongside the page. Pages that reference kit/map/ (relief tiles and China
boundary layers, see design/maps.md) get the map assets copied to <page dir>/kit/map/ automatically;
publish those sites with publish.py (multi-file), not the single-file Publisher connector.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent
VERSION = "v1"
CSS = (KIT_DIR / f"{VERSION}.css").read_text(encoding="utf-8")
JS = (KIT_DIR / f"{VERSION}.js").read_text(encoding="utf-8")

LINK_RE = re.compile(r'<link\b[^>]*href=["\'][^"\']*kit/%s\.css["\'][^>]*>' % VERSION, re.I)
SCRIPT_RE = re.compile(r'<script\b[^>]*src=["\'][^"\']*kit/%s\.js["\'][^>]*>\s*</script>' % VERSION, re.I)
STYLE_BLOCK_RE = re.compile(r'<style data-kit="%s">.*?</style>' % VERSION, re.S)
SCRIPT_BLOCK_RE = re.compile(r'<script data-kit="%s">.*?</script>' % VERSION, re.S)
SKIN_LINK_RE = re.compile(r'<link\b[^>]*href=["\'][^"\']*kit/styles/([\w-]+)\.css["\'][^>]*>', re.I)
SKIN_BLOCK_RE = re.compile(r'<style data-kit-style="([\w-]+)">.*?</style>', re.S)
DECK_CSS_RE = re.compile(r'<link\b[^>]*href=["\'][^"\']*kit/deck/deck\.css["\'][^>]*>', re.I)
DECK_JS_RE = re.compile(r'<script\b[^>]*src=["\'][^"\']*kit/deck/deck\.js["\'][^>]*>\s*</script>', re.I)
DECK_CSS_BLOCK_RE = re.compile(r'<style data-kit-deck="css">.*?</style>', re.S)
DECK_JS_BLOCK_RE = re.compile(r'<script data-kit-deck="js">.*?</script>', re.S)


def skin(name: str) -> str:
    css = (KIT_DIR / "styles" / f"{name}.css").read_text(encoding="utf-8")
    return f'<style data-kit-style="{name}">\n{css}</style>'


def inline(html: str) -> tuple[str, int]:
    style = f'<style data-kit="{VERSION}">\n{CSS}</style>'
    script = f'<script data-kit="{VERSION}">\n{JS}</script>'
    total = 0
    for pattern, block in ((LINK_RE, style), (STYLE_BLOCK_RE, style), (SCRIPT_RE, script), (SCRIPT_BLOCK_RE, script)):
        html, n = pattern.subn(lambda _m, b=block: b, html)
        total += n
    for pattern in (SKIN_LINK_RE, SKIN_BLOCK_RE):
        html, n = pattern.subn(lambda m: skin(m.group(1)), html)
        total += n
    if DECK_CSS_RE.search(html) or DECK_JS_RE.search(html) or 'data-kit-deck="' in html:
        deck = KIT_DIR / "deck"
        css = f'<style data-kit-deck="css">\n{(deck / "deck.css").read_text(encoding="utf-8")}</style>'
        js = f'<script data-kit-deck="js">\n{(deck / "deck.js").read_text(encoding="utf-8")}</script>'
        for pattern, block in ((DECK_CSS_RE, css), (DECK_CSS_BLOCK_RE, css), (DECK_JS_RE, js), (DECK_JS_BLOCK_RE, js)):
            html, n = pattern.subn(lambda _m, b=block: b, html)
            total += n
    return html, total


def pages(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    out = target / "out"
    return sorted((out if out.is_dir() else target).rglob("*.html"))


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        raise SystemExit(__doc__)
    target = Path(args[0]).resolve()
    touched = []
    map_dirs = set()
    for page in pages(target):
        html = page.read_text(encoding="utf-8")
        if "kit/map/" in html:
            map_dirs.add(page.parent)
        new, n = inline(html)
        if n and new != html:
            page.write_text(new, encoding="utf-8", newline="\n")
        if n:
            touched.append(f"{page.name} ({n})")
    for d in sorted(map_dirs):
        shutil.copytree(KIT_DIR / "map", d / "kit" / "map", dirs_exist_ok=True)
        touched.append(f"copied map assets to {d / 'kit' / 'map'}")
    if "--copy" in sys.argv:
        dest = (target / "out" if target.is_dir() else target.parent) / "kit"
        dest.mkdir(parents=True, exist_ok=True)
        for name in (f"{VERSION}.css", f"{VERSION}.js"):
            shutil.copy2(KIT_DIR / name, dest / name)
        if (KIT_DIR / "styles").is_dir():
            shutil.copytree(KIT_DIR / "styles", dest / "styles", dirs_exist_ok=True)
        (dest / "deck").mkdir(exist_ok=True)
        for name in ("deck.css", "deck.js"):
            shutil.copy2(KIT_DIR / "deck" / name, dest / "deck" / name)
        touched.append(f"copied kit files to {dest}")
    print("kit applied: " + (", ".join(touched) if touched else "no kit references found"))


if __name__ == "__main__":
    main()
