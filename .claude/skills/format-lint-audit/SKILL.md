---
name: format-lint-audit
description: Use when final quality gates must be executed to confirm formatting, linting, and agent validation status; When NOT to use: when implementation is still exploratory and files are not ready for final checks; Trigger Keywords: [quality gate, format:check, lint, CI, 検証].
---

# format-lint-audit

## When to use

- 変更完了後に `npm run format:check` と `npm run agent:check` を最終実行するとき。
- `.claude/skills/*/SKILL.md` を更新したため品質ゲートを閉じるとき。
- PR 前に Markdown/JSON/YAML とルーティング検証結果をまとめるとき。

## When NOT to use

- まだ修正作業中で失敗を前提とする段階のとき。
- 実行環境が不完全で検証コマンドを回せないとき。
- 単なる調査でファイル差分が存在しないとき。

## Trigger Keywords

- quality gate
- format:check
- lint
- CI
- 検証

## Procedure

1. `git diff --name-only` で今回変更したファイルを確定する。完了条件: 対象一覧が確定。
2. `npm run format:check` を実行し、結果を記録する。完了条件: PASS/FAIL が明示。
3. `npm run agent:check` を実行し、skills/routing 検証の結果を記録する。完了条件: PASS/FAIL が明示。
4. 必要なら `npm run lint:md` / `npm run lint:json` / `npm run lint:yaml` を追加実行する。完了条件: 追加チェック結果取得。
5. すべての結果を 1 つの品質レポートへ集約する。完了条件: 再実行可能な記録。

## Output Contract

| Check    | Command                | Result             |
| -------- | ---------------------- | ------------------ |
| Format   | `npm run format:check` | PASS / FAIL        |
| Agent    | `npm run agent:check`  | PASS / FAIL        |
| Markdown | `npm run lint:md`      | PASS / FAIL / SKIP |

### NG例

❌ 失敗したコマンドを省略して報告する（隠れ失敗）。

❌ PASS/FAIL を書かずに「問題なし」とだけ記す（判定不能）。

❌ 実行していないコマンドを実行済みとして記載する（虚偽報告）。

## Examples

### Example 1

Input: `.claude/skills/lint-fix/SKILL.md` を更新したので最終検証したい。
Output: `format:check` と `agent:check` の結果表。

### Example 2

Input: `.claude/agents/content-writer.md` と `.cursor/agents/content-writer.md` を更新したため `npm run agent:check` を実行したい。
Output: 実行コマンド一覧と PASS/FAIL サマリ。

### Example 3

Input: `.work/AI_BLUEPRINT.md` だけを編集したので Markdown チェックを追加したい。
Output: `npm run lint:md` を含む品質レポート。
