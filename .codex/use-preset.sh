#!/usr/bin/env bash
set -euo pipefail

# Keep preset names centralized to avoid typo-driven runtime failures.
readonly PRESET_REVIEW="review"
readonly PRESET_AUDIT="audit"

usage() {
  cat <<'USAGE'
Usage: ./.codex/use-preset.sh <review|audit>
USAGE
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

preset="$1"
source_file=""

case "$preset" in
  "$PRESET_REVIEW")
    source_file=".codex/config.preset.review.toml"
    ;;
  "$PRESET_AUDIT")
    source_file=".codex/config.preset.audit.toml"
    ;;
  *)
    echo "Unknown preset: $preset" >&2
    usage
    exit 1
    ;;
esac

if [[ ! -f "$source_file" ]]; then
  echo "Preset file not found: $source_file" >&2
  exit 1
fi

cp "$source_file" .codex/config.toml
printf 'Applied preset: %s\n' "$preset"
