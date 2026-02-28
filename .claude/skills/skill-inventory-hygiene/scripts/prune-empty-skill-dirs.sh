#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=".claude/skills"

if [[ ! -d "$ROOT_DIR" ]]; then
  echo "Missing skill root: $ROOT_DIR" >&2
  exit 1
fi

find "$ROOT_DIR" -name '.DS_Store' -type f -delete

while IFS= read -r dir; do
  if [[ ! -f "$dir/SKILL.md" ]]; then
    rmdir "$dir" 2>/dev/null || true
  fi
done < <(find "$ROOT_DIR" -mindepth 1 -maxdepth 1 -type d | sort)

echo "Skill inventory cleanup completed."
