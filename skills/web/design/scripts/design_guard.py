#!/usr/bin/env python3
"""PreToolUse hook: remind Claude or Codex to load the design skill before it writes or publishes something Yang will look at.

Fires on Write/Edit of .html/.htm/.css/.svg files, Artifact publishes and publish_static_site. If the session transcript
shows the design skill was loaded (Skill call, /design, or its SKILL.md read), it stays silent; otherwise it adds a
one-line reminder to the agent's context. It never blocks the call. Codex sends file edits as apply_patch (paths in the
patch text) and gets the same hook through ~/.codex/hooks.json (wired by the ai-config sync). Wire it in ~/.claude/settings.json:
  "PreToolUse": [{"matcher": "^(Write|Edit|Artifact)$|__publish_static_site$",
                  "hooks": [{"type": "command", "command": "python \"$HOME/.claude/skills/design/scripts/design_guard.py\" 2>/dev/null || true", "timeout": 10}]}]
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

VISUAL_EXT = (".html", ".htm", ".css", ".svg")
MARKERS = (b'"skill":"design"', b'"skill": "design"', b"skills\\\\design\\\\SKILL.md", b"skills/design/SKILL.md",
           b"<command-name>/design</command-name>", b"Base directory for this skill: C:\\\\Users\\\\Administrator\\\\.claude\\\\skills\\\\design")
REMINDER = ("Design rules not loaded in this session. Before writing or publishing this visual output, invoke the "
            "`design` skill (Skill tool, skill: design) and follow it: kit fonts only (never SimSun), restraint list, "
            "maps.md for maps, review.md before delivery.")
CODEX_REMINDER = ("Design rules not loaded in this session. Before writing or publishing this visual output, read "
                  "~/.codex/skills/design/SKILL.md and its references/codex.md and follow them: kit fonts only (never SimSun), "
                  "restraint list, maps.md for maps, review.md before delivery.")
PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update) File: (.+)$", re.M)


def relevant(name: str, inp: dict) -> bool:
    if name in ("Write", "Edit"):
        return str(inp.get("file_path", "")).lower().endswith(VISUAL_EXT)
    if name == "apply_patch":  # Codex: the patch text names the files
        text = inp.get("command", "") if isinstance(inp, dict) else str(inp)
        text = " ".join(text) if isinstance(text, list) else str(text)
        return any(f.strip().lower().endswith(VISUAL_EXT) for f in PATCH_FILE.findall(text))
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
    codex = "turn_id" in ev or ev.get("tool_name") == "apply_patch"
    sys.stdout.write(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                        "additionalContext": CODEX_REMINDER if codex else REMINDER}}))


if __name__ == "__main__":
    main()
