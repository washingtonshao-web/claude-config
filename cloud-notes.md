
## Cloud session notes (Claude Code cloud VM only)

- This is a Linux cloud VM, not the user's Windows PC. Local-only tools are absent: Claude in Chrome, the built-in browser pane, the Codex desktop app (codex-gpt, GPT images), the local video MCP / Google Flow, `publish.py`, AWS credentials. Say so briefly when a task needs them; the user can rerun it on the PC through Remote Control (machine "home").
- Path mapping: `E:\Claude\sites\_kit\` → `/opt/claude-config/kit/` (run `python3 /opt/claude-config/kit/apply_kit.py <site-dir>`). Temp files → `/tmp`. Keep deliverables inside the current repository and commit them.
- Publish websites with the Falconshire Publisher connector (the only publishing route here).
- Screenshots / visual review: the `playwright` MCP, or Python Playwright with `p.chromium.launch()` (no `channel="chrome"`).
- Config source: github.com/washingtonshao-web/claude-config (this file = `cloud-notes.md`; `webclaude.md` = the user's local CLAUDE.md, synced automatically).
