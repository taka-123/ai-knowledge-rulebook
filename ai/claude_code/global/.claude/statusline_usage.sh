#!/bin/bash
# ~/.claude/statusline_usage.sh
# Claude Code usage gauge for statusline
# Shows 5-hour, 7-day limits and extra usage with visual progress bars

CACHE_FILE="/tmp/claude_usage_cache.txt"
CACHE_TTL=600

# --- Cache check ---
if [[ -f "$CACHE_FILE" ]]; then
  age=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE") ))
  if (( age < CACHE_TTL )); then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# --- OAuth token from macOS Keychain ---
TOKEN=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null \
  | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('claudeAiOauth', {}).get('accessToken', ''))
except: pass
" 2>/dev/null)

if [[ -z "$TOKEN" ]]; then
  echo "usage: --"
  exit 0
fi

# --- Fetch usage API ---
RESP=$(curl -s --max-time 5 \
  -H "Authorization: Bearer $TOKEN" \
  -H "anthropic-beta: oauth-2025-04-20" \
  "https://api.anthropic.com/api/oauth/usage" 2>/dev/null)

if [[ -z "$RESP" ]] || echo "$RESP" | grep -q '"error"'; then
  # API error or rate limited — use stale cache if available, else show fallback
  if [[ -f "$CACHE_FILE" ]]; then
    cat "$CACHE_FILE"
  else
    echo "usage: ..."
  fi
  exit 0
fi

# --- Format with progress bar ---
OUTPUT=$(echo "$RESP" | python3 -c '
import sys, json
from datetime import datetime, timezone

try:
    d = json.load(sys.stdin)
except:
    print("usage: --")
    sys.exit()

def make_bar(pct, width=8):
    filled = round(pct / 100 * width)
    empty = width - filled
    return "\u2588" * filled + "\u2591" * empty

def fmt_reset(resets_at):
    if not resets_at:
        return ""
    try:
        reset = datetime.fromisoformat(resets_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = reset - now
        secs = max(int(delta.total_seconds()), 0)
        if secs >= 86400:
            days = secs // 86400
            hours = (secs % 86400) // 3600
            return f"{days}d{hours}h"
        elif secs >= 3600:
            hours = secs // 3600
            mins = (secs % 3600) // 60
            return f"{hours}h{mins:02d}m"
        else:
            mins = secs // 60
            return f"{mins}m"
    except:
        return ""

parts = []
h5 = d.get("five_hour")
d7 = d.get("seven_day")
extra = d.get("extra_usage")

if h5:
    pct = min(round(h5["utilization"] * 100), 100)
    bar = make_bar(pct)
    reset = fmt_reset(h5.get("resets_at"))
    reset_str = f"({reset})" if reset else ""
    parts.append(f"5h {bar} {pct:>3d}%{reset_str}")

if d7:
    pct = min(round(d7["utilization"] * 100), 100)
    bar = make_bar(pct)
    reset = fmt_reset(d7.get("resets_at"))
    reset_str = f"({reset})" if reset else ""
    parts.append(f"7d {bar} {pct:>3d}%{reset_str}")

if extra and extra.get("is_enabled"):
    pct = min(round(extra.get("utilization", 0)), 100)
    used = extra.get("used_credits", 0)
    limit = extra.get("monthly_limit", 0)
    bar = make_bar(pct)
    parts.append(f"ex {bar} {pct}% ${used:.0f}/${limit}")

print(" | ".join(parts) if parts else "usage: --")
' 2>/dev/null)

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="usage: --"
fi

echo "$OUTPUT" > "$CACHE_FILE"
echo "$OUTPUT"
