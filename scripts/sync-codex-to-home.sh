#!/usr/bin/env bash
# sync-codex-to-home.sh
# ai/openai_codex/global 以下を ~/.codex/ へ、
# ai/common/global/AGENTS.md を ~/.codex/AGENTS.md へコピーする。
# 既存がある場合はディレクトリ単位で日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_GLOBAL="${PROJECT_ROOT}/ai/openai_codex/global"
SRC_COMMON_AGENTS="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
DEST_CODEX="${HOME}/.codex"
DEST_AGENTS="${HOME}/.codex/AGENTS.md"
DEST_CONFIG="${HOME}/.codex/config.toml"
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

# global ディレクトリを ~/.codex へコピー（既存はディレクトリごと退避）
sync_global_dir() {
  if [[ ! -d "$SRC_GLOBAL" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_GLOBAL" >&2
    exit 1
  fi

  backup_if_exists "$DEST_CODEX"
  mkdir -p "$DEST_CODEX"
  rsync -a "$SRC_GLOBAL/" "$DEST_CODEX/"
  echo "コピー: ai/openai_codex/global/* -> $DEST_CODEX/"
}

# ai/common/global/AGENTS.md を ~/.codex/AGENTS.md へコピー（上書き）
sync_common_agents() {
  if [[ ! -f "$SRC_COMMON_AGENTS" ]]; then
    echo "エラー: ソースファイルが存在しません: $SRC_COMMON_AGENTS" >&2
    exit 1
  fi

  cp -p "$SRC_COMMON_AGENTS" "$DEST_AGENTS"
  echo "コピー: AGENTS.md (common) -> $DEST_AGENTS"
}

main() {
  echo "=== sync-codex-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  sync_global_dir
  echo ""
  sync_common_agents

  echo ""
  echo "完了しました。"
  echo ""
  if [[ -f "$DEST_CONFIG" ]] && grep -q '\[mcp_servers\.' "$DEST_CONFIG" 2>/dev/null; then
    echo "--- 注意 ---"
    echo "config.toml の [mcp_servers.*] にプレースホルダーや環境変数参照がある場合は、"
    echo "認証情報を正しく書き換えてください。"
    echo ""
  fi
}

main "$@"
