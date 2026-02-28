---
name: frontmatter-audit
description: Use proactively when editing any note under notes/ and verifying FrontMatter fields against schemas/notes.schema.json; When NOT to use: when targets are non-note Markdown files such as AGENTS.md or CLAUDE.md; Trigger Keywords: [frontmatter, ノート検証, notes lint, メタデータ, schema].
---

# frontmatter-audit

## When to use

- `notes/` 配下の Markdown ファイルが `schemas/notes.schema.json` に準拠しているか確認するとき。
- `title`・`created`・`updated`・`tags` などの必須フィールド欠落を一括検出するとき。
- `updated` フィールドが古いままのノートを更新前に洗い出すとき。

## When NOT to use

- FrontMatter を持たないドキュメント（README、AGENTS.md 等）を対象とするとき。
- ノートの本文コンテンツの品質を評価するとき（`code-reviewer` が適切）。
- JSON スキーマを変更する必要があるとき（`schema-guard` が適切）。

## Trigger Keywords

- frontmatter
- FrontMatter
- ノート検証
- notes lint
- メタデータ

## Procedure

1. `glob 'notes/**/*.md'` で対象ファイルを列挙する。完了条件: 対象ファイル一覧が確定。
2. 各ファイルの FrontMatter ブロック（`---`〜`---`）を抽出し、必須フィールド（`title`, `created`, `updated`, `tags`）の有無を確認する。完了条件: 全ファイルの必須フィールド有無が判定済み。
3. `source` フィールドが存在する場合、値が空文字または `https?://` 形式であることを確認する。完了条件: URL 形式違反が特定済み。
4. 違反ファイルのみ最小差分でフィールドを追加・修正する。完了条件: 修正箇所が最小限。
5. `npm run lint:md` を実行して Markdown 構文エラーがないことを確認する。完了条件: Lint エラー 0 件。

## Output Contract

| 項目           | 形式                                                      |
| -------------- | --------------------------------------------------------- |
| 対象ファイル数 | 数値                                                      |
| 違反ファイル   | `path/to/file.md: missing field 'updated'` 形式           |
| 修正内容       | 変更フィールドの一覧                                      |
| Lint 結果      | `npm run lint:md: PASS/FAIL`                             |

### NG例

❌ FrontMatter 以外の本文を修正する（責務外の変更）。

❌ `schemas/notes.schema.json` を読まずにフィールドを推測で追加する（型違反リスク）。

❌ 違反のないファイルにも手を加える（不要な差分）。

## Examples

### Example 1

Input: `notes/topics/` 配下のすべての Markdown が FrontMatter を持っているか確認したい。
Output: 対象 N ファイル中 M ファイルに違反あり、違反内容をファイルパス・フィールド名で一覧化。

### Example 2

Input: `notes/topics/mcp.md` に `updated` フィールドが欠落していると警告された。
Output: `updated: 2026-02-28` を FrontMatter に追加し、`npm run lint:md` が PASS。

### Example 3

Input: `source` フィールドの URL 形式が正しいか確認したい。
Output: 形式違反の URL を持つファイルを抽出し、空文字または正規化済み URL へ修正。
