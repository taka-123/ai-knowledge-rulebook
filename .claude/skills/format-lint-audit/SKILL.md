---
name: format-lint-audit
description: Use when final quality gates must run repository formatting and lint checks with explicit pass or fail reporting; When NOT to use: exploratory drafting before files are finalized; Trigger Keywords: quality gate, format:check, lint, CI, 検証.
---

# format-lint-audit

## When to use

- 変更後の最終検証を実施する。
- CI 相当の品質ゲートを確認する。

## When NOT to use

- 実装前の草案段階。
- 編集中で結果が安定しない段階。

## Trigger Keywords

- quality gate
- format:check
- lint
- CI
- 検証

## Examples

### Example 1

Input: 変更後に品質ゲートを一括で確認したい。
Output: `npm run format:check` と `npm run schema:check` を実行し、結果を要約する。

### Example 2

Input: markdownlint だけ再検証して。
Output: 対象ファイルに `npx markdownlint-cli2` を実行し、合否を明示する。

### Example 3

Input: CI 前のチェックリストを作って。
Output: 実行コマンド、期待結果、失敗時の修正先を1表にまとめる。
