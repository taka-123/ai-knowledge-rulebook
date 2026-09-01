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

cmd_scan="$(printf '%s' "$cmd" | tr -d "'\"")"

if grep -Eq ':\(\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:[[:space:]]*&[[:space:]]*\}[[:space:]]*;[[:space:]]*:' <<<"$cmd_scan"; then
  block "fork bomb pattern"
fi

if grep -Eq '(^|[[:space:];|&])(command[[:space:]]+rm|/usr/bin/rm|/bin/rm|/sbin/rm|/usr/local/bin/rm|/opt/homebrew/bin/rm|rm)[[:space:]]+' <<<"$cmd_scan"; then
  if grep -Eq '(^|[[:space:]])(--force|--recursive|-rf|-fr|-r[[:space:]]+-f|-f[[:space:]]+-r)([[:space:]]|$)' <<<"$cmd_scan"; then
    if grep -Eq '(^|[[:space:]])(/|/\*|~|~/?\*|\$HOME|\$HOME/?\*|\.|\.\/|\.\.|\.\.\/)([[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm target"
    fi
    if grep -Eq '(^|[[:space:]])/(etc|bin|sbin|usr|var|System|Library|Applications|opt/homebrew)(/|\*|[[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm system path"
    fi
    if grep -Eq '(^|[[:space:]])(~/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$)|\$HOME/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$))' <<<"$cmd_scan"; then
      block "destructive rm protected home path"
    fi
  fi
fi

if grep -Eq '(^|[[:space:];|&])dd([[:space:]]|$).*([[:space:]]if=|[[:space:]]of=)' <<<"$cmd_scan"; then
  block "dd if/of pattern"
fi

if grep -Eq '(^|[[:space:];|&])(curl|wget)([[:space:]]|$).*?\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)' <<<"$cmd_scan"; then
  block "download piped to shell"
fi

if grep -Eq '(^|[[:space:];|&])(sh|bash|zsh)[[:space:]]+-c([[:space:]]|$)' <<<"$cmd_scan"; then
  if grep -Eq '\$\([[:space:]]*(curl|wget)([[:space:]]|$)' <<<"$cmd_scan"; then
    block "shell -c with download substitution"
  fi
fi

cli_command() {
  local name="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?${name}([[:space:]|;|&]|$)" <<<"$cmd"
}

git_push_command() {
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?git[[:space:]]+push([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_subcmd() {
  local sub="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?gh[[:space:]]+${sub}([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_api_has_field_flag() {
  grep -Eq '(^|[[:space:]])(--field|--raw-field)([[:space:]|=]|$)' <<<"$cmd" ||
    grep -Eq '(^|[[:space:]])-[fF]([[:space:]=]|[^[:space:]-])' <<<"$cmd"
}

gh_api_has_explicit_get() {
  grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+GET($|[[:space:];&)])' <<<"$cmd"
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
    if grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+(POST|PUT|PATCH|DELETE)([[:space:]]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    if grep -Eq '(^|[[:space:]])(--input)([[:space:]|=]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    if gh_api_has_field_flag && ! gh_api_has_explicit_get; then
      block "mutating gh api"
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
    block "push to protected branch"
  fi
  if grep -Eq 'refs/heads/(main|master|develop|deploy)([[:space:]:^~]|$)' <<<"$cmd"; then
    block "push to protected branch"
  fi
  if [[ -n "$cwd" ]] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch="$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [[ "$branch" =~ ^(main|master|develop|deploy)$ ]]; then
      block "push from protected branch '$branch'"
    fi
  fi
fi

exit 0
