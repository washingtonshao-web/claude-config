"""Visual QA in one call: desktop + mobile, light + dark, with layout checks.

Usage: python shots.py <url-or-html-file> [outdir] [--full]
Prints one summary line per view; screenshots go to outdir (default ./qa-shots).
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

VIEWS = {
    "desktop": dict(viewport={"width": 1440, "height": 900}),
    "mobile": dict(viewport={"width": 390, "height": 844}, is_mobile=True,
                   has_touch=True, device_scale_factor=2),
}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    full = "--full" in sys.argv
    target = args[0]
    out = pathlib.Path(args[1] if len(args) > 1 else "qa-shots")
    out.mkdir(parents=True, exist_ok=True)
    if pathlib.Path(target).exists():
        target = pathlib.Path(target).resolve().as_uri()

    problems = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for name, opts in VIEWS.items():
            for scheme in ("light", "dark"):
                ctx = browser.new_context(color_scheme=scheme, **opts)
                page = ctx.new_page()
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)[:120]))
                page.on("response", lambda r: r.status >= 400 and errors.append(f"HTTP {r.status} {r.url[:100]}"))
                page.goto(target, wait_until="load", timeout=60000)
                page.wait_for_timeout(1500)
                m = page.evaluate("""() => ({
                    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                    brokenImgs: [...document.images].filter(i => i.complete && i.naturalWidth === 0).length,
                    height: document.documentElement.scrollHeight
                })""")
                path = out / f"{name}-{scheme}.png"
                page.screenshot(path=str(path), full_page=full)
                bad = m["overflow"] > 0 or m["brokenImgs"] or errors
                problems += bool(bad)
                print(f"{'FAIL' if bad else 'ok  '} {name:7} {scheme:5} overflow={m['overflow']}px "
                      f"broken_imgs={m['brokenImgs']} errors={len(errors)} height={m['height']}px -> {path}")
                for e in errors[:3]:
                    print("      error:", e)
                ctx.close()
        browser.close()
    print(f"{problems} view(s) with problems; open the PNGs to judge the design itself.")

if __name__ == "__main__":
    main()
