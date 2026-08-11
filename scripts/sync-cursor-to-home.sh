#!/usr/bin/env bash
# sync-cursor-to-home.sh
# ai/cursor/global/.cursor/agents を ~/.cursor/agents へ、
# ai/cursor/global/.cursor/hooks.json と hooks/ を ~/.cursor/ へ、
# ai/cursor/global/.cursor/mcp.json を ~/.cursor/mcp.json へコピーする。
# 既存がある場合はバックアップディレクトリへ退避してから上書きする。
#
# デフォルトでは mcp.json（MCP/認証設定）はコピー・退避しない。
# --include-mcp を指定した場合のみ含める。
# hooks.json / hooks/ は常に同期する（秘密情報を含まない）。

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
# shellcheck source=lib/sync-utils.sh
source "${SCRIPT_DIR}/lib/sync-utils.sh"

SRC_CURSOR="${PROJECT_ROOT}/ai/cursor/global/.cursor"
SRC_AGENTS="${SRC_CURSOR}/agents"
SRC_HOOKS_JSON="${SRC_CURSOR}/hooks.json"
SRC_HOOKS_DIR="${SRC_CURSOR}/hooks"
SRC_COMMON_AGENTS="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
SRC_MCP_JSON="${SRC_CURSOR}/mcp.json"
DEST_CURSOR="${HOME}/.cursor"
DEST_AGENTS="${HOME}/.cursor/agents"
DEST_HOOKS_JSON="${HOME}/.cursor/hooks.json"
DEST_HOOKS_DIR="${HOME}/.cursor/hooks"
DEST_MCP_JSON="${HOME}/.cursor/mcp.json"

init_backup_dir "$DEST_CURSOR"

# agents ディレクトリを ~/.cursor/agents へコピー（既存はディレクトリごと退避）
sync_agents_dir() {
  if [[ ! -d "$SRC_AGENTS" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_AGENTS" >&2
    exit 1
  fi

  mkdir -p "$DEST_CURSOR"
  backup_to_dir "$DEST_AGENTS"
  mkdir -p "$DEST_AGENTS"
  rsync -a "$SRC_AGENTS/" "$DEST_AGENTS/"
  echo "コピー: ai/cursor/global/.cursor/agents/* -> $DEST_AGENTS/"
}

# hooks.json と hooks/ を常時同期
sync_hooks() {
  mkdir -p "$DEST_CURSOR"

  if [[ -f "$SRC_HOOKS_JSON" ]]; then
    backup_to_dir "$DEST_HOOKS_JSON"
    cp -p "$SRC_HOOKS_JSON" "$DEST_HOOKS_JSON"
    echo "コピー: hooks.json -> $DEST_HOOKS_JSON"
  else
    echo "スキップ: hooks.json が存在しません: $SRC_HOOKS_JSON"
  fi

  if [[ -d "$SRC_HOOKS_DIR" ]]; then
    backup_to_dir "$DEST_HOOKS_DIR"
    mkdir -p "$DEST_HOOKS_DIR"
    rsync -a "$SRC_HOOKS_DIR/" "$DEST_HOOKS_DIR/"
    chmod -R u+x "$DEST_HOOKS_DIR" 2>/dev/null || true
    echo "コピー: hooks/* -> $DEST_HOOKS_DIR/"
  else
    echo "スキップ: hooks/ が存在しません: $SRC_HOOKS_DIR"
  fi
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

  backup_to_dir "$DEST_MCP_JSON"
  cp -p "$SRC_MCP_JSON" "$DEST_MCP_JSON"
  echo "コピー: mcp.json -> $DEST_MCP_JSON"
}

main() {
  echo "=== sync-cursor-to-home ==="
  echo "タイムスタンプ: $SYNC_TIMESTAMP"
  echo ""

  sync_agents_dir
  echo ""
  sync_hooks
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
