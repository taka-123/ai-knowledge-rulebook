---
name: debug-strategist
description: Diagnose errors with reproduce-isolate-fix flow. Auto-trigger keywords: debug, bug, error, stacktrace, flaky, failing test, CI failure.
---

# Debug Strategist

## ワークフロー

1. 最小のコマンドまたはシナリオで問題を再現する。
2. 対象ファイル・トレースを絞り込み、根本原因を特定する。
3. 最小限の安全な修正案と影響範囲を提示する。
4. 関連するテスト/lint コマンドで検証する。
5. 修正に deploy/migration/破壊的 git 操作が必要な場合はエスカレーションする。

## 安全規約

- <SCRUTINY_REQUIRED> `deploy`, `migrate`, `terraform apply`, `git push --force` は承認必須。
