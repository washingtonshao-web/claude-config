#!/usr/bin/env python3
"""PreToolUse hook: remind Claude to load the design skill before it writes or publishes something Yang will look at.

Fires on Write/Edit of .html/.htm/.css/.svg files, Artifact publishes and publish_static_site. If the session transcript
shows the design skill was loaded (Skill call, /design, or its SKILL.md read), it stays silent; otherwise it adds a
one-line reminder to Claude's context. It never blocks the call. Wire it in ~/.claude/settings.json:
  "PreToolUse": [{"matcher": "^(Write|Edit|Artifact)$|__publish_static_site$",
                  "hooks": [{"type": "command", "command": "python \"$HOME/.claude/skills/design/scripts/design_guard.py\" 2>/dev/null || true", "timeout": 10}]}]
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

VISUAL_EXT = (".html", ".htm", ".css", ".svg")
MARKERS = (b'"skill":"design"', b'"skill": "design"', b"skills\\\\design\\\\SKILL.md", b"skills/design/SKILL.md",
           b"<command-name>/design</command-name>", b"Base directory for this skill: C:\\\\Users\\\\Administrator\\\\.claude\\\\skills\\\\design")
REMINDER = ("Design rules not loaded in this session. Before writing or publishing this visual output, invoke the "
            "`design` skill (Skill tool, skill: design) and follow it: kit fonts only (never SimSun), restraint list, "
            "maps.md for maps, review.md before delivery.")


def relevant(name: str, inp: dict) -> bool:
    if name in ("Write", "Edit"):
        return str(inp.get("file_path", "")).lower().endswith(VISUAL_EXT)
    if name == "Artifact":
        return inp.get("action", "publish") == "publish" and not inp.get("asset")
    return name.endswith("__publish_static_site")


def loaded(transcript: str, session: str) -> bool:
    cache = Path(tempfile.gettempdir()) / "claude-design-guard" / f"{session or 'none'}.ok"
    if cache.exists():
        return True
    try:
        data = Path(transcript).read_bytes()
    except OSError:
        return True  # can't tell: stay quiet rather than nag
    if any(m in data for m in MARKERS):
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text("1")
        return True
    return False


def main() -> None:
    try:
        ev = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace") or "{}")
    except ValueError:
        return
    if os.environ.get("DESIGN_GUARD_OFF") or not relevant(ev.get("tool_name", ""), ev.get("tool_input") or {}):
        return
    if loaded(ev.get("transcript_path", ""), ev.get("session_id", "")):
        return
    sys.stdout.write(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": REMINDER}}))


if __name__ == "__main__":
    main()
