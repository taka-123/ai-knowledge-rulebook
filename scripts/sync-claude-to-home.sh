#!/usr/bin/env bash
# sync-claude-to-home.sh
# ai/claude_code/global を ~/.claude/ へ、
# ai/claude_code/claude.json を ~/.claude.json へコピーする。
# 既存がある場合はディレクトリ/ファイル単位で日時付き .bak に退避してから上書きする。
#
# デフォルトでは claude.json（MCP/認証設定）はコピー・退避しない。
# --include-mcp を指定した場合のみ含める。

set -euo pipefail

INCLUDE_MCP=false
for arg in "$@"; do
  case "$arg" in
    --include-mcp) INCLUDE_MCP=true ;;
    -h|--help)
      echo "Usage: $0 [--include-mcp]"
      echo "  --include-mcp  MCP/認証設定（claude.json）もコピー・退避する"
      exit 0
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_GLOBAL="${PROJECT_ROOT}/ai/claude_code/global"
SRC_CLAUDE_JSON="${PROJECT_ROOT}/ai/claude_code/claude.json"
DEST_CLAUDE="${HOME}/.claude"
DEST_CLAUDE_JSON="${HOME}/.claude.json"
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

# global ディレクトリを ~/.claude へコピー（既存はディレクトリごと退避）
sync_global_dir() {
  if [[ ! -d "$SRC_GLOBAL" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_GLOBAL" >&2
    exit 1
  fi

  backup_if_exists "$DEST_CLAUDE"
  mkdir -p "$DEST_CLAUDE"
  rsync -a "$SRC_GLOBAL/" "$DEST_CLAUDE/"
  echo "コピー: ai/claude_code/global/* -> $DEST_CLAUDE/"
}

# claude.json を ~/.claude.json へコピー（--include-mcp 時のみ）
sync_claude_json() {
  if [[ "$INCLUDE_MCP" != true ]]; then
    echo "スキップ: claude.json（認証情報を含むため。--include-mcp で含める）"
    return
  fi
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
  echo ""
  if [[ -f "$SRC_CLAUDE_JSON" ]]; then
    echo "--- MCP 設定の案内 ---"
    echo "ai/claude_code/claude.json に MCP 設定があります。"
    echo "必要なものがあれば ~/.claude.json の mcpServers に適切に記述してください。"
    echo "プレースホルダー（\${GITHUB_PAT} 等）は必要に応じて修正してください。"
    echo ""
  fi
}

main "$@"
