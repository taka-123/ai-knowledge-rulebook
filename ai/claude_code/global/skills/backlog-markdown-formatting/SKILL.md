---
name: backlog-markdown-formatting
description: Reformats Markdown text to comply with Backlog rendering rules. Use when the user requests Backlog-compatible formatting or mentions "バックログ用", "Backlog記法", or pasting content into Backlog.
---

# Skill: Backlog Markdown Formatting

Backlog貼り付け前提のMarkdownを、以下の規則で正規化せよ。

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
2. 変換規則に従って文法を統一する（箇条書き、見出し、コード、表）。
3. Backlog固有記法が壊れていないことを確認する。
4. 変換後のMarkdownを返し、必要時のみ変換ポイントを短く補足する。

## 変換規則

1. 箇条書きは `* ` を使う（`- ` は使わない）。
2. ネストは半角スペース4つで統一する（タブ禁止、2スペース禁止）。
3. 番号付きリストは `1. ` 形式を使う。
4. 見出しは ATX 形式（`#`）で統一する。
5. 引用は各行 `> ` で始める。空行は `>` 行で表す。
6. コードはフェンス付きコードブロック（3連バッククォート）を使う。
7. 罫線は `---` に統一する。
8. 強調はアスタリスクへ統一する（`*italic*`, `**bold**`）。
9. リンクは `[text](url)`、画像は `![alt](url)` を使い、タイトル属性は付けない。
10. テーブルは `|` を使うGFM形式に統一する。
11. 定義リストと `<details>` は通常テキストへ展開する。
12. Backlog固有記法（`BLG-95`, `[[WikiPage]]`, `#rev(...)`）は保持する。

## 優先ルール

- 本スキルが発火した場合、一般的なMarkdown慣習より上記規則を優先せよ。
- 入力に混在ルールがある場合は、出力を上記規則へ寄せる。

## Output Contract

- 変換後Markdownのみを返す（解説は最小限）。
- 元文の意味を変えない。
- 変更点が大きい場合は「主な変換点」を3行以内で添える。
