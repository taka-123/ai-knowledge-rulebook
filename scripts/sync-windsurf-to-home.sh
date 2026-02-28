#!/usr/bin/env bash
# sync-windsurf-to-home.sh
# ai/windsurf/global/mcp_config.json を ~/.codeium/windsurf/mcp_config.json へ、
# ai/common/global/AGENTS.md を ~/.codeium/windsurf/memories/global_rules.md へコピーする。
# 既存ファイルがある場合は日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_MCP="${PROJECT_ROOT}/ai/windsurf/global/mcp_config.json"
SRC_COMMON_AGENTS="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
DEST_MCP="${HOME}/.codeium/windsurf/mcp_config.json"
DEST_GLOBAL_RULES="${HOME}/.codeium/windsurf/memories/global_rules.md"
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
  echo "=== sync-windsurf-to-home ==="
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
  if [[ ! -f "$SRC_COMMON_AGENTS" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_COMMON_AGENTS" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$DEST_GLOBAL_RULES")"
  backup_if_exists "$DEST_GLOBAL_RULES"
  cp -p "$SRC_COMMON_AGENTS" "$DEST_GLOBAL_RULES"
  echo "コピー: AGENTS.md (common) -> $DEST_GLOBAL_RULES"

  echo ""
  echo "完了しました。"
}

main "$@"
