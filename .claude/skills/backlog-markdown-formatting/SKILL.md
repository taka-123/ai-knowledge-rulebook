---
name: backlog-markdown-formatting
description: Use when markdown content must be normalized for Backlog readability with consistent headings and checklist structure; When NOT to use: when markdown structure already matches repository and Backlog requirements; Trigger Keywords: [Backlog, markdown整形, 見出し, checklist, issue].
---

# backlog-markdown-formatting

## When to use

- Backlog チケットへ貼り付ける前に Markdown を整形したい場合。
- 議事録・作業メモ・手順書を Backlog issue として起票したい場合。

## When NOT to use

- 既に Backlog 記法で整形済みで追加変換が不要な場合。
- Markdown 以外のファイル（JSON・YAML等）の変換が主目的の場合。

## Trigger Keywords

- Backlog
- markdown整形
- 見出し
- checklist
- issue

## 変換規則

1. 箇条書きは `* ` を使う（`- ` は使わない）。
2. インラインコードは `` ` `` で囲む。
3. コードブロックは ```` ``` ```` で囲む（インデントブロックは使わない）。
4. 見出しは `#` 形式（`===`/`---` の下線形式は使わない）。
5. チェックリストは `- [ ]` / `- [x]` 形式。
6. 太字は `**text**`、斜体は `*text*`。
7. 表は Backlog がサポートする `|---|` 形式のみ。

## Procedure

1. 入力 Markdown をそのまま保持し、変換前の状態を基準として把握する。
2. 上記変換規則を上から順に適用する（箇条書き → コード → 見出し → チェックリスト → 装飾 → 表）。
3. Backlog 固有記法（`[[リンク]]` 等）が含まれている場合は壊さない。
4. 変換後 Markdown を出力し、変換ポイントが多い場合のみ「主な変換点」を3行以内で補足する。

## Output Contract

- 変換後 Markdown のみを返す（過剰な解説は不要）。
- 元文の意味・構造を変えない（箇条書きの順序・内容を変えない）。
- 変換規則に当てはまらない記法は触らない。

### NG例

```
❌ 「- 項目A」→ 変換しない（箇条書きは必ず「* 」に統一）
❌ インデントで字下げしたコードブロックをそのまま残す
❌ 「======」見出しを「# 」に変換し忘れる
```

## Examples

### Example 1

Input: 議事録を Backlog issue にしたい（`-` 箇条書きと下線見出しが混在）。
Output: `* ` 箇条書きと `#` 見出しに統一した整形済み Markdown を返す。

### Example 2

Input: 手順書に `` ` `` なしのコマンドが含まれている。
Output: 全コマンドをインラインコードまたはコードブロックで囲んで返す。

### Example 3

Input: チェックリストが `-` 箇条書きで書かれていて、完了状態が不明。
Output: `- [ ]` / `- [x]` 形式のチェックリストに変換して返す。
