---
name: schema-guard
description: Validate ai/ and notes/ JSON against schemas/. Auto-trigger keywords: schema, json validation, ai profile, notes json, スキーマ検証.
---

# Schema Guard

## ワークフロー

1. `npm run schema:check` を実行する。
2. 失敗時は不適合ファイルとフィールドを特定する。
3. 最小限のデータ側修正を提案する（承認なしにスキーマを緩和しない）。
4. 再検証を実行し結果を報告する。
