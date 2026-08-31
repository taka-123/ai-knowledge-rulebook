#!/usr/bin/env bash
# Cursor beforeShellExecution guard (user global: ~/.cursor)。
# stdin: Cursor hook JSON. stdout: {"permission":"allow"|"deny"|"ask","user_message":"..."}
# MCP 制限は X-MCP-Tools（server-side）に任せる。Cloud では本ファイルは効かない → project 側を使う。
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

# コマンド位置（先頭、または ;|&(){} $() backtick の直後）。引用符は剥がさない。
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

if cli_command aws; then
  deny "Use AWS MCP Server instead of aws CLI."
fi

if cli_command gh; then
  if gh_subcmd 'pr[[:space:]]+(merge|review)'; then
    deny "Forbidden gh command: pr merge/review."
  fi
  if gh_subcmd 'workflow[[:space:]]+run'; then
    deny "Forbidden gh command: workflow run."
  fi
  if gh_subcmd 'run[[:space:]]+rerun'; then
    deny "Forbidden gh command: run rerun."
  fi
  if gh_subcmd 'repo[[:space:]]+(delete|archive|edit)'; then
    deny "Forbidden gh command: repository admin."
  fi
  if gh_subcmd 'auth[[:space:]]+(token|login|logout|refresh)'; then
    deny "Forbidden gh command: auth token/login/logout/refresh."
  fi
  if gh_subcmd 'api'; then
    if grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+(POST|PUT|PATCH|DELETE)([[:space:]|;|&]|$)' <<<"$cmd"; then
      deny "Mutating gh api is forbidden."
    fi
    if grep -Eq '(^|[[:space:]])(--input)([[:space:]|=]|$)' <<<"$cmd"; then
      deny "Mutating gh api is forbidden."
    fi
    # -f/--field on explicit GET are query params (official babysit-pr watcher).
    # Bind GET to the same gh api invocation; a later GET must not authorize an earlier mutation.
    # Compound ( { and command/process substitution nest gh api; split those too.
    if grep -Eq -- '(-[fF]|--field|--raw-field|--input)([[:space:]|=]|$)' <<<"$cmd" &&
      grep -Eq '`|\$\(|<\(|>\(' <<<"$cmd"; then
      deny "Mutating gh api is forbidden."
    fi
    # Fail closed: extra or expanded -X/--method can override a literal GET (gh last-wins).
    if grep -Eq -- '(-[fF]|--field|--raw-field|--input)([[:space:]|=]|$)' <<<"$cmd"; then
      if grep -Eqi '(^|[[:space:]])(-X|--method)(=|[[:space:]]+)\$' <<<"$cmd" ||
        grep -Eqi '(^|[[:space:]])(-X|--method)(=|[[:space:]]*)"\$' <<<"$cmd" ||
        grep -Eqi '(^|[[:space:]])(-X|--method)=\$' <<<"$cmd"; then
        deny "Mutating gh api is forbidden."
      fi
      _gh_method_n="$(grep -Eo -- '-X|--method' <<<"$cmd" | wc -l | tr -d ' ')" || true
      if [ "${_gh_method_n:-0}" -gt 1 ]; then
        deny "Mutating gh api is forbidden."
      fi
    fi
    while IFS= read -r _gh_api_seg; do
      if ! grep -Eq '(^|[[:space:]])([^[:space:]"'\'']*/)?gh[[:space:]]+api([[:space:]|;|&]|$)' <<<"$_gh_api_seg"; then
        continue
      fi
      if grep -Eq '(^|[[:space:]])(-[fF]|--field|--raw-field)([[:space:]|=]|$)' <<<"$_gh_api_seg"; then
        _method_n=$(grep -Eoi -- '(-X|--method)[[:space:]]+' <<<"$_gh_api_seg" | grep -c . || true)
        if [ "${_method_n:-0}" -gt 1 ]; then
          deny "Mutating gh api is forbidden."
        fi
        if ! grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+GET([[:space:]|;|&]|$)' <<<"$_gh_api_seg"; then
          deny "Mutating gh api is forbidden."
        fi
      fi
    done < <(printf '%s\n' "$cmd" | tr ';|&(){}' '\n')
  fi
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
