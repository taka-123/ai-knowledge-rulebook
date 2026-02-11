---
name: lint-fix
description: Fix lint/format/schema errors with minimal diffs. Auto-trigger keywords: lint, format, prettier, markdownlint, yamllint, schema, test, CI.
---

# Lint Fix

## ワークフロー

1. 失敗しているチェックを特定する。
2. 最小限の影響範囲にパッチを適用する。
3. 対象を絞って再検証する。
4. 未解決項目を報告する。
