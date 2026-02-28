#!/usr/bin/env bash
# sync-windsurf-to-home.sh
# ai/windsurf/global/mcp_config.json を ~/.codeium/windsurf/mcp_config.json へ、
# ai/common/global/AGENTS.md を ~/.codeium/windsurf/memories/global_rules.md へコピーする。
# 既存がある場合はディレクトリ/ファイル単位で日時付き .bak に退避してから上書きする。
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
SRC_MCP="${PROJECT_ROOT}/ai/windsurf/global/mcp_config.json"
SRC_COMMON_AGENTS="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
DEST_WINDSURF="${HOME}/.codeium/windsurf"
DEST_MCP="${HOME}/.codeium/windsurf/mcp_config.json"
DEST_GLOBAL_RULES="${HOME}/.codeium/windsurf/memories/global_rules.md"
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

main() {
  echo "=== sync-windsurf-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  if [[ ! -f "$SRC_COMMON_AGENTS" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_COMMON_AGENTS" >&2
    exit 1
  fi

  if [[ "$INCLUDE_MCP" == true ]]; then
    if [[ ! -f "$SRC_MCP" ]]; then
      echo "エラー: ソースファイルが存在しません: $SRC_MCP" >&2
      exit 1
    fi
    backup_if_exists "$DEST_WINDSURF"
    mkdir -p "$(dirname "$DEST_MCP")"
    mkdir -p "$(dirname "$DEST_GLOBAL_RULES")"
    cp -p "$SRC_MCP" "$DEST_MCP"
    cp -p "$SRC_COMMON_AGENTS" "$DEST_GLOBAL_RULES"
    echo "コピー: mcp_config.json -> $DEST_MCP"
    echo "コピー: AGENTS.md (common) -> $DEST_GLOBAL_RULES"
  else
    echo "スキップ: mcp_config.json（認証情報を含むため。--include-mcp で含める）"
    mkdir -p "$(dirname "$DEST_GLOBAL_RULES")"
    backup_if_exists "$DEST_GLOBAL_RULES"
    cp -p "$SRC_COMMON_AGENTS" "$DEST_GLOBAL_RULES"
    echo "コピー: AGENTS.md (common) -> $DEST_GLOBAL_RULES"
  fi

  echo ""
  echo "完了しました。"
}

main "$@"
