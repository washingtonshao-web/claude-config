# claude-config

One place for Yang's Claude setup outside the home PC. Claude Code **cloud sessions** (claude.ai/code → Cloud) install everything here automatically.

## Skills catalog

| Group | Skills | Where they come from | Cloud | Home PC |
|---|---|---|---|---|
| Documents | docx, pdf, pptx, xlsx, skill-creator, docs | claude.ai account (Customize → Skills) | ✅ | ✅ |
| Web | website-design (+ `kit/`) | this repo, `skills/web/` | ✅ | ✅ |
| Video | hyperframes ×8, media-use, general-video, slideshow, product-launch-video | upstream `heygen-com/hyperframes` | ✅ | ✅ |
| Games | threejs ×9 | this repo, `skills/games/` | ✅ (asset generation needs Gemini / Tripo / ElevenLabs keys) | ✅ |
| PC only | codex-gpt, flow-video, aws-billing, signing-in-to-aws | home PC | ❌ | ✅ |

## Tools (MCP / connectors)

| Tool | Cloud | Home PC |
|---|---|---|
| Bio Research, Falconshire Publisher, Travel Planner, Claude Docs (claude.ai connectors) | ✅ | ✅ |
| Playwright (headless Chromium) | ✅ installed by `cloud/install.sh` | ✅ |
| Claude in Chrome, Flow video, Codex GPT, browser pane | ❌ use Remote Control → **home** | ✅ |

## Files

| Path | Role |
|---|---|
| `webclaude.md` | The local `~/.claude/CLAUDE.md` (shared-block markers stripped), pushed by the PCs' daily config sync |
| `cloud-notes.md` | Cloud-only notes appended to it |
| `skills/<group>/<skill>/` | Skills owned or kept by Yang, synced from the PC |
| `kit/` | Website design kit (`v1.css`, `v1.js`, `apply_kit.py`) |
| `cloud-setup.sh` → `cloud/install.sh` | Environment setup: CLAUDE.md, skills, HyperFrames CLI, Playwright MCP, ffmpeg, refresh hook |

Flow: the daily PC config sync (04:00, source of truth in a private repo) pushes changed CLAUDE.md / skills / kit here → cloud environment setup (cached ~7 days) installs all → every new cloud session's SessionStart hook pulls this repo and refreshes CLAUDE.md and skills for the next session.

Cloud environment setup script (environments "Full" and "Default"):

```bash
curl -fsSL https://raw.githubusercontent.com/washingtonshao-web/claude-config/main/cloud-setup.sh | bash || true
```
