---
description: Apply automated formatting to all code and documentation files
allowed-tools: Bash(./format.sh fix)
---

## Execute Formatting

- Run format script: !`./format.sh fix`

## Reporting

1. 整形結果を ✅/⚠️/🔴 で報告してください：
   - ✅ 正常に整形完了
   - ⚠️ 一部ファイルでエラー（処理は継続）
   - 🔴 整形スクリプトが失敗
2. 整形されたファイル数とカテゴリ（コード / ドキュメント / 設定）を報告してください。
3. 大量の変更があった場合は、主要な変更パターン（例: インデント統一、末尾改行追加）を列挙してください。
4. 整形後に `/ci-check` での検証を推奨してください。
