#!/usr/bin/env bash
# Windsurf pre_run_command / pre_mcp_tool_use guard.
# Exit 2 blocks the action. Exit 0 allows.
# Windsurf stdin: tool_info.command_line / tool_info.mcp_* （公式 Cascade Hooks）
set -euo pipefail

input="$(cat)"
cmd="$(printf '%s' "$input" | jq -r '.tool_info.command_line // empty' 2>/dev/null || true)"
cmd_scan="$(printf '%s' "$cmd" | tr -d "'\"")"

block() {
  echo "Blocked: $1" >&2
  exit 2
}

[[ -z "$cmd" ]] && exit 0

if grep -Eq '(^|[[:space:];|&])(/usr/bin/aws|/bin/aws|/sbin/aws|/usr/local/bin/aws|/opt/homebrew/bin/aws|aws)[[:space:]]' <<<"$cmd_scan"; then
  block "aws CLI (use AWS MCP Server)"
fi

if grep -Eq '(^|[[:space:];|&])(/usr/bin/gh|/bin/gh|/sbin/gh|/usr/local/bin/gh|/opt/homebrew/bin/gh|gh)[[:space:]]' <<<"$cmd_scan"; then
  block "gh CLI (use GitHub MCP Server)"
fi

if grep -Eq '(^|[[:space:];|&])(/usr/bin/git|/bin/git|/sbin/git|/usr/local/bin/git|/opt/homebrew/bin/git|git)[[:space:]]+push([[:space:]]|$)' <<<"$cmd_scan"; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease|-f)([[:space:]]|$)' <<<"$cmd_scan"; then
    block "force push"
  fi
fi

exit 0
