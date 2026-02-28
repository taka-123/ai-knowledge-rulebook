#!/usr/bin/env bash
# sync-claude-to-home.sh
# ai/claude_code/global を ~/.claude/ へ、
# ai/claude_code/claude.json を ~/.claude.json へコピーする。
# 既存ファイルがある場合は日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_GLOBAL="${PROJECT_ROOT}/ai/claude_code/global"
SRC_CLAUDE_JSON="${PROJECT_ROOT}/ai/claude_code/claude.json"
DEST_CLAUDE="${HOME}/.claude"
DEST_CLAUDE_JSON="${HOME}/.claude.json"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

# 既存ファイルを日時付き .bak に退避
backup_if_exists() {
  local target="$1"
  if [[ -e "$target" ]]; then
    local bak="${target}.${TIMESTAMP}.bak"
    echo "退避: $target -> $bak"
    mv "$target" "$bak"
  fi
}

# global ディレクトリを ~/.claude へコピー（既存は退避）
sync_global_dir() {
  if [[ ! -d "$SRC_GLOBAL" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_GLOBAL" >&2
    exit 1
  fi

  mkdir -p "$DEST_CLAUDE"

  while IFS= read -r -d '' relpath; do
    local src="${SRC_GLOBAL}/${relpath}"
    local dest="${DEST_CLAUDE}/${relpath}"

    if [[ -d "$src" ]]; then
      backup_if_exists "$dest"
      mkdir -p "$dest"
    else
      local dest_dir
      dest_dir="$(dirname "$dest")"
      mkdir -p "$dest_dir"
      backup_if_exists "$dest"
      cp -p "$src" "$dest"
      echo "コピー: $relpath"
    fi
  done < <(cd "$SRC_GLOBAL" && find . -mindepth 1 -print0 | sort -z)
}

# claude.json を ~/.claude.json へコピー
sync_claude_json() {
  if [[ ! -f "$SRC_CLAUDE_JSON" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_CLAUDE_JSON" >&2
    exit 1
  fi

  backup_if_exists "$DEST_CLAUDE_JSON"
  cp -p "$SRC_CLAUDE_JSON" "$DEST_CLAUDE_JSON"
  echo "コピー: claude.json -> $DEST_CLAUDE_JSON"
}

main() {
  echo "=== sync-claude-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  sync_global_dir
  echo ""
  sync_claude_json

  echo ""
  echo "完了しました。"
}

main "$@"
