#!/usr/bin/env bash
# Cursor beforeShellExecution guard (project / Cloud Agent 向け)。
# プロジェクトルート相対で実行される。stdin: Cursor hook JSON。
# stdout: {"permission":"allow"|"deny"|"ask","user_message":"..."}
set -euo pipefail

input="$(cat)"
cmd="$(printf '%s' "$input" | jq -r '.command // .tool_input.command // empty' 2>/dev/null || true)"
cmd_scan="$(printf '%s' "$cmd" | tr -d "'\"")"

deny() {
  jq -n --arg msg "$1" '{permission:"deny",user_message:$msg}'
  exit 0
}

allow() {
  echo '{"permission":"allow"}'
  exit 0
}

[[ -z "$cmd" ]] && allow

# aws CLI
if grep -Eq '(^|[[:space:];|&])(/usr/bin/aws|/bin/aws|/sbin/aws|/usr/local/bin/aws|/opt/homebrew/bin/aws|aws)[[:space:]]' <<<"$cmd_scan"; then
  deny "Use AWS MCP Server instead of aws CLI."
fi

# gh CLI
if grep -Eq '(^|[[:space:];|&])(/usr/bin/gh|/bin/gh|/sbin/gh|/usr/local/bin/gh|/opt/homebrew/bin/gh|gh)[[:space:]]' <<<"$cmd_scan"; then
  deny "Use GitHub MCP Server instead of gh CLI."
fi

# force push
if grep -Eq '(^|[[:space:];|&])(/usr/bin/git|/bin/git|/sbin/git|/usr/local/bin/git|/opt/homebrew/bin/git|git)[[:space:]]+push([[:space:]]|$)' <<<"$cmd_scan"; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease|-f)([[:space:]]|$)' <<<"$cmd_scan"; then
    deny "Force push is forbidden for AI agents."
  fi
fi

allow
