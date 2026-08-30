#!/usr/bin/env bash
# Windsurf pre_run_command / pre_mcp_tool_use guard.
# Exit 2 blocks the action. Exit 0 allows.
# Windsurf stdin: tool_info.command_line / tool_info.mcp_* （公式 Cascade Hooks）
# CLI 起動の best-effort 抑止。SDK・未列挙ラッパは対象外（IAM / Rulesets が本丸）。
# pre_mcp_tool_use は command_line が空なので通過する。MCP 制限は X-MCP-Tools 側。
set -euo pipefail

input="$(cat)"

block() {
  echo "Blocked: $1" >&2
  exit 2
}

cmd="$(jq -r '.tool_info.command_line // empty' <<<"$input")" || block "hook input parse failed"
cwd="$(jq -r '.cwd // .tool_info.cwd // empty' <<<"$input")" || cwd=""

[[ -z "$cmd" ]] && exit 0

cli_command() {
  local name="$1"
  grep -Eq "(^|[;|&]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?${name}([[:space:]|;|&]|$)" <<<"$cmd"
}

git_push_command() {
  grep -Eq "(^|[;|&]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?git[[:space:]]+push([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_subcmd() {
  local sub="$1"
  grep -Eq "(^|[;|&]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?gh[[:space:]]+${sub}([[:space:]|;|&]|$)" <<<"$cmd"
}

if cli_command aws; then
  block "aws CLI (use AWS MCP Server)"
fi

if cli_command gh; then
  if gh_subcmd 'pr[[:space:]]+(merge|review)'; then
    block "dangerous gh command (pr merge/review)"
  fi
  if gh_subcmd 'workflow[[:space:]]+run'; then
    block "dangerous gh command (workflow run)"
  fi
  if gh_subcmd 'run[[:space:]]+rerun'; then
    block "dangerous gh command (run rerun)"
  fi
  if gh_subcmd 'repo[[:space:]]+(delete|archive|edit)'; then
    block "dangerous gh command (repo admin)"
  fi
  if gh_subcmd 'auth[[:space:]]+(token|login|logout|refresh)'; then
    block "dangerous gh command (auth)"
  fi
  if gh_subcmd 'api'; then
    if grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+(POST|PUT|PATCH|DELETE)([[:space:]|;|&]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    if grep -Eq '(^|[[:space:]])(--input)([[:space:]|=]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    # -f/--field on explicit GET are query params (official babysit-pr watcher).
    # Unspecified method + -f stays denied so `gh api graphql -f` remains blocked.
    if grep -Eq '(^|[[:space:]])(-[fF]|--field|--raw-field)([[:space:]|=]|$)' <<<"$cmd"; then
      if ! grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+GET([[:space:]|;|&]|$)' <<<"$cmd"; then
        block "mutating gh api"
      fi
    fi
  fi
fi

if git_push_command; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease)(=|[[:space:]]|$)' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]]([^;&|]*[[:space:]])?-f([[:space:]|=]|$)' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]][^;&|]*\+[A-Za-z0-9._/-]+' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq '(^|[[:space:]]|:)(main|master|develop|deploy)([[:space:]]|$)' <<<"$cmd"; then
    block "push to protected branch (explicit)"
  fi
  if grep -Eq 'refs/heads/(main|master|develop|deploy)([[:space:]:^~]|$)' <<<"$cmd"; then
    block "push to protected branch (refspec)"
  fi
  if [[ -n "$cwd" ]] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch="$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [[ "$branch" =~ ^(main|master|develop|deploy)$ ]]; then
      block "push from protected branch '$branch'"
    fi
  fi
fi

exit 0
