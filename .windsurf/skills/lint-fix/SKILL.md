---
name: lint-fix
description: Fix lint/format/schema issues with minimal edits. Auto-trigger keywords: lint, format, prettier, markdownlint, yamllint, schema, CI, test.
---

# Lint Fix

## ワークフロー

1. 失敗しているコマンドを検出する。
2. 問題箇所のみを修正する。
3. 最小限の再検証を実行する。
4. pass/fail と残存問題を報告する。
