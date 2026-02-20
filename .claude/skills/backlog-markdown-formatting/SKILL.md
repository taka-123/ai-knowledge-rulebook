---
name: backlog-markdown-formatting
description: Use when markdown content must be normalized for Backlog readability with consistent headings and checklist structure; When NOT to use: when markdown structure already matches repository and Backlog requirements; Trigger Keywords: [Backlog, markdown整形, 見出し, checklist, issue].
---

# backlog-markdown-formatting

## When to use

- Backlog チケット用に Markdown を整形する場合。
- src/main や build.sh の作業記録を読みやすく整理する場合。

## When NOT to use

- 既に規約準拠で追加整形が不要な場合。
- Markdown 以外のファイルのみを扱う場合。

## Trigger Keywords

- Backlog
- markdown整形
- 見出し
- checklist
- issue

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/worker 障害対応メモを Backlog 登録したい。
Output: 見出し階層、チェックリスト、再現手順を整形して提示する。

### Example 2

Input: build.sh 更新手順書をチーム共有向けに整えたい。
Output: 手順番号と検証項目を統一フォーマットへ変換する。

### Example 3

Input: src/common 仕様変更の議事録を issue 化したい。
Output: 決定事項と未決事項を分離した Markdown に整える。
