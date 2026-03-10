#!/usr/bin/env bash
# sync-claude-to-home.sh
# ai/claude_code/global/ 以下を ~/ へコピーする。
# global/ 以下には .claude/ ディレクトリ構造と claude.json が含まれる。
# 既存がある場合はバックアップディレクトリへ退避してから上書きする。
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
# shellcheck source=lib/sync-utils.sh
source "${SCRIPT_DIR}/lib/sync-utils.sh"

SRC_GLOBAL="${PROJECT_ROOT}/ai/claude_code/global"
SRC_CLAUDE_MD="${SRC_GLOBAL}/CLAUDE.md"
SRC_CLAUDE_JSON="${SRC_GLOBAL}/claude.json"
DEST_CLAUDE="${HOME}/.claude"
DEST_CLAUDE_JSON="${HOME}/.claude.json"

init_backup_dir "$DEST_CLAUDE"

# global/.claude/ 内のサブディレクトリ・ファイルを ~/.claude/ へ個別にコピー
# ソースに存在する項目のみ退避・上書きし、ユーザー作成データ（plans/, memory/ 等）は保持する
sync_claude_dir() {
  local src_claude_dir="${SRC_GLOBAL}/.claude"
  if [[ ! -d "$src_claude_dir" ]]; then
    echo "エラー: ソースディレクトリが存在しません: $src_claude_dir" >&2
    exit 1
  fi

  mkdir -p "$DEST_CLAUDE"

  # サブディレクトリを個別に退避・コピー（例: hooks/）
  for src_entry in "$src_claude_dir"/*/; do
    [[ -d "$src_entry" ]] || continue
    local name
    name="$(basename "$src_entry")"
    local dest_entry="${DEST_CLAUDE}/${name}"
    backup_to_dir "$dest_entry"
    mkdir -p "$dest_entry"
    rsync -a "$src_entry" "$dest_entry/"
    echo "コピー: .claude/${name}/ -> $dest_entry/"
  done

  # ソースに存在しないサブディレクトリを退避（例: commands/ が廃止された場合）
  # plans/, memory/, projects/, backups/ 等のユーザー作成データは除外
  local -a user_dirs=(plans memory projects backups sync-backups bak cache file-history ide paste-cache plugins session-env shell-snapshots)
  for dest_entry in "$DEST_CLAUDE"/*/; do
    [[ -d "$dest_entry" ]] || continue
    local name
    name="$(basename "$dest_entry")"
    # ユーザー作成データは除外
    local is_user_dir=false
    for ud in "${user_dirs[@]}"; do
      if [[ "$name" == "$ud" ]]; then
        is_user_dir=true
        break
      fi
    done
    [[ "$is_user_dir" == true ]] && continue
    # .bak ディレクトリは除外（旧方式の残存分）
    [[ "$name" == *.bak.* ]] && continue
    # ソースに存在しなければ退避
    if [[ ! -d "${src_claude_dir}/${name}" ]]; then
      backup_to_dir "${dest_entry%/}"
      echo "削除（ソースに不在）: .claude/${name}/"
    fi
  done

  # ファイルを個別に退避・コピー（例: settings.json）
  for src_file in "$src_claude_dir"/*; do
    [[ -f "$src_file" ]] || continue
    local name
    name="$(basename "$src_file")"
    local dest_file="${DEST_CLAUDE}/${name}"
    backup_to_dir "$dest_file"
    cp -p "$src_file" "$dest_file"
    echo "コピー: .claude/${name} -> $dest_file"
  done
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

  backup_to_dir "$DEST_CLAUDE_JSON"
  cp -p "$SRC_CLAUDE_JSON" "$DEST_CLAUDE_JSON"
  echo "コピー: claude.json -> $DEST_CLAUDE_JSON"
}

main() {
  echo "=== sync-claude-to-home ==="
  echo "タイムスタンプ: $SYNC_TIMESTAMP"
  echo ""

  sync_claude_dir

  # CLAUDE.md を ~/.claude/CLAUDE.md へコピー
  if [[ -f "$SRC_CLAUDE_MD" ]]; then
    local dest_claude_md="${DEST_CLAUDE}/CLAUDE.md"
    backup_to_dir "$dest_claude_md"
    cp -p "$SRC_CLAUDE_MD" "$dest_claude_md"
    echo "コピー: CLAUDE.md -> $dest_claude_md"
  fi

  echo ""
  sync_claude_json

  echo ""
  echo "完了しました。"
  echo ""
  if [[ -f "$SRC_CLAUDE_JSON" ]]; then
    echo "--- MCP 設定の案内 ---"
    echo "ai/claude_code/global/claude.json に MCP 設定があります。"
    echo "必要なものがあれば ~/.claude.json の mcpServers に適切に記述してください。"
    echo "プレースホルダー（\${GITHUB_PAT} 等）は必要に応じて修正してください。"
    echo ""
  fi
}

main "$@"
