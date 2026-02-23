---
name: backlog-markdown-formatting
description: Use when markdown text must be reformatted for Backlog-compatible readability and checklist structure; When NOT to use: when markdown already follows Backlog formatting rules; Trigger Keywords: [Backlog, markdown整形, 見出し, checklist, issue].
---

# backlog-markdown-formatting

## When to use

- `.work/AI_SCAN.md` や `.work/AI_BLUEPRINT.md` を Backlog チケットへ貼り付ける前に整形したいとき。
- `npx markdownlint-cli2 .work/AI_BLUEPRINT.md` は通るが、Backlog 表示で箇条書き崩れが出るとき。
- `README.md` から抜粋した運用手順を Backlog 用に再整形したいとき。

## When NOT to use

- Backlog ではなく GitHub README 用の体裁を維持したいとき。
- コードブロック内容や技術仕様そのものを変更する必要があるとき。
- 単なる typo 修正で整形変換が不要なとき。

## Trigger Keywords

- Backlog
- markdown整形
- checklist
- 見出し
- issue

## Procedure

1. `cat .work/AI_SCAN.md` など対象 Markdown を確認し、変換対象を明確化する。完了条件: 元文の節構成を把握済み。
2. 箇条書き・見出し・チェックリストを Backlog 表示前提の記法に統一する。完了条件: 箇条書き記号と階層が一貫。
3. コードブロックとリンクは意味を変えずに維持し、本文のみ整形する。完了条件: コード内容差分がない。
4. `npx markdownlint-cli2 .work/AI_SCAN.md` を実行し、Markdown 構文エラーがないことを確認する。完了条件: 0 error。
5. 変換前後の主要差分を 3 点以内で要約する。完了条件: 差分説明が過不足なく記録。

## Output Contract

| 項目 | 形式 |
| --- | --- |
| Target | `path/to/file.md` |
| Reformatted Sections | `1. ...` の番号リスト |
| Verification | `npx markdownlint-cli2 .work/AI_SCAN.md: PASS/FAIL` |
| Notes | 変換時の注意点（任意） |

### NG例

❌ 原文の意味を変える要約を加える（要件逸脱）。

❌ コードブロック内まで自動整形する（実装内容を破壊）。

❌ 検証コマンドを実行せずに完了報告する（再現性不足）。

## Examples

### Example 1

Input: `.work/AI_SCAN.md` を Backlog チケット本文へ貼る前に整形したい。
Output: 整形済み Markdown と `npx markdownlint-cli2 .work/AI_SCAN.md` の結果表。

### Example 2

Input: `.work/AI_BLUEPRINT.md` のチェックリストを Backlog で崩れない形式へそろえたい。
Output: 箇条書き階層を統一した修正版と差分サマリ。

### Example 3

Input: `README.md` の運用手順を Backlog 用にコピーするため見出しレベルを調整したい。
Output: 見出し/箇条書き調整後の Markdown と変更点 3 件。
