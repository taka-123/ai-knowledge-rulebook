#!/usr/bin/env bash
# sync-gemini-to-home.sh
# ai/antigravity/gemini/antigravity/mcp_config.json を ~/.gemini/antigravity/mcp_config.json へコピーする。
# 既存ファイルがある場合は日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_MCP="${PROJECT_ROOT}/ai/antigravity/gemini/antigravity/mcp_config.json"
DEST_MCP="${HOME}/.gemini/antigravity/mcp_config.json"
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

main() {
  echo "=== sync-gemini-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  if [[ ! -f "$SRC_MCP" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_MCP" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$DEST_MCP")"
  backup_if_exists "$DEST_MCP"
  cp -p "$SRC_MCP" "$DEST_MCP"
  echo "コピー: mcp_config.json -> $DEST_MCP"

  echo ""
  echo "完了しました。"
}

main "$@"
