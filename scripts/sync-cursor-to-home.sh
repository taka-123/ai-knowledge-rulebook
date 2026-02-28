#!/usr/bin/env bash
# sync-cursor-to-home.sh
# ai/cursor/global/agents を ~/.cursor/agents へ、
# ai/cursor/global/mcp.json を ~/.cursor/mcp.json へコピーする。
# 既存がある場合はディレクトリ/ファイル単位で日時付き .bak に退避してから上書きする。
#
# デフォルトでは mcp.json（MCP/認証設定）はコピー・退避しない。
# --include-mcp を指定した場合のみ含める。

set -euo pipefail

INCLUDE_MCP=false
for arg in "$@"; do
  case "$arg" in
    --include-mcp) INCLUDE_MCP=true ;;
    -h|--help)
      echo "Usage: $0 [--include-mcp]"
      echo "  --include-mcp  MCP/認証設定（mcp.json）もコピー・退避する"
      exit 0
      ;;
  esac
done

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

# mcp.json を ~/.cursor/mcp.json へコピー（--include-mcp 時のみ）
sync_mcp_json() {
  if [[ "$INCLUDE_MCP" != true ]]; then
    echo "スキップ: mcp.json（認証情報を含むため。--include-mcp で含める）"
    return
  fi
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
  echo "  1. 以下を開いて内容をコピーする:"
  echo "     ${SRC_COMMON_AGENTS}"
  echo "  2. Cursor 設定 (Cmd+, / Ctrl+,) > [Rules, Skills, Subagents] > Rules"
  echo "  3. User Rule に貼り付けて追加または編集"
  echo ""
}

main "$@"
