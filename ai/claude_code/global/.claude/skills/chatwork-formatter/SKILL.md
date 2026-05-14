---
name: chatwork-formatter
description: "Use when markdown content must be converted to ChatWork-readable format and presented as a copyable block in the conversation; When NOT to use: when the destination supports markdown rendering or when the task is not ChatWork-related; Trigger Keywords: [ChatWork, CW, チャットワーク, CW用, ChatWork用, CWで共有, CWの返信]."
---

# chatwork-formatter

Markdown を ChatWork 記法に変換し、コピー可能ブロックとして会話内に提示する。

## Procedure

1. `docs/transform-rules.md` を Read で参照し、変換規則に従って全文を変換する。
2. 構造（見出し・セクション）を含む場合は `[info]...[/info]` で全体を囲む。
3. 「👇 CWにそのままコピーしてください」を 1 行出力し、続けて変換済みテキストをコードブロックで提示する。

## ルール（必守）

- ファイルへ保存しない（会話内提示のみ）。
- 指示なしに絵文字を追加しない。
- `[title]` は `[info]` の内側でのみ使う。
- 元文の意味・構成は変えない。

## Examples

### Example 1: 構造を含む Markdown

Input:

```markdown
## 進捗報告

- 設計完了
- 実装中
  - APIレイヤー完了
  - DBレイヤー未着手
```

Output:

👇 CWにそのままコピーしてください

```
[info]
▼ 進捗報告

・設計完了
・実装中
　・APIレイヤー完了
　・DBレイヤー未着手
[/info]
```

### Example 2: 構造を持たない返信文（`[info]` 不要）

Input: 「承認した旨と次のステップを伝える返信文」
Output:

👇 CWにそのままコピーしてください

```
承認しました。

次のステップは以下の通りです。
・〇〇 の対応をお願いします。
・完了後にこちらのスレッドへご連絡ください。
```

### Example 3: 番号付きリスト + コードブロック

Input: H1 見出し + 番号付きリスト + bash コードブロック 2 つを含む Markdown。

Output:

👇 CWにそのままコピーしてください

```
[info]
[title]セットアップ手順[/title]

1. 依存をインストール
[code]npm install[/code]

2. 起動
[code]npm run dev[/code]
[/info]
```
