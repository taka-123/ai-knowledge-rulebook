#!/usr/bin/env bash
# sync-cursor-to-home.sh
# ai/cursor/global/agents を ~/.cursor/agents へ、
# ai/cursor/global/mcp.json を ~/.cursor/mcp.json へコピーする。
# 既存がある場合はディレクトリ/ファイル単位で日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_AGENTS="${PROJECT_ROOT}/ai/cursor/global/agents"
SRC_COMMON_AGENTS="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
SRC_MCP_JSON="${PROJECT_ROOT}/ai/cursor/global/mcp.json"
DEST_CURSOR="${HOME}/.cursor"
DEST_AGENTS="${HOME}/.cursor/agents"
DEST_MCP_JSON="${HOME}/.cursor/mcp.json"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BAK_SUFFIX=".bak.${TIMESTAMP}"

# 既存のディレクトリまたはファイルを日時付き .bak に退避
backup_if_exists() {
  local target="$1"
  if [[ -e "$target" ]]; then
    local bak="${target}${BAK_SUFFIX}"
    echo "退避: $target -> $bak"
    mv "$target" "$bak"
  fi
}

# agents ディレクトリを ~/.cursor/agents へコピー（既存はディレクトリごと退避）
sync_agents_dir() {
  if [[ ! -d "$SRC_AGENTS" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_AGENTS" >&2
    exit 1
  fi

  mkdir -p "$DEST_CURSOR"
  backup_if_exists "$DEST_AGENTS"
  mkdir -p "$DEST_AGENTS"
  rsync -a "$SRC_AGENTS/" "$DEST_AGENTS/"
  echo "コピー: ai/cursor/global/agents/* -> $DEST_AGENTS/"
}

# mcp.json を ~/.cursor/mcp.json へコピー
sync_mcp_json() {
  if [[ ! -f "$SRC_MCP_JSON" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_MCP_JSON" >&2
    exit 1
  fi

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
  echo ""
  echo "--- User Rule の設定 ---"
  echo "ai/common/global/AGENTS.md を Cursor の User Rule として設定することをお勧めします。"
  echo ""
  echo "手順:"
  echo "  1. Cursor 設定を開く (Cmd+, / Ctrl+,)"
  echo "  2. [Rules, Skills, Subagents] > Rules を選択"
  echo "  3. User Rule に以下を追加または編集:"
  echo ""
  if [[ -f "$SRC_COMMON_AGENTS" ]]; then
    echo "--- 以下をコピー ---"
    cat "$SRC_COMMON_AGENTS"
    echo ""
    echo "--- ここまで ---"
  else
    echo "  （ファイルが存在しません: ${SRC_COMMON_AGENTS}）"
  fi
  echo ""
}

main "$@"
