#!/usr/bin/env bash
# sync-codex-to-home.sh
# ai/openai_codex/global/.codex/ 以下を ~/.codex/ へコピーする。
# 既存がある場合はディレクトリ単位で日時付き .bak に退避してから上書きする。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_CODEX="${PROJECT_ROOT}/ai/openai_codex/global/.codex"
SRC_COMMON_AGENTS="${PROJECT_ROOT}/ai/common/global/AGENTS.md"
DEST_CODEX="${HOME}/.codex"
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

# .codex/ 内のサブディレクトリ・ファイルを ~/.codex/ へ個別にコピー
# ソースに存在する項目のみ退避・上書きし、ユーザーデータ（sessions/, history.jsonl 等）は保持する
sync_codex_dir() {
  if [[ ! -d "$SRC_CODEX" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $SRC_CODEX" >&2
    exit 1
  fi

  mkdir -p "$DEST_CODEX"

  # サブディレクトリを個別に退避・コピー（例: agents/, prompts/, rules/）
  for src_entry in "$SRC_CODEX"/*/; do
    [[ -d "$src_entry" ]] || continue
    local name
    name="$(basename "$src_entry")"
    local dest_entry="${DEST_CODEX}/${name}"
    backup_if_exists "$dest_entry"
    mkdir -p "$dest_entry"
    rsync -a "$src_entry" "$dest_entry/"
    echo "コピー: .codex/${name}/ -> $dest_entry/"
  done

  # ファイルを個別に退避・コピー（例: config.toml）
  for src_file in "$SRC_CODEX"/*; do
    [[ -f "$src_file" ]] || continue
    local name
    name="$(basename "$src_file")"
    local dest_file="${DEST_CODEX}/${name}"
    backup_if_exists "$dest_file"
    cp -p "$src_file" "$dest_file"
    echo "コピー: .codex/${name} -> $dest_file"
  done

  # AGENTS.md (common) -> ~/.codex/AGENTS.md
  backup_if_exists "${DEST_CODEX}/AGENTS.md"
  cp -p "$SRC_COMMON_AGENTS" "${DEST_CODEX}/AGENTS.md"
  echo "コピー: AGENTS.md (common) -> ${DEST_CODEX}/AGENTS.md"
}

main() {
  echo "=== sync-codex-to-home ==="
  echo "タイムスタンプ: $TIMESTAMP"
  echo ""

  sync_codex_dir

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
