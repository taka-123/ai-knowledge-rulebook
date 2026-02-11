---
name: format-lint-audit
description: Run format/lint checks and report results. Auto-trigger keywords: format, lint, prettier, markdownlint, yamllint, lint error, 整形, 検証, CI通過確認.
---

# Format Lint Audit

## ワークフロー

1. `./format.sh check` を実行する。
2. 変更ファイルの種類に応じて個別チェックを実行する（`npm run lint:md`, `lint:yaml`, `lint:json`）。
3. ツールごとに pass/fail をエラー詳細付きで報告する。
4. 最小限の修正を提案する。承認なしに自動修正は行わない。
