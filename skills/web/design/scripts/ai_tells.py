#!/usr/bin/env python3
"""Moved to the de-ai skill (de-ai/scripts/ai_tells.py); this shim keeps old paths working.

Looks for the de-ai skill beside this skill first, then in the installed skills folders of Claude and Codex.
"""
import runpy
import sys
from pathlib import Path

here = Path(__file__).resolve()
candidates = [here.parents[2] / "de-ai" / "scripts" / "ai_tells.py",
              Path.home() / ".claude" / "skills" / "de-ai" / "scripts" / "ai_tells.py",
              Path.home() / ".codex" / "skills" / "de-ai" / "scripts" / "ai_tells.py"]
target = next((c for c in candidates if c.exists()), None)
if target is None:
    sys.exit("ai_tells.py: the de-ai skill is not installed; run the words check by hand with writing.md")
sys.argv[0] = str(target)
runpy.run_path(str(target), run_name="__main__")
