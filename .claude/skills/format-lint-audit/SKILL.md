---
name: format-lint-audit
description: Use when final quality gates must confirm format and lint checks with explicit pass or fail evidence; When NOT to use: when implementation is still exploratory and files are not ready for final verification; Trigger Keywords: [quality gate, format:check, lint, CI, 検証].
---

# format-lint-audit

## When to use

- 完了前に品質ゲートを明示的に通す必要がある場合。
- src/main、src/worker、src/common、build.sh の最終検証をまとめる場合。

## When NOT to use

- 作業途中で頻繁に設計が変わる段階の場合。
- 実行環境が未整備で検証コマンドを走らせられない場合。

## Trigger Keywords

- quality gate
- format:check
- lint
- CI
- 検証

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main の改修完了後に最終品質確認をしたい。
Output: format:check と lint の結果を PASS/FAIL で報告する。

### Example 2

Input: build.sh 変更後に回帰確認を一括実行したい。
Output: 実行コマンド、終了コード、残課題を一覧化する。

### Example 3

Input: src/common の更新を PR 前に監査したい。
Output: 品質ゲート観点で不適合有無を判定する。
