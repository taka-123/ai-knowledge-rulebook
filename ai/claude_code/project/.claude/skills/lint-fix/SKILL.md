---
name: lint-fix
description: Use when lint or format checks fail and deterministic repository commands must be applied to fix issues; When NOT to use: when there is no failing lint signal or the task is architecture design only; Trigger Keywords: [lint, format, markdownlint, prettier, yamllint].
---

# lint-fix

## When to use

- lint 出力に基づく修正を機械的に進める必要がある場合。
- 複数ディレクトリにまたがる整形崩れを一括修正したい場合。

## When NOT to use

- 失敗ログがなく推測のみで修正対象を決める場合。
- 設計議論のみで実ファイル修正が不要な場合。
- 今回変更していないファイルや箇所への formatter 実行（差分が無関係に広がるため禁止）。

## Trigger Keywords

- lint
- format
- markdownlint
- prettier
- yamllint

## Procedure

1. 失敗コマンドとエラーログを固定する。ログがなければプロジェクトの format/lint チェックコマンドを先に実行する。
2. **今回変更した箇所のみ**を対象に自動修正を適用する（新規ファイルはファイル全体でよいが、既存ファイルは変更箇所に限定し、無関係な差分を出さない）。
3. 自動修正で残った項目だけを手動で最小修正する（挙動変更を入れない）。
4. 同じコマンドを再実行し、失敗件数が 0 になったことを確認する。
5. 変更ファイルと修正理由を 1 行ずつ記録する。

## Output Contract

- 必ず「失敗コマンド / 修正内容 / 再実行結果 / 未解決」を出す。
- 未解決がある場合は、次に必要な追加情報（ログや環境差）を 1 つだけ要求する。
- リファクタや命名変更など、lint解消と無関係な変更は含めない。

## Examples

### Example 1

Input: API ハンドラファイルで prettier エラーが出ている。
Output: 該当ファイルのみ修正し、format check の再実行結果を記録する。

### Example 2

Input: 設定ファイルとビルドスクリプト周辺の行末空白を解消したい。
Output: 最小差分で修正し、lint コマンドの pass を確認する。

### Example 3

Input: キューワーカーの import 並び替え違反を直したい。
Output: 違反箇所を修正後に再検証し、残課題があれば一覧化する。
