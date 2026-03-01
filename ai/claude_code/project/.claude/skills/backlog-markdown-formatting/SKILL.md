---
name: backlog-markdown-formatting
description: |
  Use when: Backlogチケット向けにMarkdown整形を依頼された場合。既存文書をBacklog表示崩れなく貼り付けたい場合。
  When NOT to use: 既にBacklog記法へ整っており変換不要な場合。Markdown以外（コード修正・設計変更）が主目的の場合。
  Trigger Keywords: [Backlog, backlog記法, markdown整形, issue整形, チケット整形]
---

# backlog-markdown-formatting

Backlog貼り付け前提のMarkdownを、以下の規則で正規化する。

## When to use

- Backlogチケット向けにMarkdown整形を依頼された場合。
- 既存文書をBacklog表示崩れなく貼り付けたい場合。

## When NOT to use

- 既にBacklog記法へ整っており変換不要な場合。
- Markdown以外（コード修正・設計変更）が主目的の場合。

## Trigger Keywords

- Backlog
- backlog記法
- markdown整形
- issue整形
- チケット整形

## Procedure

1. 入力Markdownをそのまま保持してバックアップとし、変換対象のみを編集する。
2. `docs/transform-rules.md` を Read で参照し、変換規則に従って文法を統一する（箇条書き、見出し、コード、表）。
3. Backlog固有記法が壊れていないことを確認する。
4. 変換後のMarkdownを返し、必要時のみ変換ポイントを短く補足する。

## Output Contract

- 変換後Markdownのみを返す（解説は最小限）。
- 元文の意味を変えない。
- 変更点が大きい場合は「主な変換点」を3行以内で添える。

### NG例

❌ `- ` で箇条書きする（Backlog では `* ` を使用）。

❌ ネストに半角スペース2つを使う（4つに統一）。

❌ Backlog固有記法（`BLG-95`, `[[WikiPage]]`, `#rev(...)`）を変換・削除する（保持必須）。

❌ 元文の意味を変えないという制約を無視して大幅に書き換える。

## Examples

### Example 1

Input: チケットに貼るための進捗報告 Markdown を整形してほしい。
Output: `* ` 箇条書き・ATX 見出し・4スペースネストに統一した変換後 Markdown。

### Example 2

Input: 既存の設計書を Backlog の Wiki に貼りたい。表とコードブロックがある。
Output: GFM 表・フェンス付きコードブロックに統一した Markdown と主な変換点 3 行。

### Example 3

Input: 「以下をバックログ用に」と送ってきた Markdown（`- ` と `* ` が混在）。
Output: 全箇条書きを `* ` に統一し、ネストを4スペースに統一した Markdown。
