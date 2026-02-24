---
name: task-planner
description: Use when implementation work needs stepwise planning with explicit targets, commands, and completion criteria; When NOT to use: when a tiny one-file change can be completed safely without decomposition; Trigger Keywords: [計画, 分解, roadmap, milestone, 実装手順].
---

# task-planner

## When to use

- Skills/agents を横断して複数ファイル更新が必要なとき。
- `npm run agent:check` や `npm run format:check` を含む検証計画を先に固定したいとき。
- 依存関係がある修正を段階実行で安全に進めたいとき。

## When NOT to use

- 1ファイル数行の修正で即時完了できるとき。
- 実装ではなく情報収集だけを行うとき。
- 緊急修正で段階計画より即時復旧が優先されるとき。

## Trigger Keywords

- 計画
- 分解
- roadmap
- milestone
- 実装手順

## Procedure

1. `git status --short` と `git diff --name-only` で作業範囲を確定する。完了条件: 対象ファイル一覧が確定。
2. 変更を 3〜5 ステップへ分解し、各ステップに完了条件を定義する。完了条件: 手順ごとの Done 条件が明示。
3. 検証コマンド（`npm run agent:check`, `npm run format:check` など）を各ステップへ割り当てる。完了条件: 検証タイミングが確定。
4. リスクとロールバック方針を明記する。完了条件: 失敗時の戻し方が説明可能。
5. 実行順と優先度を確定して提示する。完了条件: そのまま実装開始できる計画が完成。

## Output Contract

| Step | Target Files                               | Action   | Completion Criteria | Verification          |
| ---- | ------------------------------------------ | -------- | ------------------- | --------------------- |
| 1    | `.claude/skills/skill-discoverer/SKILL.md` | 新規追加 | 8セクション実装済み | `npm run agent:check` |

### NG例

❌ 「調査して実装する」だけの抽象計画で終える（実行不能）。

❌ 検証手順を含めない（品質未担保）。

❌ 依存関係の順序を示さない（手戻り増加）。

## Examples

### Example 1

Input: `.claude/skills` と `.claude/agents` を同時更新する計画を作りたい。
Output: 5ステップの実行計画表と検証コマンド割当。

### Example 2

Input: `scripts/validate-skills.mjs` を厳格化する前に実装順を固めたい。
Output: 依存順とロールバック方針を含む計画書。

### Example 3

Input: `.claude/skills/skill-discoverer/SKILL.md` 新規追加の前後で必要な作業を整理したい。
Output: 新規作成→README反映→検証の段階計画。
