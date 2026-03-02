#!/usr/bin/env bash
# sync-geminicli-to-home.sh
# ai/common/global/AGENTS.md を ~/.gemini/GEMINI.md へ、
# ai/gemini_cli/global/.gemini/settings.json を ~/.gemini/settings.json へコピーする。
# 既存がある場合はファイル単位で日時付き .bak に退避してから上書きする。
#
# 注意: antigravity の MCP 設定（~/.gemini/antigravity/）は
# sync-antigravity-to-home.sh で管理される。

set -euo pipefail

for arg in "$@"; do
  case "$arg" in
    -h|--help)
      echo "Usage: $0"
      echo ""
      echo "Gemini CLI グローバル設定（GEMINI.md, settings.json）を ~/.gemini/ へコピーする。"
      exit 0
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_GEMINI_MD="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
SRC_SETTINGS="${PROJECT_ROOT}/ai/gemini_cli/global/.gemini/settings.json"
DEST_GEMINI="${HOME}/.gemini"
DEST_GEMINI_MD="${DEST_GEMINI}/GEMINI.md"
DEST_SETTINGS="${DEST_GEMINI}/settings.json"
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
  echo "=== sync-geminicli-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  mkdir -p "$DEST_GEMINI"

  # AGENTS.md を GEMINI.md としてコピー
  if [[ ! -f "$SRC_GEMINI_MD" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_GEMINI_MD" >&2
    exit 1
  fi
  backup_if_exists "$DEST_GEMINI_MD"
  cp -p "$SRC_GEMINI_MD" "$DEST_GEMINI_MD"
  echo "コピー: AGENTS.md (common) -> $DEST_GEMINI_MD"

  # settings.json のコピー
  if [[ -f "$SRC_SETTINGS" ]]; then
    backup_if_exists "$DEST_SETTINGS"
    cp -p "$SRC_SETTINGS" "$DEST_SETTINGS"
    echo "コピー: settings.json -> $DEST_SETTINGS"
  else
    echo "スキップ: settings.json が存在しません: $SRC_SETTINGS"
  fi

  echo ""
  echo "完了しました。"
}

main "$@"
