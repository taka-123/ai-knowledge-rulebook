---
name: repo-quality-gate
description: Repository quality gate for CI前確認 and 品質ゲート tasks. Use when requests include format check, schema check, lint, CI通過確認, or pre-PR validation.
---

# Repo Quality Gate

## 手順

1. 変更対象を確認し、検証範囲を `ai/` `notes/` `schemas/` `policy/` などに分解する。
2. `npm run format:check` を実行する。
3. `npm run lint:md` `npm run lint:yaml` `npm run lint:json` を実行する。
4. `npm run schema:check` を実行する。
5. 失敗がある場合は、原因をファイル単位で列挙し、最小修正を提案する。
6. 修正後に同じ検証コマンドを再実行し、結果を再確認する。

## Safety

- 破壊的操作やリモート影響のある操作は実行しない。必要なら提案し、承認後に実行する。
- `git push` `deploy` `migrate` `infra` `db` 系コマンドは必ず承認を要求する。
- 自動修正系（`./format.sh fix` など）はデフォルト実行せず、提案して承認を取る。

## 継承

- `task-reviewer` の完遂判定と `codebase-explorer` の対象範囲特定を継承する。
