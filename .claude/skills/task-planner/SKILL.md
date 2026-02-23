---
name: task-planner
description: Use when implementation requires step-by-step planning with explicit file targets and verification gates; When NOT to use: when a one-line edit can be completed safely without decomposition; Trigger Keywords: [計画, 分解, roadmap, milestone, 実装手順].
---

# task-planner

## When to use

- 複数ファイルにまたがる変更を着手前に分解したい場合。
- src/main、src/worker、src/common の依存関係を順序立てて更新したい場合。

## When NOT to use

- 単一ファイルの軽微な文言修正のみで完了する場合。
- 既存手順が確定しており追加計画が不要な場合。
- ユーザーが「計画不要で実装して」と明示している場合。

## Trigger Keywords

- 計画
- 分解
- roadmap
- milestone
- 実装手順

## Procedure

1. タスクを 🟢/🟡/🔴 で分類し、破壊的変更の有無を先に宣言する。
2. 対象ファイルを明示する（新規/更新/削除を分ける）。
3. 実装ステップを 3〜6 手順で書く（各手順に完了条件を付ける）。
4. 検証コマンドを先に固定する（最低: `npm run format:check`、必要時 `npm run schema:check`）。
5. 依存・前提不足がある場合だけ質問し、それ以外は実装に進む。

## Output Contract

- 必ず「目的 / 制約 / 影響範囲 / 実装手順 / 検証」をこの順で提示する。
- 実装手順はチェックリスト形式で出す（完了判断が曖昧な文を避ける）。
- 「調査だけ」で終わらせず、次の実行アクションを 1 行で明記する。

## Examples

### Example 1

Input: src/main/api.ts と src/common/types.ts の同時改修順を決めたい。
Output: 影響範囲、実装順、検証順を4ステップで提示し、最後に `npm run format:check` と `npm run schema:check` を完了条件にする。

### Example 2

Input: src/worker/job-runner.ts のリトライ処理追加に合わせて関連設定も直したい。
Output: src/worker -> src/common -> src/main の順で作業計画を提示し、各段階の確認コマンドを明示する。

### Example 3

Input: build.sh を更新して lint と schema check を段階化したい。
Output: 変更前確認、修正、回帰確認、報告の4フェーズ計画を提示する。
