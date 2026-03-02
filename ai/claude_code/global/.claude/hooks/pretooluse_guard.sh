#!/usr/bin/env bash
set -euo pipefail

input="$(cat)"

tool="$(jq -r '.tool_name // ""' <<<"$input")"
cmd="$(jq -r '.tool_input.command // ""' <<<"$input")"
cwd="$(jq -r '.cwd // ""' <<<"$input")"

[[ "$tool" == "Bash" ]] || exit 0
[[ -n "$cmd" ]] || exit 0

block() {
  echo "Blocked: $1" >&2
  echo "Command: $cmd" >&2
  exit 2
}

# fork bomb
if grep -Eq ':\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:' <<<"$cmd"; then
  block "fork bomb pattern"
fi

# destructive rm flags (rm -rf 等)。/bin/rm や command rm も「危険形だけ」止める
if grep -Eq '(^|[[:space:]])(\/bin\/rm|rm|command[[:space:]]+rm)[[:space:]]+.*(--force|--recursive|-rf|-fr)([[:space:]]|$)' <<<"$cmd"; then
  block "destructive rm flags"
fi

# dd if=
if grep -Eq '(^|[[:space:]])dd([[:space:]]|$).*if=' <<<"$cmd"; then
  block "dd if= pattern"
fi

# curl/wget piped to shell
if grep -Eq '(^|[[:space:]])(curl|wget)([[:space:]]|$).*?\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)' <<<"$cmd"; then
  block "download piped to shell"
fi

# $(curl/wget ...) を shell -c で実行する系
if grep -Eq '\$\([[:space:]]*(curl|wget)([[:space:]]|$)' <<<"$cmd"; then
  if grep -Eq '(^|[[:space:]])(sh|bash|zsh)[[:space:]]+-c([[:space:]]|$)' <<<"$cmd"; then
    block "shell -c with \$(curl/wget)"
  fi
fi

# git push ガード（force push と保護ブランチをブロック）
if grep -Eq '^git[[:space:]]+push([[:space:]]|$)' <<<"$cmd"; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease|-f)([[:space:]]|$)' <<<"$cmd"; then
    block "force push"
  fi

  # コマンドに main/master/develop/deploy が明示されている場合（origin main / HEAD:main 等）
  if grep -Eq '(^|[[:space:]]|:)(main|master|develop|deploy)([[:space:]]|$)' <<<"$cmd"; then
    block "push to protected branch (explicit)"
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
