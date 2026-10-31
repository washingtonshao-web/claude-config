"""Fresh Falconshire login for AI browsers, on any PC that has the static-sites-prod SSH key.

    python falcon_login.py                 # put a 30-day login into ~/.claude/playwright-profile
    python falcon_login.py --profile DIR   # another persistent browser profile (Codex, a second tool)
    python falcon_login.py --check URL     # open URL headless with a fresh login; reports gated or not
    python falcon_login.py --text URL      # print the page's visible text (reading a protected page)
        [--storage KEY=VALUE]              # localStorage before load, e.g. a site's own PIN unlock (health: hr-unlock)

The AWS host signs the cookies (`falconshire-ops login-cookies`, root-only secret): the shared site
password, the Personal and Private Library collections, and every site with its own password. No
password is typed and no cookie value is printed. Each issue is logged on the host (syslog tag
falconshire-ops). shoot.py --login calls fetch_cookies() directly, so screenshots never need the profile.
Close the Playwright MCP browser before writing its profile (Chrome locks an open profile).
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path

SSH_ALIAS = "static-sites-prod"
PROFILE = Path.home() / ".claude" / "playwright-profile"


def storage_state(label: str = "") -> dict:
    """The same login as a Playwright storage_state (browser.new_context(storage_state=...))."""
    cookies = [dict(c, domain=c["url"].split("/")[2], path="/") if "url" in c else c for c in fetch_cookies(label)]
    return {"cookies": [{k: v for k, v in c.items() if k != "url"} for c in cookies], "origins": []}


def fetch_cookies(label: str = "") -> list[dict]:
    """Playwright-format cookies from the host; raises RuntimeError when SSH or the host refuses."""
    label = "".join(ch for ch in (label or platform.node() or "pc") if ch.isalnum() or ch in "-_")[:40] or "pc"
    proc = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", SSH_ALIAS,
                           f"sudo -n /usr/local/sbin/falconshire-ops login-cookies --label {label}"],
                          capture_output=True, text=True, timeout=60)
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        raise RuntimeError(f"no answer from {SSH_ALIAS}: {(proc.stderr or proc.stdout).strip()[:200]}") from None
    if not data.get("ok"):
        raise RuntimeError(f"host refused: {data.get('error', 'unknown error')}")
    out = []
    for c in data["cookies"]:
        c = dict(c)
        if c["name"].startswith("__Host-"):  # host-only cookie: Playwright wants a url, not a domain
            c["url"] = f"https://{c.pop('domain')}/"
            c.pop("path", None)
        out.append(c)
    return out


def install(profile: Path, cookies: list[dict]) -> str:
    """Write the cookies into a persistent profile; returns the browser channel that accepted them."""
    from playwright.sync_api import sync_playwright
    if profile_in_use(profile):
        raise RuntimeError("the Playwright browser has this profile open; close it (Playwright MCP browser_close) and rerun")
    errors = []
    with sync_playwright() as p:
        # The Playwright MCP opens this profile with Chrome; bundled Chromium only where Chrome is missing.
        for channel in ("chrome", None):
            try:
                ctx = p.chromium.launch_persistent_context(str(profile), headless=True,
                                                           **({"channel": channel} if channel else {}))
            except Exception as e:
                errors.append(str(e).splitlines()[0][:120])
                if channel and chrome_installed():
                    break  # Chrome exists but failed: writing with Chromium would not help the MCP browser
                continue
            ctx.add_cookies(cookies)
            ctx.close()
            return channel or "chromium"
    raise RuntimeError(f"profile not writable ({errors[0]}); close the Playwright browser and rerun")


def chrome_installed() -> bool:
    import shutil
    return bool(shutil.which("chrome")) or any(Path(d, "Google", "Chrome", "Application", "chrome.exe").exists()
                                               for d in (r"C:\Program Files", r"C:\Program Files (x86)"))


def profile_in_use(profile: Path) -> bool:
    """A running Chrome keeps <profile>/lockfile open; on Windows it then cannot be removed."""
    lock = profile / "lockfile"
    if not lock.exists():
        return False
    try:
        lock.unlink()
        return False
    except OSError:
        return True


def check(url: str, cookies: list[dict], text: bool = False, storage: dict | None = None) -> tuple[bool, str]:
    """(opened without the Falconshire login page, visible text when asked)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()
        ctx.add_cookies(cookies)
        if storage:
            ctx.add_init_script("try{const p=%s;for(const k in p)localStorage.setItem(k,p[k])}catch(e){}" % json.dumps(storage))
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle" if text else "domcontentloaded", timeout=45000)
        ok = "/_falcon-auth/" not in page.url
        body = page.inner_text("body")[:50000] if text and ok else ""
        browser.close()
    return ok, body


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", type=Path, default=PROFILE)
    ap.add_argument("--check", metavar="URL")
    ap.add_argument("--text", metavar="URL")
    ap.add_argument("--storage", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--label", default="", help="name for the host's log; default: this PC's name")
    a = ap.parse_args()
    try:
        cookies = fetch_cookies(a.label)
        if a.check or a.text:
            url = a.text or a.check
            ok, body = check(url, cookies, text=bool(a.text), storage=dict(kv.split("=", 1) for kv in a.storage))
            if a.text and ok:
                sys.stdout.reconfigure(encoding="utf-8")
                print(body)
            else:
                print(json.dumps({"ok": ok, "url": url, "gated": not ok}))
            sys.exit(0 if ok else 1)
        channel = install(a.profile, cookies)
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        sys.exit(1)
    days = round((max(c["expires"] for c in cookies) - __import__("time").time()) / 86400)
    print(json.dumps({"ok": True, "profile": str(a.profile), "browser": channel, "cookies": len(cookies),
                      "valid_days": days}))


if __name__ == "__main__":
    main()
