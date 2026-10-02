#!/usr/bin/env python3
"""Print the kit's design tokens as JSON for Python charts and Office files.

Usage:
    python tokens.py [--style kit|economist|<skin>] [--theme light|dark]

Reads E:\\Claude\\sites\\_kit\\v1.css (and kit/styles/<skin>.css on top), so colors are never
copied by hand. Output keys: tokens (all --k-* values), series (8 categorical colors in order),
seq (5 magnitude steps), font, matplotlib (rcParams ready for mpl.rcParams.update).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

KIT = Path(r"E:\Claude\sites\_kit")
VAR_RE = re.compile(r"--(k-[\w-]+)\s*:\s*([^;]+);")


def block(css: str, selector_re: str) -> dict[str, str]:
    m = re.search(selector_re + r"\s*\{([^}]*)\}", css)
    return dict(VAR_RE.findall(m.group(1))) if m else {}


def load(style: str, theme: str) -> dict[str, str]:
    css = (KIT / "v1.css").read_text(encoding="utf-8")
    tokens = block(css, r"(?m)^:root")
    if theme == "dark":
        tokens.update(block(css, r':root\[data-theme="dark"\]'))
    if style != "kit":
        skin = (KIT / "styles" / f"{style}.css").read_text(encoding="utf-8")
        tokens.update(block(skin, r":root, :root\[data-theme=\"dark\"\]"))
    return {k: v.strip() for k, v in tokens.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", default="kit")
    ap.add_argument("--theme", default="light", choices=["light", "dark"])
    a = ap.parse_args()
    t = load(a.style, a.theme)
    series = [t[f"k-s{i}"] for i in range(1, 9) if f"k-s{i}" in t]
    seq = [t[f"k-seq-{i}"] for i in range(1, 6) if f"k-seq-{i}" in t]
    font = ["Microsoft YaHei UI", "PingFang SC", "Noto Sans SC", "DejaVu Sans"]
    if a.style == "economist":
        font = ["Roboto Condensed"] + font
    mpl = {
        "font.family": "sans-serif",
        "font.sans-serif": font,
        "axes.unicode_minus": False,
        "axes.prop_cycle": "cycler('color', %r)" % series,
        "axes.edgecolor": t.get("k-axis", "#333333"),
        "axes.labelcolor": t.get("k-ink-2", "#333333"),
        "axes.facecolor": t.get("k-surface", "#ffffff"),
        "figure.facecolor": t.get("k-page", "#ffffff"),
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": t.get("k-grid", "#dddddd"),
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "xtick.color": t.get("k-muted", "#666666"),
        "ytick.color": t.get("k-muted", "#666666"),
        "ytick.major.size": 0,
        "xtick.major.size": 3,
        "text.color": t.get("k-ink", "#111111"),
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    }
    if a.style == "economist":
        mpl["ytick.labelright"] = True
        mpl["ytick.labelleft"] = False
    print(json.dumps({"style": a.style, "theme": a.theme, "tokens": t, "series": series, "seq": seq,
                      "font": font, "matplotlib": mpl}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
