---
name: backlog-markdown-formatting
description: |
  Use when: Backlogチケット向けにMarkdown整形を依頼された場合。既存文書をBacklog表示崩れなく貼り付けたい場合。
  When NOT to use: 既にBacklog記法へ整っており変換不要な場合。Markdown以外（コード修正・設計変更）が主目的の場合。
  Trigger Keywords: [Backlog, backlog記法, markdown整形, issue整形, チケット整形]
---

# backlog-markdown-formatting

Backlog 貼り付け前提の Markdown を、固定規則で正規化する。

## Procedure

1. `docs/transform-rules.md` を Read で参照し、規則に従って箇条書き / 見出し / コード / 表を変換する。
2. Backlog 固有記法（`BLG-95`, `[[WikiPage]]`, `#rev(...)` 等）は保持する。
3. 変換後の Markdown のみを返す。変更が大きい場合のみ「主な変換点」を 3 行以内で添える。

## ルール（必守）

- 箇条書きは `* `（`- ` 不可）。
- ネストは半角スペース 4 つ（2 つ不可）。
- 元文の意味は変えない。

## Examples

- Input: 進捗報告 Markdown を Backlog 用に整形。
  Output: `* ` 箇条書き・ATX 見出し・4 スペースネストに統一した Markdown。
- Input: `- ` と `* ` が混在した Markdown。
  Output: 全て `* ` に統一・ネスト 4 スペースに整えた Markdown。
