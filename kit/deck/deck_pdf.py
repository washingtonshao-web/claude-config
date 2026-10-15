#!/usr/bin/env python3
"""Export a kit/deck HTML deck to a 16:9 PDF (one slide per page), optionally with 1920x1080 PNGs of slides.

Usage:
    python deck_pdf.py deck.html [out.pdf] [--png 1,4,6 | --png all] [--png-dir DIR]

The PDF uses the deck's print CSS (@page 338.67mm x 190.5mm, margin 0), printed by system Chrome
(Playwright channel "chrome"; falls back to Playwright's Chromium). The script checks that the page
count equals the number of .k-slide sections. --png shoots the chosen slides at 1920x1080 without
the navigation bar (default folder: <deck name>-slides next to the PDF) for visual review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def pdf_pages(path: Path) -> int:
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(path)).pages)
    except ImportError:
        return len(re.findall(rb"/Type\s*/Page[^s]", path.read_bytes()))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--png", help="slide numbers (1-based, comma separated) or 'all'")
    ap.add_argument("--png-dir")
    a = ap.parse_args()
    src = Path(a.deck).resolve()
    out = Path(a.out).resolve() if a.out else src.with_suffix(".pdf")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(src.as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready.then(() => true)")
        n = page.evaluate("document.querySelectorAll('.k-slide').length")
        page.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
        shots = []
        if a.png:
            idx = range(1, n + 1) if a.png == "all" else [int(x) for x in a.png.split(",") if x.strip()]
            folder = Path(a.png_dir).resolve() if a.png_dir else out.with_name(out.stem + "-slides")
            folder.mkdir(parents=True, exist_ok=True)
            page.add_style_tag(content=".k-deck-bar{display:none!important}")
            for i in idx:
                page.evaluate(f"location.hash = '#{i}'")
                page.wait_for_timeout(150)
                shot = folder / f"slide-{i:02d}.png"
                page.screenshot(path=str(shot))
                shots.append(str(shot))
        browser.close()
    pages = pdf_pages(out)
    print(f"{out}  {pages} pages, {n} slides, {out.stat().st_size / 1024:.0f} KB")
    for s in shots:
        print(s)
    if pages != n:
        print(f"WARNING: page count {pages} != slide count {n} (a slide overflows its 16:9 page?)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
