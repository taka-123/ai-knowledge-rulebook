#!/usr/bin/env bash
# sync-all-to-home.sh
# 5つの sync スクリプト（claude, cursor, codex, windsurf, gemini）を順に実行する。
# --include-mcp を渡すと各スクリプトにそのまま引き継ぐ。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

EXTRA_ARGS=()
for arg in "$@"; do
  case "$arg" in
    -h|--help)
      echo "Usage: $0 [--include-mcp]"
      echo ""
      echo "以下を順に実行: sync-claude, sync-cursor, sync-codex, sync-windsurf, sync-gemini"
      echo "  --include-mcp  各スクリプトに渡し、MCP/認証設定もコピーする"
      exit 0
      ;;
    *) EXTRA_ARGS+=("$arg") ;;
  esac
done

echo "=========================================="
echo "sync-all-to-home"
echo "=========================================="
echo ""

"${SCRIPT_DIR}/sync-claude-to-home.sh" ${EXTRA_ARGS+"${EXTRA_ARGS[@]}"}
echo ""
echo "---"
echo ""

"${SCRIPT_DIR}/sync-cursor-to-home.sh" ${EXTRA_ARGS+"${EXTRA_ARGS[@]}"}
echo ""
echo "---"
echo ""

"${SCRIPT_DIR}/sync-codex-to-home.sh" ${EXTRA_ARGS+"${EXTRA_ARGS[@]}"}
echo ""
echo "---"
echo ""

"${SCRIPT_DIR}/sync-windsurf-to-home.sh" ${EXTRA_ARGS+"${EXTRA_ARGS[@]}"}
echo ""
echo "---"
echo ""

"${SCRIPT_DIR}/sync-gemini-to-home.sh" ${EXTRA_ARGS+"${EXTRA_ARGS[@]}"}

echo ""
echo "=========================================="
echo "全 sync 完了"
echo "=========================================="
echo ""
echo "--- skills の共通化（推奨） ---"
echo "~/.claude/skills/ を共通として、他ツールからシンボリックリンクで参照する場合:"
echo ""
echo "  Codex: ~/.agents/skills (https://developers.openai.com/codex/skills)"
echo "  Cursor/Windsurf 等: 各ツールの skills パスを確認の上、必要に応じて追加"
echo ""
echo '  for d in ~/.cursor ~/.agents ~/.windsurf; do rm -rf "$d/skills" 2>/dev/null; mkdir -p "$d"; ln -sf "$HOME/.claude/skills" "$d/skills"; done'
echo ""
echo "※ 既存の skills ディレクトリは上書きされます。必要に応じて退避してから実行してください。"
echo ""
