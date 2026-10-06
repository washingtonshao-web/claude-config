#!/bin/bash
# Installs the user's Claude config into a Claude Code cloud VM.
#   full  (default) - run by the environment setup script; result is cached by the environment snapshot
#   quick           - run by the SessionStart hook; pulls this repo and refreshes CLAUDE.md + own skills only
# Source of truth: the private repo washingtonshao-web/ai-config; the PCs' daily sync refreshes this public repo.
# Sources, first that works: private repo (AI_CONFIG_TOKEN) > bundle.enc (AI_CONFIG_KEY) > readable public copy.
# ~/.claude/.config-source says which one was used.
set -u
MODE="${1:-full}"
REPO=https://github.com/washingtonshao-web/claude-config
DIR=/opt/claude-config
HF_SKILLS="hyperframes hyperframes-animation hyperframes-audio hyperframes-cli hyperframes-core hyperframes-creative hyperframes-keyframes hyperframes-registry media-use general-video slideshow product-launch-video"
mkdir -p ~/.claude/skills

if [ -d $DIR/.git ]; then git -C $DIR pull -q --ff-only 2>/dev/null || true
else git clone -q --depth 1 $REPO $DIR || exit 0; fi
# The pull may have replaced this very file: run the fresh copy once instead of finishing the old one.
if [ -z "${CFG_REEXEC:-}" ] && [ -f $DIR/cloud/install.sh ]; then CFG_REEXEC=1 exec bash $DIR/cloud/install.sh "$MODE"; fi

# Preferred source: the private repo washingtonshao-web/ai-config (the PCs' source of truth).
# Cloud sessions' own GitHub access covers only the session's repo, so reading it needs a read-only token in the
# environment variable AI_CONFIG_TOKEN (cloud environment settings). Without it: the public mirror in this repo.
PRIV=/opt/ai-config
PC_ONLY="codex-gpt aws-billing-and-cost-management signing-in-to-aws"
privgit() {
  if [ -n "${AI_CONFIG_TOKEN:-}" ]; then
    GIT_TERMINAL_PROMPT=0 git -c http.extraHeader="Authorization: Basic $(printf 'x-access-token:%s' "$AI_CONFIG_TOKEN" | base64 -w0)" "$@"
  else GIT_TERMINAL_PROMPT=0 git "$@"; fi
}
if [ -d $PRIV/.git ]; then privgit -C $PRIV pull -q --ff-only 2>/dev/null || true
else rm -rf $PRIV; privgit clone -q --depth 1 https://github.com/washingtonshao-web/ai-config $PRIV 2>/dev/null || rm -rf $PRIV; fi
if [ -n "${AI_CONFIG_TOKEN:-}" ]; then WHY="AI_CONFIG_TOKEN is set but could not read washingtonshao-web/ai-config"
else WHY="no AI_CONFIG_TOKEN in this cloud environment"; fi

# Second choice: bundle.enc in this repo - the same content as the private repo, encrypted on the PCs; readable with
# the key in the environment variable AI_CONFIG_KEY (cloud environment settings). Third: the readable public copy.
BUNDLE=""
if [ ! -f $PRIV/claude/CLAUDE.md ] && [ -n "${AI_CONFIG_KEY:-}" ] && [ -f $DIR/bundle.enc ]; then
  BUNDLE=$(mktemp -d)
  if ! openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 -pass env:AI_CONFIG_KEY -in $DIR/bundle.enc \
       | tar -xz -C "$BUNDLE" 2>/dev/null || [ ! -f "$BUNDLE/CLAUDE.md" ]; then
    rm -rf "$BUNDLE"; BUNDLE=""; WHY="AI_CONFIG_KEY is set but does not decrypt bundle.enc"
  fi
fi

if [ -f $PRIV/claude/CLAUDE.md ]; then
  # 1. Global instructions (shared-block markers dropped) + cloud notes
  sed -E '/^<!-- \/?shared:[A-Za-z0-9_-]+ -->\r?$/d' $PRIV/claude/CLAUDE.md > ~/.claude/CLAUDE.md
  if [ -f $PRIV/cloud/cloud-notes.md ]; then cat $PRIV/cloud/cloud-notes.md >> ~/.claude/CLAUDE.md
  elif [ -f $DIR/cloud-notes.md ]; then cat $DIR/cloud-notes.md >> ~/.claude/CLAUDE.md; fi
  # 2. All Claude skills from the private repo, except PC-only ones
  for s in $PRIV/skills/claude/*/; do
    n=$(basename "$s"); case " $PC_ONLY " in *" $n "*) continue;; esac
    rm -rf ~/.claude/skills/"$n"; cp -r "$s" ~/.claude/skills/"$n"
  done
  [ -d $PRIV/kit ] && rm -rf $DIR/kit && cp -r $PRIV/kit $DIR/kit
  echo "private repo ai-config" > ~/.claude/.config-source
elif [ -n "$BUNDLE" ]; then
  # 1-2. CLAUDE.md (cloud notes included) and every non-PC-only Claude skill, from the decrypted bundle
  cp "$BUNDLE/CLAUDE.md" ~/.claude/CLAUDE.md
  for s in "$BUNDLE"/skills/*/; do
    [ -d "$s" ] || continue; n=$(basename "$s"); rm -rf ~/.claude/skills/"$n"; cp -r "$s" ~/.claude/skills/"$n"
  done
  [ -d "$BUNDLE/kit" ] && rm -rf $DIR/kit && cp -r "$BUNDLE/kit" $DIR/kit
  echo "encrypted mirror (bundle.enc)" > ~/.claude/.config-source
elif [ -f $DIR/webclaude.md ]; then
  # 1. Global instructions: local CLAUDE.md + cloud notes -> ~/.claude/CLAUDE.md
  cat $DIR/webclaude.md $DIR/cloud-notes.md > ~/.claude/CLAUDE.md
  # 2. Own skills: category folders in the repo, installed flat (~/.claude/skills/<name>/SKILL.md)
  for s in $DIR/skills/*/*/; do
    n=$(basename "$s"); rm -rf ~/.claude/skills/"$n"; cp -r "$s" ~/.claude/skills/"$n"
  done
  echo "public mirror ($WHY)" > ~/.claude/.config-source
else
  echo "none ($WHY; no readable copy in claude-config - set AI_CONFIG_KEY in the cloud environment)" > ~/.claude/.config-source
fi

# 2b. Workflows (deep-research.js ...) and selected settings (workflowSizeGuideline), from the same source as above
WF=$DIR/workflows; [ -n "$BUNDLE" ] && WF="$BUNDLE/workflows"; [ -d $PRIV/claude/workflows ] && WF=$PRIV/claude/workflows
if [ -d "$WF" ]; then mkdir -p ~/.claude/workflows && cp -r "$WF"/. ~/.claude/workflows/; fi
CS=$DIR/cloud/settings.json; [ -n "$BUNDLE" ] && CS="$BUNDLE/settings.json"
if [ -f "$CS" ]; then
  python3 - "$CS" <<'PY' || true
import json, os, sys
p = os.path.expanduser("~/.claude/settings.json")
s = json.load(open(p)) if os.path.exists(p) else {}
s.update(json.load(open(sys.argv[1])))
os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(s, open(p, "w"), indent=1)
PY
fi

[ -n "$BUNDLE" ] && rm -rf "$BUNDLE"
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
