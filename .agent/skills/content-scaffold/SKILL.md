---
name: content-scaffold
description: Apply templates and validate required fields for new files. Auto-trigger keywords: new file, template, scaffold, note creation, 新規ファイル, ノート作成, 新規追加.
---

# Content Scaffold

## ワークフロー

1. 対象ディレクトリ（notes/ clips/ ai/ snippets/）を検出し、テンプレートを選択する。
2. 必須フィールドを埋めた状態でファイルを生成する。
3. `./format.sh check` と `npm run schema:check`（JSON の場合）を実行する。
4. 生成結果と検証ステータスを報告する。
