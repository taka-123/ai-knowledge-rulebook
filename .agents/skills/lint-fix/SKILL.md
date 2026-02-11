---
name: lint-fix
description: Resolve lint/format/schema failures with minimal edits. Auto-trigger keywords: lint, format, prettier, markdownlint, yamllint, schema, test, CI.
---

# Lint Fix

## ワークフロー

1. 失敗している lint/format/schema コマンドを特定する。
2. 失敗ルールを満たす最小のパッチを適用する。
3. 必要な検証コマンドのみを再実行する。
4. pass/fail と残存リスクを報告する。

## 安全規約

- 大量ファイルを変更する自動修正はユーザー確認が必要。
