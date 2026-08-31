#!/usr/bin/env bash
set -euo pipefail

input="$(cat)"
if ! tool="$(jq -r '.tool_name // ""' <<<"$input")" \
  || ! cmd="$(jq -r '.tool_input.command // ""' <<<"$input")" \
  || ! cwd="$(jq -r '.cwd // ""' <<<"$input")"; then
  echo "Blocked: hook parse failed" >&2
  exit 2
fi
cmd_scan="$(printf '%s' "$cmd" | tr -d "'\"")"

[[ "$tool" == "Bash" ]] || exit 0
[[ -n "$cmd" ]] || exit 0

block() {
  echo "Blocked: $1" >&2
  echo "Command: $cmd" >&2
  exit 2
}

# fork bomb
if grep -Eq ':\(\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:[[:space:]]*&[[:space:]]*\}[[:space:]]*;[[:space:]]*:' <<<"$cmd_scan"; then
  block "fork bomb pattern"
fi

# rm -rf / rm -fr / rm --recursive --force のうち、危険な削除対象だけ止める。
# プロジェクト内の rm -rf ./dist, ./build, ./node_modules, ./.claude/skills/foo などは sandbox に任せる。
if grep -Eq '(^|[[:space:];|&])(command[[:space:]]+rm|/usr/bin/rm|/bin/rm|/sbin/rm|/usr/local/bin/rm|/opt/homebrew/bin/rm|rm)[[:space:]]+' <<<"$cmd_scan"; then
  if grep -Eq '(^|[[:space:]])(--force|--recursive|-rf|-fr|-r[[:space:]]+-f|-f[[:space:]]+-r)([[:space:]]|$)' <<<"$cmd_scan"; then
    # ルート、ホーム、カレント全体、親ディレクトリ全体
    if grep -Eq '(^|[[:space:]])(/|/\*|~|~/?\*|\$HOME|\$HOME/?\*|\.|\.\/|\.\.|\.\.\/)([[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm target"
    fi

    # macOS / Unix の重要ディレクトリ
    if grep -Eq '(^|[[:space:]])/(etc|bin|sbin|usr|var|System|Library|Applications|opt/homebrew)(/|\*|[[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm system path"
    fi

    # ユーザーホーム直下全体や主要設定ディレクトリ
    if grep -Eq '(^|[[:space:]])(~/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$)|\$HOME/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$))' <<<"$cmd_scan"; then
      block "destructive rm protected home path"
    fi
  fi
fi

# dd if= / of= はディスク破壊・大量上書きリスクが高いので止める
if grep -Eq '(^|[[:space:];|&])dd([[:space:]]|$).*([[:space:]]if=|[[:space:]]of=)' <<<"$cmd_scan"; then
  block "dd if/of pattern"
fi

# curl/wget piped to shell
if grep -Eq '(^|[[:space:];|&])(curl|wget)([[:space:]]|$).*?\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)' <<<"$cmd_scan"; then
  block "download piped to shell"
fi

# sh -c "$(curl ...)" / bash -c "$(wget ...)" 系
if grep -Eq '(^|[[:space:];|&])(sh|bash|zsh)[[:space:]]+-c([[:space:]]|$)' <<<"$cmd_scan"; then
  if grep -Eq '\$\([[:space:]]*(curl|wget)([[:space:]]|$)' <<<"$cmd_scan"; then
    block "shell -c with download substitution"
  fi
fi

# コマンド位置の aws を抑止。gh は危険サブコマンドだけ止める（引用符は剥がさない。SDK は対象外）
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
    # Bind GET to the same gh api invocation; a later GET must not authorize an earlier mutation.
    # Compound ( { and command/process substitution nest gh api; split those too.
    if grep -Eq -- '(-[fF]|--field|--raw-field|--input)([[:space:]|=]|$)' <<<"$cmd" &&
      grep -Eq '`|\$\(|<\(|>\(' <<<"$cmd"; then
      block "mutating gh api"
    fi
    # Fail closed: extra or expanded -X/--method can override a literal GET (gh last-wins).
    if grep -Eq -- '(-[fF]|--field|--raw-field|--input)([[:space:]|=]|$)' <<<"$cmd"; then
      if grep -Eqi '(^|[[:space:]])(-X|--method)(=|[[:space:]]+)\$' <<<"$cmd" ||
        grep -Eqi '(^|[[:space:]])(-X|--method)(=|[[:space:]]*)"\$' <<<"$cmd" ||
        grep -Eqi '(^|[[:space:]])(-X|--method)=\$' <<<"$cmd"; then
        block "mutating gh api"
      fi
      _gh_method_n="$(grep -Eo -- '-X|--method' <<<"$cmd" | wc -l | tr -d ' ')" || true
      if [ "${_gh_method_n:-0}" -gt 1 ]; then
        block "mutating gh api"
      fi
      # Fail closed: standalone $var / $@ / $* / $1 can expand to -X POST.
      if grep -Eq '(^|[[:space:]])\$[{A-Za-z_@*0-9]' <<<"$cmd" ||
        grep -Eq '(^|[[:space:]])"\$[{A-Za-z_@*0-9]' <<<"$cmd" ||
        grep -Eq "(^|[[:space:]])'\\\$[{A-Za-z_@*0-9]" <<<"$cmd"; then
        block "mutating gh api"
      fi
      # Fail closed: backslash-escaped tokens can become -X POST after shell parse.
      if grep -Eq '\\' <<<"$cmd"; then
        block "mutating gh api"
      fi
    fi
    while IFS= read -r _gh_api_seg; do
      if ! grep -Eq '(^|[[:space:]])([^[:space:]"'\'']*/)?gh[[:space:]]+api([[:space:]|;|&]|$)' <<<"$_gh_api_seg"; then
        continue
      fi
      if grep -Eq '(^|[[:space:]])(-[fF]|--field|--raw-field)([[:space:]|=]|$)' <<<"$_gh_api_seg"; then
        _method_n=$(grep -Eoi -- '(-X|--method)[[:space:]]+' <<<"$_gh_api_seg" | grep -c . || true)
        if [ "${_method_n:-0}" -gt 1 ]; then
          block "mutating gh api"
        fi
        if ! grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+GET([[:space:]|;|&]|$)' <<<"$_gh_api_seg"; then
          block "mutating gh api"
        fi
      fi
    done < <(printf '%s\n' "$cmd" | tr ';|&(){}' '\n')
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
