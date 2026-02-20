---
name: lint-fix
description: Use when lint or format checks fail and deterministic repository commands must be applied to fix issues; When NOT to use: when there is no failing lint signal or the task is architecture design only; Trigger Keywords: [lint, format, markdownlint, prettier, yamllint].
---

# lint-fix

## When to use

- lint 出力に基づく修正を機械的に進める必要がある場合。
- src/main、src/worker、src/common の整形崩れを一括修正したい場合。

## When NOT to use

- 失敗ログがなく推測のみで修正対象を決める場合。
- 設計議論のみで実ファイル修正が不要な場合。

## Trigger Keywords

- lint
- format
- markdownlint
- prettier
- yamllint

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main/handler.ts で prettier エラーが出ている。
Output: 該当ファイルのみ修正し、format check の再実行結果を記録する。

### Example 2

Input: src/common/config.ts と build.sh 周辺の行末空白を解消したい。
Output: 最小差分で修正し、lint コマンドの pass を確認する。

### Example 3

Input: src/worker/queue.ts の import 並び替え違反を直したい。
Output: 違反箇所を修正後に再検証し、残課題があれば一覧化する。
