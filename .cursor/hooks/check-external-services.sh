#!/usr/bin/env bash
# Cursor beforeShellExecution guard (project / Cloud Agent 向け)。
# プロジェクトルート相対で実行される。stdin: Cursor hook JSON。
# stdout: {"permission":"allow"|"deny"|"ask","user_message":"..."}
# CLI 起動の best-effort 抑止。SDK・未列挙ラッパは対象外（IAM / Rulesets が本丸）。
set -euo pipefail

input="$(cat)"

deny() {
  jq -n --arg msg "$1" '{permission:"deny",user_message:$msg}'
  exit 0
}

allow() {
  echo '{"permission":"allow"}'
  exit 0
}

cmd="$(jq -r '.command // .tool_input.command // empty' <<<"$input")" || deny "hook input parse failed"
cwd="$(jq -r '.cwd // empty' <<<"$input")" || cwd=""

[[ -z "$cmd" ]] && allow

# コマンド位置（先頭、または ;|& $() backtick の直後）。引用符は剥がさない。
cli_command() {
  local name="$1"
  grep -Eq "(^|[;|&]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?${name}([[:space:]|;|&]|$)" <<<"$cmd"
}

git_push_command() {
  grep -Eq "(^|[;|&]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?git[[:space:]]+push([[:space:]|;|&]|$)" <<<"$cmd"
}

if cli_command aws; then
  deny "Use AWS MCP Server instead of aws CLI."
fi

if cli_command gh; then
  deny "Use GitHub MCP Server instead of gh CLI."
fi

if git_push_command; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease)(=|[[:space:]]|$)' <<<"$cmd"; then
    deny "Force push is forbidden for AI agents."
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]]([^;&|]*[[:space:]])?-f([[:space:]|=]|$)' <<<"$cmd"; then
    deny "Force push is forbidden for AI agents."
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]][^;&|]*\+[A-Za-z0-9._/-]+' <<<"$cmd"; then
    deny "Force push is forbidden for AI agents."
  fi
  if grep -Eq '(^|[[:space:]]|:)(main|master|develop|deploy)([[:space:]]|$)' <<<"$cmd"; then
    deny "Push to protected branch is forbidden for AI agents."
  fi
  if grep -Eq 'refs/heads/(main|master|develop|deploy)([[:space:]:^~]|$)' <<<"$cmd"; then
    deny "Push to protected branch is forbidden for AI agents."
  fi
  if [[ -n "$cwd" ]] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch="$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [[ "$branch" =~ ^(main|master|develop|deploy)$ ]]; then
      deny "Push from protected branch '$branch' is forbidden for AI agents."
    fi
  fi
fi

allow
