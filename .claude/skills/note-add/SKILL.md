---
name: note-add
description: Use when a new topic note must be created in notes/topics/ with valid FrontMatter and structured content; When NOT to use: when the note already exists and only updates are needed; Trigger Keywords: [ノート追加, note作成, トピック, notes/topics, 新規ノート].
---

# note-add

## When to use

- `notes/topics/` に新しいテーマのノートを追加するとき。
- FrontMatter スキーマ（`schemas/notes.schema.json`）に準拠したノートを素早く生成したいとき。
- 参照元 URL とともに知識を記録するとき。

## When NOT to use

- 既存のノートを更新するだけのとき（Edit を直接使う）。
- FrontMatter が不要なドラフトや一時メモを作成するとき。
- `notes/topics/` 以外のディレクトリへのファイル作成が目的のとき。

## Trigger Keywords

- ノート追加
- note作成
- トピック
- notes/topics
- 新規ノート

## Procedure

1. ユーザーからタイトル・タグ・内容・出典 URL を収集する。完了条件: 必須フィールドが確定。
2. ファイル名を `YYYY-MM-DD-<slug>.md` 形式で決定する（`updated` は今日の日付）。完了条件: ファイルパスが確定。
3. FrontMatter を `schemas/notes.schema.json` の required 項目（`title`, `created`, `updated`, `tags`）に従って生成する。完了条件: 全必須フィールドが揃っている。
4. `notes/topics/<YYYY-MM-DD-slug>.md` にファイルを書き出す。完了条件: ファイルが存在する。
5. `npm run lint:md` を実行して Markdown 構文エラーがないことを確認する。完了条件: Lint エラー 0 件。

## Output Contract

| 項目           | 形式                                                 |
| -------------- | ---------------------------------------------------- |
| ファイルパス   | `notes/topics/YYYY-MM-DD-<slug>.md`                 |
| FrontMatter    | `title`, `created`, `updated`, `tags` を必ず含む    |
| 出典 URL       | `source: "https://..."` または `source: ""`         |
| Lint 結果      | `npm run lint:md: PASS`                             |

### NG例

❌ FrontMatter なしで本文だけ書き出す（スキーマ違反）。

❌ `tags` を配列ではなく文字列で書く（型エラー）。

❌ `created` / `updated` を YYYY-MM-DD 以外の形式にする（format エラー）。

## Examples

### Example 1

Input: MCP（Model Context Protocol）についての学習メモを追加したい。タグは `[mcp, claude, tool]`。
Output: `notes/topics/2026-02-28-mcp-overview.md` が FrontMatter 付きで生成され、`npm run lint:md` が PASS。

### Example 2

Input: Zenn 記事を参考に Cursor のルール設定をまとめたい。出典 URL あり。
Output: `notes/topics/2026-02-28-cursor-rules.md` に `source` フィールド付きで生成。

### Example 3

Input: エージェント設計パターンについてのメモを `[agent, design-pattern]` タグで記録したい。
Output: `notes/topics/2026-02-28-agent-design-patterns.md` が作成され Lint PASS。

### Example 4

Input: Claude Code のフック機能についてのノートを追加したい。出典なし。
Output: `notes/topics/2026-02-28-claude-code-hooks.md` が `source: ""` で生成される。
