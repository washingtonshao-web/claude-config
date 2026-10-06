# claude-config

Bootstrap for Yang's Claude Code **cloud sessions** (claude.ai/code → Cloud), plus the new-PC installer
(release `setup` → `AI-Config-Setup.cmd`). The source of truth is a private repo; the PCs' daily sync refreshes this one.

## How a cloud session gets its config

`cloud/install.sh` installs global instructions, skills, workflows and the website kit from the first source that works:

| # | Source | Needs (cloud environment variable) |
|---|---|---|
| 1 | The private repo | `AI_CONFIG_TOKEN` (read-only GitHub token) |
| 2 | `bundle.enc` here — the same content, encrypted (AES-256-CBC, PBKDF2) | `AI_CONFIG_KEY` |
| 3 | The readable copy here (`webclaude.md`, `skills/`, `kit/`), while it is still published | — |

It also installs the HyperFrames skills and CLI, Playwright MCP + Chromium and ffmpeg, and adds a SessionStart hook
that refreshes instructions and skills at the start of every session. `~/.claude/.config-source` says which source was used.

## Files

| Path | Role |
|---|---|
| `cloud-setup.sh` → `cloud/install.sh` | Environment setup script and refresh hook |
| `bundle.enc`, `bundle.sha256` | Encrypted config bundle; the hash changes when its content changes |
| `webclaude.md`, `cloud-notes.md`, `skills/`, `kit/`, `workflows/`, `cloud/settings.json` | Readable copy (being retired) |

Cloud environment setup script (environments "Full" and "Default"):

```bash
curl -fsSL https://raw.githubusercontent.com/washingtonshao-web/claude-config/main/cloud-setup.sh | bash || true
```
