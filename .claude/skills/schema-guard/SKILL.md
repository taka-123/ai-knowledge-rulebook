---
name: schema-guard
description: ai/ と notes/ の JSON が schemas/ で定義されたスキーマに適合するか検証するスキル。キーワード「schema」「json validation」「ai profile」「notes json」「スキーマ検証」で自動検出。
user-invocable: true
allowed-tools: Read, Bash
disable-model-invocation: true
---

# Schema Guard

`ai/` と `notes/` 配下の JSON ファイルが `schemas/` で定義されたスキーマに適合するか検証する。

## 実行手順

1. `npm run schema:check` を実行する。
2. 失敗した場合、出力から対象ファイルと不適合フィールドを特定する。
3. 最小限の修正を提示し、再実行で検証を確認する。

## 判定ルール

- スキーマ自体は明示的な指示がない場合は変更しない。
- データファイルの修正をスキーマの緩和より優先する。

## 出力形式

```markdown
## Schema Guard 検証結果

- **コマンド**: npm run schema:check
- **結果**: pass / fail
- **問題**: [不適合ファイルとフィールド]
- **修正方針**: [最小限の変更内容]
- **再検証**: 実施済み / 未実施
```

## 制約

- 検証コマンドの出力を必ず報告に含める。
- 再チェックの結果も報告する。
