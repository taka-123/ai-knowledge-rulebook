#!/usr/bin/env bash
# copy-portable-to-project.sh
# ai/*/global の Portable Kit（汎用 Skills / Agents）を、任意プロジェクトへ実体コピーする。
#
# 正本: この rulebook。ホームや他プロジェクトからコピーしない。
# Cloud で使う場合は、コピー後に対象プロジェクトで git commit すること。
#
# Usage:
#   ./scripts/copy-portable-to-project.sh --list
#   ./scripts/copy-portable-to-project.sh <project-root> --preset cloud-basic
#   ./scripts/copy-portable-to-project.sh <project-root> --preset cloud-handoff
#   ./scripts/copy-portable-to-project.sh <project-root> --skill document-authoring --agent codebase-explorer
#   ./scripts/copy-portable-to-project.sh <project-root> --preset cloud-basic --dry-run
#   ./scripts/copy-portable-to-project.sh <project-root> --skill grill-me --force

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

SRC_CLAUDE_SKILLS="${PROJECT_ROOT}/ai/claude_code/global/.claude/skills"
SRC_CLAUDE_AGENTS="${PROJECT_ROOT}/ai/claude_code/global/.claude/agents"
SRC_CURSOR_AGENTS="${PROJECT_ROOT}/ai/cursor/global/.cursor/agents"

DRY_RUN=false
FORCE=false
LIST_ONLY=false
PRESET=""
TARGET=""
declare -a SKILLS=()
declare -a AGENTS=()

# プリセット（ai/PORTABLE_KIT.md と同期）
PRESET_CLOUD_BASIC_SKILLS=(
  document-authoring
  ai-instruction-authoring
  backlog-markdown-formatting
)
PRESET_CLOUD_BASIC_AGENTS=(
  codebase-explorer
  tech-researcher
)
PRESET_CLOUD_HANDOFF_SKILLS=(
  handoff-html-digest
  one-page-graphic-recorder
)
PRESET_CLOUD_HANDOFF_AGENTS=()

