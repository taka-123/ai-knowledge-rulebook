---
name: debug-strategist
description: Use when runtime failures require hypothesis-driven debugging with reproducible steps and narrowed root causes; When NOT to use: when formatting-only fixes can be completed without investigation; Trigger Keywords: [debug, 不具合, 再現, stacktrace, root cause].
---

# debug-strategist

## When to use

- 再現手順が必要な実行時不具合を切り分ける場合。
- src/main と src/worker の連携障害を原因別に狭めたい場合。

## When NOT to use

- 単純な整形不備の修正のみを行う場合。
- 失敗が再現せず証跡がない状態で断定する場合。

## Trigger Keywords

- debug
- 不具合
- 再現
- stacktrace
- root cause

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main/server.ts から src/worker/task.ts へのジョブ投入が失敗する。
Output: 仮説を3件に分け、ログ取得ポイントと検証順を提示する。

### Example 2

Input: build.sh 実行時にテスト前で停止する。
Output: 停止位置を再現し、依存コマンド欠落かスクリプト分岐かを判定する手順を示す。

### Example 3

Input: src/common/retry.ts の例外処理が無限ループを起こす。
Output: 入力条件と境界値を定義し、最小再現コードの観点を提示する。
