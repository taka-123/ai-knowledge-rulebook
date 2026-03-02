#!/usr/bin/env bash
set -euo pipefail
if ! command -v jq >/dev/null 2>&1; then echo "jq not found; skip"; exit 0; fi
payload="$(cat)"
url="$(echo "$payload" | jq -r '.url // empty')"
host="$(echo "$url" | sed -E 's#^[a-z]+://([^/]+)/?.*$#\1#')"
path="$(echo "$url" | sed -E 's#^[a-z]+://[^/]+(/.*)?$#\1#')"
ROOT="${CLAUDE_PROJECT_DIR:-.}"
ALLOW="$ROOT/.claude/hooks/validate-webfetch.allow"
DENY="$ROOT/.claude/hooks/validate-webfetch.deny"
if [[ -f "$DENY" ]] && grep -Eiq "$(paste -sd'|' "$DENY")" <<< "${host}${path}"; then echo "blocked by denylist: $url" >&2; exit 2; fi
if grep -Eiq '/(auth|login|password|secret|token|admin)\b' <<< "${path}"; then echo "blocked suspicious path: $url" >&2; exit 2; fi
if grep -Eiq '/api/v[0-9]+/auth' <<< "${path}"; then echo "blocked api auth path: $url" >&2; exit 2; fi
if [[ -f "$ALLOW" ]]; then
  if grep -Eiq "$(paste -sd'|' "$ALLOW")" <<< "${host}${path}"; then exit 0; fi
  # 厳格運用したい場合は次行のコメントを外す
  # echo "not in allowlist: $url" >&2; exit 2
fi
exit 0
