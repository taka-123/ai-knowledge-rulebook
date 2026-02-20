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

## Trigger Keywords

- 計画
- 分解
- roadmap
- milestone
- 実装手順

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main/api.ts と src/common/types.ts の同時改修順を決めたい。
Output: 影響範囲、実装順、検証順を4ステップで提示し、最後に ./build.sh 実行を完了条件にする。

### Example 2

Input: src/worker/job-runner.ts のリトライ処理追加に合わせて関連設定も直したい。
Output: src/worker -> src/common -> src/main の順で作業計画を提示し、各段階の確認コマンドを明示する。

### Example 3

Input: build.sh を更新して lint と schema check を段階化したい。
Output: 変更前確認、修正、回帰確認、報告の4フェーズ計画を提示する。
