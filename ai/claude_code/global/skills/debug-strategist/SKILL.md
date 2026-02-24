---
name: debug-strategist
description: Use when runtime failures require hypothesis-driven debugging with reproducible steps and narrowed root causes; When NOT to use: when formatting-only fixes can be completed without investigation; Trigger Keywords: [debug, 不具合, 再現, stacktrace, root cause].
---

# debug-strategist

## When to use

- 再現手順が必要な実行時不具合を切り分ける場合。
- モジュール間の連携障害を原因別に狭めたい場合。

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

1. 失敗現象を 1 行で固定し、再現コマンドと期待値/実際値を分離する。
2. ログ・スタックトレース・直近差分を収集する（`rg`, `git diff`, 実行ログ）。
3. 仮説を 3 件作り、各仮説に「反証できる最短テスト」を 1 つずつ付ける。
4. 検証コストが低い順にテストし、外れ仮説を明示的に捨てる。
5. 当たり仮説に対して最小差分修正を行い、同じ再現コマンドで再検証する。
6. 回帰観点を 1〜3 件だけ追加確認して報告する。

## Output Contract

- 必ず「症状 / 仮説A-B-C / 検証結果 / 採用修正 / 残リスク」を出す。
- 仮説は断定口調で書かず、検証結果とセットで確度を示す。
- 修正案が複数ある場合は、最小差分案を推奨として先頭に置く。

### NG例

❌ 再現手順なしに断定する（証跡不足）。

❌ 仮説を検証せずに修正を適用する（根拠なき変更）。

❌ 推測で処理を続行する（失敗時は Status で停止する）。

## Examples

### Example 1

Input: API サーバーからワーカーへのジョブ投入が失敗する。
Output: 仮説を3件に分け、ログ取得ポイントと検証順を提示する。

### Example 2

Input: CI スクリプト実行時にテスト前で停止する。
Output: 停止位置を再現し、依存コマンド欠落かスクリプト分岐かを判定する手順を示す。

### Example 3

Input: リトライ処理の例外ハンドリングが無限ループを起こす。
Output: 入力条件と境界値を定義し、最小再現コードの観点を提示する。