usage() {
  cat <<'EOF'
Usage:
  copy-portable-to-project.sh --list
  copy-portable-to-project.sh <project-root> --preset cloud-basic [--dry-run] [--force]
  copy-portable-to-project.sh <project-root> --preset cloud-handoff [--dry-run] [--force]
  copy-portable-to-project.sh <project-root> --skill NAME [--agent NAME]... [--dry-run] [--force]

Options:
  --list           Portable Kit の一覧を表示して終了
  --preset NAME    cloud-basic | cloud-handoff
  --skill NAME     コピーする Skill（複数可）
  --agent NAME     コピーする Agent（Claude + Cursor の両方にあれば両方）
  --dry-run        コピーせず予定だけ表示
  --force          既存を確認なしで上書き（先に .portable-kit-backup へ退避）
  -h, --help       このヘルプ

Notes:
  - 正本は rulebook の ai/*/global。詳細は ai/PORTABLE_KIT.md
  - 同名を ~/.claude/skills 等に残すと Claude Skills は personal が優先され得る
  - Cloud 利用時はコピー後に対象プロジェクトで commit すること
EOF
}

preset_mark() {
  local name="$1"
  local kind="$2" # skill|agent
  local mark=" "
  local p
  if [[ "$kind" == skill ]]; then
    for p in "${PRESET_CLOUD_BASIC_SKILLS[@]}"; do
      [[ "$p" == "$name" ]] && mark="B" && break
    done
    for p in "${PRESET_CLOUD_HANDOFF_SKILLS[@]}"; do
      if [[ "$p" == "$name" ]]; then
        [[ "$mark" == "B" ]] && mark="*" || mark="H"
        break
      fi
    done
  else
    for p in "${PRESET_CLOUD_BASIC_AGENTS[@]}"; do
      [[ "$p" == "$name" ]] && mark="B" && break
    done
    if [[ ${#PRESET_CLOUD_HANDOFF_AGENTS[@]} -gt 0 ]]; then
      for p in "${PRESET_CLOUD_HANDOFF_AGENTS[@]}"; do
        if [[ "$p" == "$name" ]]; then
          [[ "$mark" == "B" ]] && mark="*" || mark="H"
          break
        fi
      done
    fi
  fi
  printf '%s' "$mark"
}

die() {
  echo "エラー: $*" >&2
  exit 1
}

warn() {
  echo "警告: $*" >&2
}

list_kit() {
  echo "=== Portable Kit（正本: ${PROJECT_ROOT}/ai）==="
  echo ""
  echo "Skills (ai/claude_code/global/.claude/skills/):"
  if [[ -d "$SRC_CLAUDE_SKILLS" ]]; then
    for d in "$SRC_CLAUDE_SKILLS"/*/; do
      [[ -d "$d" ]] || continue
      local name mark
      name="$(basename "$d")"
      [[ -f "${d}SKILL.md" ]] || continue
      mark="$(preset_mark "$name" skill)"
      echo "  [${mark}] ${name}"
    done
  fi
  echo "  (B = cloud-basic, H = cloud-handoff)"
  echo ""
  echo "Claude agents (ai/claude_code/global/.claude/agents/):"
  if [[ -d "$SRC_CLAUDE_AGENTS" ]]; then
    for f in "$SRC_CLAUDE_AGENTS"/*.md; do
      [[ -f "$f" ]] || continue
      local name mark
      name="$(basename "$f" .md)"
      mark="$(preset_mark "$name" agent)"
      echo "  [${mark}] ${name}"
    done
  fi
  echo ""
  echo "Cursor agents (ai/cursor/global/.cursor/agents/):"
  if [[ -d "$SRC_CURSOR_AGENTS" ]]; then
    for f in "$SRC_CURSOR_AGENTS"/*.md; do
      [[ -f "$f" ]] || continue
      local name mark
      name="$(basename "$f" .md)"
      mark="$(preset_mark "$name" agent)"
      echo "  [${mark}] ${name}"
    done
  fi
  echo ""
  echo "詳細: ai/PORTABLE_KIT.md"
}

confirm_overwrite() {
  local dest="$1"
  [[ "$FORCE" == true ]] && return 0
  [[ ! -e "$dest" ]] && return 0
  if [[ ! -t 0 ]]; then
    die "既存あり（非対話）: $dest （--force を指定）"
  fi
  local ans
  read -r -p "上書きしますか? $dest [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]] || die "中止: $dest"
}

backup_if_exists() {
  local dest="$1"
  local backup_root="$2"
  [[ -e "$dest" ]] || return 0
  mkdir -p "$backup_root"
  local base
  base="$(basename "$dest")"
  local dest_dir
  dest_dir="$(cd "$(dirname "$dest")" && pwd)"
  local rel="${dest_dir#"$TARGET_ABS"}"
  rel="${rel#/}"
  local bak_dir="${backup_root}/${rel}"
  mkdir -p "$bak_dir"
  mv "$dest" "${bak_dir}/${base}"
  echo "退避: $dest -> ${bak_dir}/${base}"
}

copy_tree() {
  local src="$1"
  local dest="$2"
  local backup_root="$3"
  [[ -e "$src" ]] || die "ソースがありません: $src"
  if [[ "$DRY_RUN" == true ]]; then
    echo "DRY-RUN: $src -> $dest"
    return 0
  fi
  confirm_overwrite "$dest"
  backup_if_exists "$dest" "$backup_root"
  mkdir -p "$(dirname "$dest")"
  if [[ -d "$src" ]]; then
    mkdir -p "$dest"
    # macOS / Linux: ディレクトリ内容をコピー
    cp -R "$src"/. "$dest"/
  else
    cp -p "$src" "$dest"
  fi
  echo "コピー: $src -> $dest"
}

warn_homonym() {
  local kind="$1"
  local name="$2"
  if [[ "$kind" == "skill" && -d "${HOME}/.claude/skills/${name}" ]]; then
    warn "同名 Skill が ~/.claude/skills/${name} にあります。Claude では personal が優先され得ます。別名か global 側の整理を検討してください。"
  fi
  if [[ "$kind" == "agent" && -f "${HOME}/.claude/agents/${name}.md" ]]; then
    warn "同名 Agent が ~/.claude/agents/${name}.md にあります（Claude）。"
  fi
  if [[ "$kind" == "agent" && -f "${HOME}/.cursor/agents/${name}.md" ]]; then
    warn "同名 Agent が ~/.cursor/agents/${name}.md にあります（Cursor）。"
  fi
}

write_lock() {
  local lock_file="${TARGET_ABS}/.portable-kit.lock"
  local rev
  rev="$(git -C "$PROJECT_ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  if [[ "$DRY_RUN" == true ]]; then
    echo "DRY-RUN: would update ${lock_file}"
    return 0
  fi
  {
    echo "# Generated by copy-portable-to-project.sh — do not hand-edit unless needed"
    echo "source_repo: ${PROJECT_ROOT}"
    echo "source_rev: ${rev}"
    echo "copied_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "skills:"
    for s in "${SKILLS[@]:-}"; do
      [[ -n "${s:-}" ]] && echo "  - ${s}"
    done
    echo "agents:"
    for a in "${AGENTS[@]:-}"; do
      [[ -n "${a:-}" ]] && echo "  - ${a}"
    done
  } >"$lock_file"
  echo "記録: $lock_file"
}

# --- args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --list)
      LIST_ONLY=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --preset)
      [[ $# -ge 2 ]] || die "--preset には名前が必要です"
      PRESET="$2"
      shift 2
      ;;
    --skill)
      [[ $# -ge 2 ]] || die "--skill には名前が必要です"
      SKILLS+=("$2")
      shift 2
      ;;
    --agent)
      [[ $# -ge 2 ]] || die "--agent には名前が必要です"
      AGENTS+=("$2")
      shift 2
      ;;
    --*)
      die "不明なオプション: $1"
      ;;
    *)
      if [[ -z "$TARGET" ]]; then
        TARGET="$1"
        shift
      else
        die "引数が多すぎます: $1"
      fi
      ;;
  esac
done

if [[ "$LIST_ONLY" == true ]]; then
  list_kit
  exit 0
fi

[[ -n "$TARGET" ]] || die "project-root を指定してください（--list で一覧）"
[[ -d "$TARGET" ]] || die "ディレクトリがありません: $TARGET"
TARGET_ABS="$(cd "$TARGET" && pwd)"

if [[ -n "$PRESET" ]]; then
  case "$PRESET" in
    cloud-basic)
      SKILLS+=("${PRESET_CLOUD_BASIC_SKILLS[@]}")
      AGENTS+=("${PRESET_CLOUD_BASIC_AGENTS[@]}")
      ;;
    cloud-handoff)
      SKILLS+=("${PRESET_CLOUD_HANDOFF_SKILLS[@]}")
      if [[ ${#PRESET_CLOUD_HANDOFF_AGENTS[@]} -gt 0 ]]; then
        AGENTS+=("${PRESET_CLOUD_HANDOFF_AGENTS[@]}")
      fi
      ;;
    *)
      die "未知の preset: ${PRESET} (cloud-basic | cloud-handoff)"
      ;;
  esac
fi

# uniq (bash 3.2 互換: mapfile 不使用)
uniq_array() {
  local -a in=("$@")
  local -a out=()
  local x y seen
  for x in "${in[@]}"; do
    [[ -n "$x" ]] || continue
    seen=false
    for y in "${out[@]:-}"; do
      [[ "$x" == "$y" ]] && seen=true && break
    done
    [[ "$seen" == false ]] && out+=("$x")
  done
  printf '%s\n' "${out[@]:-}"
}
if [[ ${#SKILLS[@]} -gt 0 ]]; then
  # shellcheck disable=SC2207
  SKILLS=($(uniq_array "${SKILLS[@]}"))
fi
if [[ ${#AGENTS[@]} -gt 0 ]]; then
  # shellcheck disable=SC2207
  AGENTS=($(uniq_array "${AGENTS[@]}"))
fi

[[ ${#SKILLS[@]} -gt 0 || ${#AGENTS[@]} -gt 0 ]] \
  || die "--preset / --skill / --agent のいずれかを指定してください"

BACKUP_ROOT="${TARGET_ABS}/.portable-kit-backup/$(date +%Y%m%d-%H%M%S)"

echo "=== copy-portable-to-project ==="
echo "正本: $PROJECT_ROOT"
echo "対象: $TARGET_ABS"
[[ "$DRY_RUN" == true ]] && echo "モード: dry-run"
echo ""

for name in "${SKILLS[@]:-}"; do
  [[ -n "${name:-}" ]] || continue
  src="${SRC_CLAUDE_SKILLS}/${name}"
  [[ -d "$src" && -f "${src}/SKILL.md" ]] || die "未知の Skill: $name"
  warn_homonym skill "$name"
  copy_tree "$src" "${TARGET_ABS}/.claude/skills/${name}" "$BACKUP_ROOT"
done

for name in "${AGENTS[@]:-}"; do
  [[ -n "${name:-}" ]] || continue
  copied=false
  warn_homonym agent "$name"
  if [[ -f "${SRC_CLAUDE_AGENTS}/${name}.md" ]]; then
    copy_tree "${SRC_CLAUDE_AGENTS}/${name}.md" \
      "${TARGET_ABS}/.claude/agents/${name}.md" "$BACKUP_ROOT"
    copied=true
  fi
  if [[ -f "${SRC_CURSOR_AGENTS}/${name}.md" ]]; then
    copy_tree "${SRC_CURSOR_AGENTS}/${name}.md" \
      "${TARGET_ABS}/.cursor/agents/${name}.md" "$BACKUP_ROOT"
    copied=true
  fi
  [[ "$copied" == true ]] || die "未知の Agent: $name"
done

write_lock

echo ""
echo "完了しました。"
echo "--- 次の手順 ---"
echo "1. 対象プロジェクトで差分を確認する"
echo "2. Cloud / チーム共有で使うなら git add && git commit する"
echo "3. Claude Skills の同名が ~/.claude/skills にある場合は整理する（personal 優先に注意）"
echo "詳細: ${PROJECT_ROOT}/ai/PORTABLE_KIT.md"
