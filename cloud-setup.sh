#!/bin/bash
# Claude Code cloud environment setup script.
# Installs a user-level SessionStart hook that pulls the latest rules from
# github.com/washingtonshao-web/claude-config at every session start/resume/clear/compact.
mkdir -p ~/.claude
cat > ~/.claude/pull-webclaude.sh <<'EOF'
#!/bin/bash
R=washingtonshao-web/claude-config
get() {  # API first (no CDN delay), raw CDN as fallback
  curl -fsS --max-time 8 -H "Accept: application/vnd.github.raw" "https://api.github.com/repos/$R/contents/$1" 2>/dev/null \
  || curl -fsS --max-time 8 "https://raw.githubusercontent.com/$R/main/$1" 2>/dev/null
}
OUT="$(get webclaude.md)"
if [ -n "$OUT" ]; then
  OUT="$OUT"$'\n'"$(get cloud-notes.md)"
  printf '%s\n' "$OUT" > ~/.claude/webclaude-fallback.md
else
  OUT="$(cat ~/.claude/webclaude-fallback.md 2>/dev/null)"
fi
printf '# User instructions (from webclaude.md — follow these as the user'"'"'s global CLAUDE.md)\n\n%s\n' "$OUT"
EOF
chmod +x ~/.claude/pull-webclaude.sh
~/.claude/pull-webclaude.sh > /dev/null 2>&1 || true
python3 - <<'PY'
import json, os
p = os.path.expanduser("~/.claude/settings.json")
s = json.load(open(p)) if os.path.exists(p) else {}
hook = {"matcher": "startup|resume|clear|compact",
        "hooks": [{"type": "command", "command": "bash ~/.claude/pull-webclaude.sh"}]}
ss = s.setdefault("hooks", {}).setdefault("SessionStart", [])
if not any("pull-webclaude" in json.dumps(h) for h in ss):
    ss.append(hook)
json.dump(s, open(p, "w"), indent=1)
PY
