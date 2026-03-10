#!/usr/bin/env bash
# sync-utils.sh — sync-*-to-home.sh スクリプト共通ユーティリティ
#
# 使い方:
#   source "$(dirname "${BASH_SOURCE[0]}")/lib/sync-utils.sh"
#   init_backup_dir "$HOME/.claude"
#   backup_to_dir "/path/to/target"

# タイムスタンプ（全スクリプトで統一）
SYNC_TIMESTAMP="${SYNC_TIMESTAMP:-$(date +%Y%m%d-%H%M%S)}"

# バックアップディレクトリのルートパス（init_backup_dir で設定）
_BACKUP_DIR=""

# バックアップディレクトリを初期化
# 引数: $1 = ツールのホームディレクトリ（例: ~/.claude）
init_backup_dir() {
  local tool_home="$1"
  _BACKUP_DIR="${tool_home}/sync-backups/${SYNC_TIMESTAMP}"
}

# 対象をバックアップディレクトリへ移動
# 引数: $1 = 退避対象のパス
backup_to_dir() {
  local target="$1"
  [[ -e "$target" ]] || return 0

  if [[ -z "$_BACKUP_DIR" ]]; then
    echo "エラー: init_backup_dir を先に呼んでください" >&2
    return 1
  fi

  mkdir -p "$_BACKUP_DIR"
  local name
  name="$(basename "$target")"
  echo "退避: $target -> ${_BACKUP_DIR}/${name}"
  mv "$target" "${_BACKUP_DIR}/${name}"
}
