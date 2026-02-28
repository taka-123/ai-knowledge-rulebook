#!/usr/bin/env bash
# sync-codex-to-home.sh
# ai/openai_codex/global 以下を ~/.codex/ へコピーする。
# 既存ファイルがある場合は日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_GLOBAL="${PROJECT_ROOT}/ai/openai_codex/global"
DEST_CODEX="${HOME}/.codex"
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

# global ディレクトリを ~/.codex へコピー（既存は退避）
sync_global_dir() {
  if [[ ! -d "$SRC_GLOBAL" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_GLOBAL" >&2
    exit 1
  fi

  mkdir -p "$DEST_CODEX"

  while IFS= read -r -d '' relpath; do
    local src="${SRC_GLOBAL}/${relpath}"
    local dest="${DEST_CODEX}/${relpath}"

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

main() {
  echo "=== sync-codex-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  sync_global_dir

  echo ""
  echo "完了しました。"
}

main "$@"
