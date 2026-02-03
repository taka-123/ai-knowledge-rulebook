---
name: docs-sync
description: Keeps README.md, directorystructure.md, and technologystack.md in sync with repo changes. Use when the user mentions README updates, directory changes, structure, or tech stack updates.
disable-model-invocation: true
---

# Docs Sync

## Quick Start

1. Identify the change set (files/dirs/stack).
2. Update the minimal documentation set:
   - `README.md`
   - `directorystructure.md`
   - `technologystack.md`
3. Run `./format.sh check` after edits.

## Decision Rules

- Reflect only confirmed changes; avoid speculation.
- Keep updates minimal and consistent with existing style.

## Output Format

対象:

- ...
  更新内容:
- ...
  検証:
- コマンド: ./format.sh check
  結果: pass/fail

## Verification

- If edits were made, report the format check result.
