---
name: content-scaffold
description: Use when new markdown or rule files must be created from repository-specific templates with concrete commands and validation criteria; When NOT to use: modifications to already complete files that need no scaffolding; Trigger Keywords: 新規ファイル, scaffold, テンプレート, 雛形, 初期化.
---

# content-scaffold

## When to use

- 新規ドキュメントやルールを追加する。
- 既存規約に沿った雛形が必要。

## When NOT to use

- 既存ファイルの小修正のみ。
- 雛形不要な単発回答。

## Trigger Keywords

- 新規ファイル
- scaffold
- テンプレート
- 雛形
- 初期化

## Examples

### Example 1

Input: 新しい運用手順書を作るので骨組みを生成して。
Output: 見出し、入力条件、実行手順、検証項目を含む markdown 雛形を作成する。

### Example 2

Input: Cursor rule ファイルを追加するテンプレがほしい。
Output: frontmatter と trigger 節を持つ `.mdc` 雛形を生成する。

### Example 3

Input: 検証レポート用の標準フォーマットを作って。
Output: KPI、根拠、テスト結果、残課題の固定セクションを持つ雛形を出す。
