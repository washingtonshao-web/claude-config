#!/usr/bin/env python3
"""Moved to the de-ai skill (de-ai/scripts/ai_tells.py); this shim keeps old paths working."""
import runpy
import sys
from pathlib import Path

target = Path(__file__).resolve().parents[2] / "de-ai" / "scripts" / "ai_tells.py"
sys.argv[0] = str(target)
runpy.run_path(str(target), run_name="__main__")
