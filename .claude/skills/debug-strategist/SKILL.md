---
name: debug-strategist
description: Use when failures require hypothesis-driven debugging with reproducible steps, logs, and narrowed root cause candidates; When NOT to use: routine formatting tasks with obvious fixes; Trigger Keywords: debug, 不具合, 再現, stacktrace, root cause.
---

# debug-strategist

## When to use

- 原因不明の失敗を再現可能な形で切り分ける必要がある。
- ログと期待値の差分から根本原因を特定したい。

## When NOT to use

- フォーマットのみの単純修正。
- 再現手順が不要な既知エラー。

## Trigger Keywords

- debug
- 不具合
- 再現
- stacktrace
- root cause

## Examples

### Example 1

Input: `schema:check` が時々失敗する原因を調べて。
Output: 入力データを固定し、失敗条件を最小再現して、候補原因を優先度順で提示する。

### Example 2

Input: ルール適用が環境によって変わる不具合を切り分けたい。
Output: 読み込みパスと階層差分を収集し、再現条件を明示した上で修正案を示す。

### Example 3

Input: CI では落ちるがローカルでは通る理由を調査して。
Output: 実行コマンド、バージョン差、パス依存を比較し、検証ログ付きで根本原因候補を提示する。
