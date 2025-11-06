---
description: Prepare focused review notes for current documentation changes
allowed-tools: Bash(git status:*), Bash(git diff --stat), Bash(git diff --unified=0 -- '*.md' '*.mdx' '*.json' '*.yaml' '*.yml')
---

## Capture Current Changes

- Working tree status: !`git status --short`
- Diffstat summary: !`git diff --stat`
- Documentation-only diff (no context lines): !`git diff --unified=0 -- '*.md' '*.mdx' '*.json' '*.yaml' '*.yml'`

## Review Preparation

1. 変更されたドキュメントを用途別（ガイド／リファレンス／設定ファイルなど）に分類してください。
2. 各分類でレビュー時に注目すべきポイントをチェックリスト形式（`- [ ]`）で列挙してください：
   - 出典の有無（URL + 取得日）
   - FrontMatter の必須項目（`created`, `updated`, `tags`）
   - スキーマ整合性（JSON Schema 準拠）
   - リンク切れの確認
   - コードブロックの言語指定
3. 各チェック項目に対して現状のステータスを ✅/⚠️/🔴 で示してください：
   - ✅ 問題なし
   - ⚠️ 要確認（軽微な問題）
   - 🔴 要修正（重大な問題）
4. 想定されるリスクや追加確認事項があればまとめてください。
