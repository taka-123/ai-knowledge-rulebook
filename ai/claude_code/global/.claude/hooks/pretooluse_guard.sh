#!/usr/bin/env bash
set -euo pipefail

input="$(cat)"
tool="$(jq -r '.tool_name // ""' <<<"$input")"
cmd="$(jq -r '.tool_input.command // ""' <<<"$input")"
cwd="$(jq -r '.cwd // ""' <<<"$input")"
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

# git push ガード
if grep -Eq '(^|[[:space:];|&])(/usr/bin/git|/bin/git|/sbin/git|/usr/local/bin/git|/opt/homebrew/bin/git|git)[[:space:]]+push([[:space:]]|$)' <<<"$cmd_scan"; then
  # force push は常にブロック
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease|-f)([[:space:]]|$)' <<<"$cmd_scan"; then
    block "force push"
  fi

  # コマンドに main/master/develop/deploy が明示されている場合
  if grep -Eq '(^|[[:space:]]|:)(main|master|develop|deploy)([[:space:]]|$)' <<<"$cmd_scan"; then
    block "push to protected branch (explicit)"
  fi

  # refspec 形式の保護ブランチ指定
  if grep -Eq 'refs/heads/(main|master|develop|deploy)([[:space:]:^~]|$)' <<<"$cmd_scan"; then
    block "push to protected branch (refspec)"
  fi

  # 現在ブランチが保護対象ならブロック
  if [[ -n "$cwd" ]] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch="$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [[ "$branch" =~ ^(main|master|develop|deploy)$ ]]; then
      block "push from protected branch '$branch'"
    fi
  fi
fi

exit 0
