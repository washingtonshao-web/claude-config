#!/bin/bash
# Installs the user's Claude config into a Claude Code cloud VM.
#   full  (default) - run by the environment setup script; result is cached by the environment snapshot
#   quick           - run by the SessionStart hook; pulls this repo and refreshes CLAUDE.md + own skills only
# Source of truth: github.com/washingtonshao-web/claude-config (synced from the user's PC).
set -u
MODE="${1:-full}"
REPO=https://github.com/washingtonshao-web/claude-config
DIR=/opt/claude-config
HF_SKILLS="hyperframes hyperframes-animation hyperframes-audio hyperframes-cli hyperframes-core hyperframes-creative hyperframes-keyframes hyperframes-registry media-use general-video slideshow product-launch-video"
mkdir -p ~/.claude/skills

if [ -d $DIR/.git ]; then git -C $DIR pull -q --ff-only 2>/dev/null || true
else git clone -q --depth 1 $REPO $DIR || exit 0; fi

# 1. Global instructions: local CLAUDE.md + cloud notes -> ~/.claude/CLAUDE.md
cat $DIR/webclaude.md $DIR/cloud-notes.md > ~/.claude/CLAUDE.md

# 2. Own skills: category folders in the repo, installed flat (~/.claude/skills/<name>/SKILL.md)
for s in $DIR/skills/*/*/; do
  n=$(basename "$s"); rm -rf ~/.claude/skills/"$n"; cp -r "$s" ~/.claude/skills/"$n"
done

[ "$MODE" = quick ] && exit 0

# 3. HyperFrames skills from upstream (same source as the PC: heygen-com/hyperframes)
(
  T=$(mktemp -d)
  git clone -q --depth 1 --filter=blob:none --sparse https://github.com/heygen-com/hyperframes "$T" &&
  git -C "$T" sparse-checkout set skills >/dev/null 2>&1 &&
  for n in $HF_SKILLS; do [ -d "$T/skills/$n" ] && rm -rf ~/.claude/skills/$n && cp -r "$T/skills/$n" ~/.claude/skills/$n; done
  rm -rf "$T"
) &

# 4. Tools: HyperFrames CLI, Playwright MCP + Chromium, ffmpeg
( npm i -g hyperframes >/dev/null 2>&1
  npx -y @playwright/mcp@0.0.83 --version >/dev/null 2>&1            # warm the npx cache (kept in the snapshot)
  npx -y playwright@1.64.0-alpha-1790635538000 install chromium >/dev/null 2>&1 ) &
( command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg) >/dev/null 2>&1 ) &
wait

# 5. User-level MCP server + SessionStart refresh hook
python3 - <<'PY'
import json, os
p = os.path.expanduser("~/.claude.json")
c = json.load(open(p)) if os.path.exists(p) else {}
c.setdefault("mcpServers", {})["playwright"] = {
    "type": "stdio", "command": "npx",
    "args": ["-y", "@playwright/mcp@0.0.83", "--headless", "--browser", "chromium", "--no-sandbox", "--output-dir", "/tmp/playwright-output"]}
json.dump(c, open(p, "w"), indent=1)

p = os.path.expanduser("~/.claude/settings.json")
s = json.load(open(p)) if os.path.exists(p) else {}
ss = [h for h in s.setdefault("hooks", {}).get("SessionStart", [])
      if "pull-webclaude" not in json.dumps(h) and "claude-config" not in json.dumps(h)]
ss.append({"matcher": "startup", "hooks": [{"type": "command", "async": True,
           "command": "bash /opt/claude-config/cloud/install.sh quick >/dev/null 2>&1"}]})
s["hooks"]["SessionStart"] = ss
json.dump(s, open(p, "w"), indent=1)
PY
rm -f ~/.claude/pull-webclaude.sh ~/.claude/webclaude-fallback.md
exit 0
