---
name: task-planner
description: Use when implementation requires an explicit step plan with file targets, validation commands, and completion criteria; When NOT to use: tiny edits that can be completed safely without planning; Trigger Keywords: 計画, 分解, roadmap, milestone, 実装手順.
---

# task-planner

## When to use

- 変更が複数ファイルにまたがる。
- 実装前に影響範囲の分解が必要。

## When NOT to use

- 1ファイル内の軽微な文言修正。
- 既存手順が明確で追加分解が不要。

## Trigger Keywords

- 計画
- 分解
- roadmap
- milestone
- 実装手順

## Examples

### Example 1

Input: schema チェック失敗を直す前に実装計画を作って。
Output: `schemas/` と `notes/` の対象を分離し、`npm run schema:check` を終点にした4ステップ計画を提示する。

### Example 2

Input: ルール衝突を最小差分で解消する順序を決めたい。
Output: `AGENTS.md` → `CLAUDE.md` → `.cursor/rules` の順で修正し、各ステップの完了条件を提示する。

### Example 3

Input: ドキュメント更新と lint 修正を同時に進める手順を設計して。
Output: 並列可能タスクと逐次タスクを分離し、`npm run format:check` で統合検証する計画を提示する。
