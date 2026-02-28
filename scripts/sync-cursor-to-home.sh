#!/usr/bin/env bash
# sync-cursor-to-home.sh
# ai/cursor/global/agents を ~/.cursor/ へ、
# ai/cursor/global/mcp.json を ~/.cursor/mcp.json へコピーする。
# 既存ファイルがある場合は日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_AGENTS="${PROJECT_ROOT}/ai/cursor/global/agents"
SRC_MCP_JSON="${PROJECT_ROOT}/ai/cursor/global/mcp.json"
DEST_CURSOR="${HOME}/.cursor"
DEST_MCP_JSON="${HOME}/.cursor/mcp.json"
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

# agents ディレクトリを ~/.cursor へコピー（既存は退避）
sync_agents_dir() {
  if [[ ! -d "$SRC_AGENTS" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_AGENTS" >&2
    exit 1
  fi

  mkdir -p "$DEST_CURSOR"

  while IFS= read -r -d '' relpath; do
    local src="${SRC_AGENTS}/${relpath}"
    local dest="${DEST_CURSOR}/agents/${relpath}"

    if [[ -d "$src" ]]; then
      backup_if_exists "$dest"
      mkdir -p "$dest"
    else
      local dest_dir
      dest_dir="$(dirname "$dest")"
      mkdir -p "$dest_dir"
      backup_if_exists "$dest"
      cp -p "$src" "$dest"
      echo "コピー: agents/$relpath"
    fi
  done < <(cd "$SRC_AGENTS" && find . -mindepth 1 -print0 | sort -z)
}

# mcp.json を ~/.cursor/mcp.json へコピー
sync_mcp_json() {
  if [[ ! -f "$SRC_MCP_JSON" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_MCP_JSON" >&2
    exit 1
  fi

  mkdir -p "$DEST_CURSOR"
  backup_if_exists "$DEST_MCP_JSON"
  cp -p "$SRC_MCP_JSON" "$DEST_MCP_JSON"
  echo "コピー: mcp.json -> $DEST_MCP_JSON"
}

main() {
  echo "=== sync-cursor-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  sync_agents_dir
  echo ""
  sync_mcp_json

  echo ""
  echo "完了しました。"
}

main "$@"
