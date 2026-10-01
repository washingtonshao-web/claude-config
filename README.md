# claude-config

Global Claude instructions for Claude Code **cloud sessions** (claude.ai/code).

| File | Role |
|---|---|
| `webclaude.md` | Copy of the local `~/.claude/CLAUDE.md`, pushed automatically by a local Claude Code hook whenever it changes |
| `cloud-notes.md` | Cloud-only notes appended after the rules |
| `cloud-setup.sh` | Run by the cloud environment's setup script; installs a SessionStart hook in the VM |

How it flows: local CLAUDE.md changes → local SessionStart/SessionEnd hook (`~/.claude/hooks/sync-webclaude.ps1`) uploads `webclaude.md` → every cloud session start (and resume / clear / compact) the VM hook fetches `webclaude.md` + `cloud-notes.md` from the GitHub API and injects them as context.

Cloud environments "Full" and "Default" use this setup script:

```bash
curl -fsSL https://raw.githubusercontent.com/washingtonshao-web/claude-config/main/cloud-setup.sh | bash || true
```
