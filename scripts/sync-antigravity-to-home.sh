#!/usr/bin/env bash
# sync-antigravity-to-home.sh
# ai/antigravity/global/.gemini/antigravity/mcp_config.json を
# ~/.gemini/antigravity/mcp_config.json へ、
# ai/common/global/AGENTS.md を ~/.gemini/GEMINI.md へコピーする。
# 既存がある場合はファイル単位で日時付き .bak に退避してから上書きする。
#
# デフォルトでは mcp_config.json（MCP/認証設定）はコピー・退避しない。
# --include-mcp を指定した場合のみ含める。

set -euo pipefail

INCLUDE_MCP=false
for arg in "$@"; do
  case "$arg" in
    --include-mcp) INCLUDE_MCP=true ;;
    -h|--help)
      echo "Usage: $0 [--include-mcp]"
      echo "  --include-mcp  MCP/認証設定（mcp_config.json）もコピー・退避する"
      exit 0
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_MCP="${PROJECT_ROOT}/ai/antigravity/global/.gemini/antigravity/mcp_config.json"
SRC_GEMINI_MD="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
DEST_MCP="${HOME}/.gemini/antigravity/mcp_config.json"
DEST_GEMINI_MD="${HOME}/.gemini/GEMINI.md"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BAK_SUFFIX=".bak.${TIMESTAMP}"

# 既存のファイルを日時付き .bak に退避
backup_if_exists() {
  local target="$1"
  if [[ -e "$target" ]]; then
    local bak="${target}${BAK_SUFFIX}"
    echo "退避: $target -> $bak"
    mv "$target" "$bak"
  fi
}

main() {
  echo "=== sync-antigravity-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  # AGENTS.md を GEMINI.md としてコピー
  if [[ -f "$SRC_GEMINI_MD" ]]; then
    mkdir -p "$(dirname "$DEST_GEMINI_MD")"
    backup_if_exists "$DEST_GEMINI_MD"
    cp -p "$SRC_GEMINI_MD" "$DEST_GEMINI_MD"
    echo "コピー: AGENTS.md (common) -> $DEST_GEMINI_MD"
  else
    echo "スキップ: AGENTS.md が存在しません: $SRC_GEMINI_MD"
  fi

  echo ""

  # MCP 設定のコピー
  if [[ "$INCLUDE_MCP" != true ]]; then
    echo "スキップ: mcp_config.json（認証情報を含むため。--include-mcp で含める）"
    echo ""
    echo "完了しました。"
    return
  fi

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
